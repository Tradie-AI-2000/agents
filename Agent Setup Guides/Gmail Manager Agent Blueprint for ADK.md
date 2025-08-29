# Prerequisites

Before you begin, ensure you have the following installed:

* **Google Cloud SDK (`gcloud` CLI):** For authenticating and managing Google Cloud resources.
* **Python 3.10 or higher:** The project is built with Python.
* **`curl`:** Used by the `Makefile` to install `uv`.

---

**Gmail Manager Agent Blueprint for ADK**

This document serves as a comprehensive blueprint for designing, implementing, testing, and deploying a Gmail Manager multi-agent system using the Google Agent Development Kit (ADK). It is intended as a reusable guide for creating similar Gmail-centric agents for various clients.

## 1. Project Overview

**Problem Statement:** The goal is to create an ADK-powered multi-agent system to manage a Gmail account. The agent must selectively draft replies only for emails from real people that require a direct response, while categorizing all emails and preparing drafts for final approval. The system must operate with a polling interval of 30 minutes, and all drafted replies must adhere to a casual, friendly, and professional tone.

**High-Level Design Plan:**

This multi-agent system uses a Coordinator/Dispatcher pattern to manage a workflow of specialized sub-agents. The workflow is a Sequential Pipeline, processing each new unread email through a series of steps. The primary interaction model is LLM-driven delegation for task handoffs and shared session state for passing email data between agents. A crucial filtering step is integrated into the initial CategorizationAgent to prevent unnecessary processing.

**Agent Hierarchy:**

* **Coordinator Agent:** `GmailCoordinator` (CustomAgent) - The root agent that orchestrates the entire workflow.
* **Specialist Agents:**
* `CategorizationAgent` (LlmAgent)
* `DraftingAgent` (LlmAgent)
* `_calendar_tool_caller` (LlmAgent) - Internal agent used by `GmailCoordinator` to call `CalendarAgent`.
* `CalendarAgent` (LlmAgent)
* `SenderAgent` (LlmAgent)

**Agent Roles & Interaction Model:**

* **`GmailCoordinator` (CustomAgent):**
* **Function:** Acts as the central dispatcher. It polls for new unread emails (or processes the most recent for testing), passes the email object to the `CategorizationAgent`, and then conditionally delegates to subsequent agents based on the output.
* **Interaction:** Uses programmatic control flow (`_run_async_impl`) to orchestrate sub-agents. It inspects the output of `CategorizationAgent` and `DraftingAgent` to make decisions. It manages `ctx.session.state` to pass data.
* **`CategorizationAgent` (LlmAgent):**
* **Function:** Reads the email's subject and body, assigns labels, and determines if the email requires a direct, human-to-human reply.
* **Output Schema:** Pydantic model with `labels: list[str]` and `requires_reply: bool`.
* **Interaction:** Receives email content from `GmailCoordinator`. Its output is stored in `ctx.session.state` via `output_key`.
* **`DraftingAgent` (LlmAgent):**
* **Function:** Drafts a response to the email. Its instruction defines the tone: "casual, friendly, and professional."
* It includes a `[CALENDAR_REQUEST]` placeholder if a meeting is suggested.
* **Output Schema:** Pydantic model with `response_body: str`, `subject: str`, and `to_address: str`.
* **Interaction:** Receives email context from `GmailCoordinator`. Its output is stored in `ctx.session.state` via `output_key`.
* **`_calendar_tool_caller` (LlmAgent):**
* **Function:** A specialized internal agent whose sole purpose is to call the `CalendarAgent` tool.
* **Tool Integration:** Uses `AgentTool(CalendarAgent)`.
* **Interaction:** Called by `GmailCoordinator` if `[CALENDAR_REQUEST]` is detected. Its output is stored in `ctx.session.state` via `output_key`.
* **`CalendarAgent` (LlmAgent):**
* **Function:** Generates a Google Calendar booking link and a brief message.
* **Tool Integration:** Uses a custom Python function (`generate_calendar_link`).
* **Interaction:** Called as a tool by `_calendar_tool_caller`. Its output is returned to `_calendar_tool_caller`.
* **`SenderAgent` (LlmAgent):**
* **Function:** Assembles the final draft email and places it in the user's Gmail Drafts folder using the Gmail API.
* **Tool Integration:** Uses a custom Python function (`create_draft_in_gmail`).
* **Interaction:** Receives email details (subject, body, to) via `new_message` from `GmailCoordinator`. Its instruction guides it to use the `create_draft_in_gmail` tool.

## 2. GCP Setup (One-Time)

These steps configure your Google Cloud environment with all necessary resources and permissions. This is a one-time setup per Google Cloud Project.

### 2.1. Authenticate and Set Project

```bash
# Log in to Google Cloud  
gcloud auth login

# Set up Application Default Credentials for libraries  
gcloud auth application-default login

# Set your target project (replace YOUR_PROJECT_ID)  
gcloud config set project YOUR_PROJECT_ID  
```

### 2.2. Enable Required APIs

```bash
# This command enables all necessary APIs at once  
gcloud services enable aiplatform.googleapis.com storage.googleapis.com cloudbuild.googleapis.com run.googleapis.com artifactregistry.googleapis.com  
```

### 2.3. Link Billing Account (If not already enabled)

```bash
# First, run this command to find your available billing account ID:  
gcloud billing accounts list

# Copy the full ID from the ACCOUNT_ID column. Then, use that ID to link it:  
gcloud billing projects link YOUR_PROJECT_ID --billing-account=YOUR_BILLING_ACCOUNT_ID  
```

### 2.4. Create GCS Staging Bucket

```bash
# Use your project ID to create a globally unique bucket name  
# Replace YOUR_PROJECT_ID and YOUR_LOCATION (e.g., us-central1)  
gcloud storage buckets create gs://YOUR_PROJECT_ID-adk-staging --project=YOUR_PROJECT_ID --location=YOUR_LOCATION  
```

### 2.5. Grant Required IAM Permissions

```bash
# Get your email address  
export USER_EMAIL=$(gcloud config get-value account)

# Grant the necessary roles to your user account  
gcloud projects add-iam-policy-binding YOUR_PROJECT_ID --member="user:$USER_EMAIL" --role="roles/aiplatform.user"  
gcloud projects add-iam-policy-binding YOUR_PROJECT_ID --member="user:$USER_EMAIL" --role="roles/iam.serviceAccountTokenCreator"  
```

## 3. Project Setup

This section details the creation of the ADK project and its initial structure.

### 3.1. Project Creation

```bash
# Create the project directory  
mkdir gmail_manager  
cd gmail_manager

# Create the core directory structure  
mkdir -p app/sub_agents/categorization_agent \
         app/sub_agents/drafting_agent \
         app/sub_agents/calendar_agent \
         app/sub_agents/sender_agent

# Create __init__.py files  
touch app/__init__.py \
      app/sub_agents/__init__.py \
      app/sub_agents/categorization_agent/__init__.py \
      app/sub_agents/drafting_agent/__init__.py \
      app/sub_agents/calendar_agent/__init__.py \
      app/sub_agents/sender_agent/__init__.py  

# # # 3.1.1. Create `.env` File (Moved from Section 2.6)

After creating the project structure, create a `.env` file in your project's `app/` directory (or copy `app/.env.example` to `app/.env`) and populate it with your specific Google Cloud project details. This file should **never** be committed to version control.

```python  
# GCP Configuration  
GOOGLE_CLOUD_PROJECT="your-gcp-project-id"  
GOOGLE_CLOUD_LOCATION="your-gcp-location" # e.g., us-central1  
GOOGLE_CLOUD_STAGING_BUCKET="your-gcp-staging-bucket-name" # e.g., your-gcp-project-id-adk-staging

# Set to true when deploying to Vertex AI  
GOOGLE_GENAI_USE_VERTEXAI="True"

# Gemini API Key (for local development if not using Vertex)  
# GOOGLE_API_KEY="your-gemini-api-key"  
```

```

```

### 3.2. `Makefile` Content

Create a `Makefile` in the project root (`gmail_manager/Makefile`) with the following content:

```makefile
# Automates common development tasks

install:
    @command -v uv >/dev/null 2>&1 || { echo "uv is not installed. Installing uv..."; curl -LsSf https://astral.sh/uv/0.6.12/install.sh | sh; source $HOME/.local/bin/env; }
    uv sync

dev:
    uv run adk web .

lint:
    uv run ruff check . --diff  
    uv run mypy .

deploy-adk:
    uv export --no-hashes --no-header --no-dev --no-emit-project > .requirements.txt && uv run python app/agent_engine_app.py  
```

### 3.3. `pyproject.toml` Content

Create a `pyproject.toml` file in the project root (`gmail_manager/pyproject.toml`) with the following content:

```toml
[project]  
name = "gmail-manager"
version = "0.1.0"  
dependencies = [
   "google-adk==1.7.0",
   "python-dotenv",
   "google-cloud-logging",
   "opentelemetry-sdk",
   "google-api-python-client",
   "google-auth-httplib2",
   "google-auth-oauthlib",
]
requires-python = ">=3.10"

[project.optional-dependencies]  
dev = [
   "ruff",
   "mypy",
   "uv",
]

[tool.ruff.lint]  
select = ["E", "F", "W", "I", "UP", "RUF"]
```

### 3.4. `.env.example` Content

Create an `.env.example` file in `gmail_manager/app/.env.example` with the following content. This serves as a template for your actual `.env` file.

```python
# GCP Configuration  
GOOGLE_CLOUD_PROJECT="your-gcp-project-id"  
GOOGLE_CLOUD_LOCATION="your-gcp-location" # e.g., us-central1  
GOOGLE_CLOUD_STAGING_BUCKET="your-gcp-staging-bucket-name" # e.g., your-gcp-project-id-adk-staging

# Set to true when deploying to Vertex AI  
GOOGLE_GENAI_USE_VERTEXAI="True"

# Gemini API Key (for local development if not using Vertex)  
# GOOGLE_API_KEY="your-gemini-api-key"  
```

## 4. Gmail API Specific Setup

To enable the agent to interact with your Gmail account, you need to configure OAuth 2.0 credentials.

### 4.1. Create OAuth 2.0 Client ID

1. Go to the [Google Cloud Console API Credentials page](https://console.cloud.google.com/apis/credentials).
2. Ensure you are in the correct Google Cloud Project.
3. Click **"+ CREATE CREDENTIALS"** and select **"OAuth client ID"**.
4. For the Application type, choose **"Desktop app"**.
5. Give it a name (e.g., "Gmail Manager Agent").
6. Click **"Create"**.

### 4.2. Download and Place `credentials.json`

1. After creating the client ID, click the "Download JSON" icon next to it in the list.
2. Rename the downloaded file to `credentials.json`.
3. Place this file inside the `gmail_manager/app/` directory.

**Important:** The first time you run the agent, a browser window will open prompting you to authorize access to your Gmail account. After you approve, a `token.json` file will be created in the `gmail_manager/app/` directory, and the agent will be able to create drafts automatically in the future.

## 5. Agent Definitions (Code)

This section provides the complete Python code for all agents and supporting modules.

### 5.1. `app/prompts.py`

```python
# Centralized place for all agent instruction prompts

LABELS = ["Financial", "AI Audit emails", "Personal", "Promotional", "Social Media", "Business"]

COORDINATOR_INSTRUCTION = """
As the GmailCoordinator, your job is to manage an incoming email by processing it through a series of specialist agents.

1.  First, you MUST use the 'categorization_agent' tool to analyze the email's content. This agent will categorize the email with appropriate labels and determine if it requires a reply.

2.  Review the output from the 'categorization_agent'.  
    - If 'requires_reply' is True, you MUST then delegate the task to the 'drafting_agent' to create a response.  
    - If 'requires_reply' is False, your job is done for this email. Simply report back the labels that were assigned and state that no reply is needed.

3.  After the 'drafting_agent' has created a draft, you MUST use the 'sender_agent' tool to save the draft to the user's Gmail account.

4.  Finally, report that the draft has been saved successfully.  
"""

CATEGORIZATION_INSTRUCTION = f"""

You are a specialized agent responsible for email categorization.  
Read the provided email content (subject and body) and perform two tasks:  
1.  Assign one or more labels from this predefined list: {LABELS}  
2.  Determine if the email is from a real person and requires a direct, human-to-human reply. Do not mark newsletters, promotional content, or automated notifications as requiring a reply.

Your output must conform to the specified JSON schema.  
"""

DRAFTING_INSTRUCTION = """

You are a helpful assistant that drafts email replies.  
Your response must have a casual, friendly, and professional tone.

**IMPORTANT STYLE GUIDELINES:**  
- DO NOT use formal sign-offs like "Best wishes," or "Kind regards."  
- DO NOT use formal greetings like "Hello,".  
- DO NOT use formal closings like "Goodbye.".

If the email content suggests scheduling a meeting, you MUST include the exact phrase "[CALENDAR_REQUEST]" in the response_body where the calendar link should go. DO NOT try to generate the link yourself.

Your output must conform to the specified JSON schema, including the recipient's email address.  
"""

CALENDAR_INSTRUCTION = "You are a calendar assistant. Your sole purpose is to generate a Google Calendar booking link and a brief, professional message for scheduling a meeting."

SENDER_INSTRUCTION = """

You are a Gmail assistant. Your purpose is to take a drafted email (subject, body, and recipient) and save it to the user's Gmail Drafts folder using the provided tool.

You will receive the email details in the user's message. Extract the 'Subject:', 'To:', and 'Body:' from the message and use them as arguments for the 'create_draft_in_gmail' tool.  
"""
```

### 5.2. `app/config.py`

```python
# Handles structured configuration  
import os  
from dotenv import load_dotenv  
from pydantic import BaseModel

load_dotenv()

class DeploymentConfig(BaseModel):
   agent_name: str = "gmail-manager-agent"  
   project: str = os.environ["GOOGLE_CLOUD_PROJECT"]  
   location: str = os.environ["GOOGLE_CLOUD_LOCATION"]  
   staging_bucket: str = os.environ["GOOGLE_CLOUD_STAGING_BUCKET"]  
   requirements_file: str = ".requirements.txt"  
   extra_packages: list[str] = ["./app"]

def get_deployment_config() -> DeploymentConfig:
   return DeploymentConfig()
```

### 5.3. `app/gmail_service.py`

```python
import os.path  
import base64  
from email.message import EmailMessage  
import quopri

from google.auth.transport.requests import Request  
from google.oauth2.credentials import Credentials  
from google_auth_oauthlib.flow import InstalledAppFlow  
from googleapiclient.discovery import build  
from googleapiclient.errors import HttpError

# If modifying these scopes, delete the file token.json.  
SCOPES = ["https://www.googleapis.com/auth/gmail.modify"]

TOKEN_PATH = "app/token.json"  
CREDS_PATH = "app/credentials.json"

def get_gmail_service():
    creds = None  
    if os.path.exists(TOKEN_PATH):
        creds = Credentials.from_authorized_user_file(TOKEN_PATH, SCOPES)
    if not creds or not creds.valid:
        if creds and creds.expired and creds.refresh_token:
            creds.refresh(Request())
        else:
            flow = InstalledAppFlow.from_client_secrets_file(CREDS_PATH, SCOPES)
            creds = flow.run_local_server(port=0)
        with open(TOKEN_PATH, "w") as token:
            token.write(creds.to_json())
    return build("gmail", "v1", credentials=creds)

def get_latest_unread_email(service):
    results = service.users().messages().list(userId="me", q="is:unread", maxResults=1).execute()
    messages = results.get("messages", [])
    if not messages:
        return None

    msg = service.users().messages().get(userId="me", id=messages[0]["id"], format="full").execute()
    return msg

def parse_email_content(msg):
    payload = msg["payload"]
    headers = payload["headers"]
    subject = next((d["value"] for d in headers if d["name"] == "Subject"), None)
    sender = next((d["value"] for d in headers if d["name"] == "From"), None)

    if "parts" in payload:
        parts = payload["parts"]
        body_part = next((p for p in parts if p["mimeType"] == "text/plain"), None)
        if body_part:
            body_data = body_part["body"]["data"]
            body = base64.urlsafe_b64decode(body_data).decode("utf-8")
        else: # Fallback to html if no plain text
            body_part = next((p for p in parts if p["mimeType"] == "text/html"), None)
            if body_part:
                body_data = body_part["body"]["data"]
                # HTML body might be quoted-printable
                decoded_data = base64.urlsafe_b64decode(body_data)
                try:
                    body = quopri.decodestring(decoded_data).decode("utf-8")
                except Exception:
                    body = decoded_data.decode("utf-8", errors="ignore") # Failsafe
            else:
                body = ""
    else:
        body_data = payload["body"]["data"]
        body = base64.urlsafe_b64decode(body_data).decode("utf-8")

    return {"id": msg["id"], "subject": subject, "from": sender, "body": body}

def mark_as_read(service, msg_id):
    return service.users().messages().modify(userId="me", id=msg_id, body={"removeLabelIds": ["UNREAD"]}).execute()

def create_gmail_draft(service, subject: str, body: str, to: str):
    try:
        message = EmailMessage()
        message.set_content(body)
        message["To"] = to
        message["Subject"] = subject
        encoded_message = base64.urlsafe_b64encode(message.as_bytes()).decode()
        create_message = {"message": {"raw": encoded_message}}
        draft = service.users().drafts().create(userId="me", body=create_message).execute()
        print(f'Draft id: {draft["id"]}\nDraft message: {draft["message"]}')
        return draft

    except HttpError as error:
        print(f"An error occurred: {error}")
        return None
```

### 5.4. `app/sub_agents/categorization_agent/agent.py`

```python
from google.adk.agents import Agent  
from pydantic import BaseModel, Field  
from app import prompts

class CategorizationOutput(BaseModel):
    labels: list[str] = Field(..., description="A list of labels assigned to the email.")  
    requires_reply: bool = Field(..., description="Whether the email requires a direct, human-to-human reply.")

categorization_agent = Agent(
    name="categorization_agent",
    model="gemini-2.5-flash-lite",
    description="Categorizes an email and determines if it needs a reply.",
    instruction=prompts.CATEGORIZATION_INSTRUCTION,
    output_schema=CategorizationOutput,
    output_key="categorization_result", # Key to store the output in session state  
    tools=[]
)
```

### 5.5. `app/sub_agents/drafting_agent/agent.py`

```python
from google.adk.agents import Agent, LlmAgent  
from google.adk.tools.agent_tool import AgentTool  
from pydantic import BaseModel, Field  
from app import prompts  
from app.sub_agents.calendar_agent.agent import calendar_agent

# This agent's sole purpose is to call the calendar_agent tool.  
# It does NOT have an output_schema.  
_calendar_tool_caller = LlmAgent(
    name="calendar_tool_caller",
    model="gemini-2.5-flash-lite",
    description="A specialized agent that calls the calendar_agent tool to generate booking links.",
    instruction="You are a tool caller. Your only task is to use the 'calendar_agent' tool to generate booking links. You will find context in the session state under 'calendar_tool_caller_context'. After generating the link, you MUST return the link as your final response.",
    tools=[AgentTool(calendar_agent)],
    output_key="calendar_link_output", # Add output_key  
)

class DraftOutput(BaseModel):
    response_body: str = Field(..., description="The drafted body of the email response.")  
    subject: str = Field(..., description="The subject line for the email response.")  
    to_address: str = Field(..., description="The email address of the recipient.")

drafting_agent = Agent(
    name="drafting_agent",
    model="gemini-2.5-flash-lite",
    description="Drafts a reply to an email with a casual, friendly, and professional tone.",
    instruction=prompts.DRAFTING_INSTRUCTION,
    output_schema=DraftOutput,
)
```

### 5.6. `app/sub_agents/calendar_agent/agent.py`

```python
from google.adk.agents import Agent  
from app import prompts

def generate_calendar_link(attendees: list[str], duration_minutes: int) -> str:
    """Generates a dummy Google Calendar booking link and a message."""
    link = f"https://calendar.google.com/book?attendees={','.join(attendees)}&duration={duration_minutes}"
    message = "You can use the following link to book a meeting with me:"
    return f'{message}\n{link}'

calendar_agent = Agent(
    name="calendar_agent",
    model="gemini-2.5-flash-lite",
    description="Generates a Google Calendar booking link for scheduling meetings.",
    instruction=prompts.CALENDAR_INSTRUCTION,
    tools=[generate_calendar_link],
    output_key="calendar_link_output", # Add output_key  
)
```

### 5.7. `app/sub_agents/sender_agent/agent.py`

```python
from google.adk.agents import Agent  
from app import prompts  
from app.gmail_service import get_gmail_service, create_gmail_draft

def create_draft_in_gmail(subject: str, body: str, to: str) -> str:
    """Saves a draft email to the user's Gmail account. Returns the draft ID."""
    try:
        service = get_gmail_service()
        draft = create_gmail_draft(service, subject, body, to)
        if draft:
            return f"Successfully created draft with ID: {draft['id']}"
        return "Failed to create draft."
    except Exception as e:
        return f"An error occurred: {e}"

sender_agent = Agent(
    name="sender_agent",
    model="gemini-2.5-flash-lite",
    description="Saves a draft email to the user's Gmail account.",
    instruction=prompts.SENDER_INSTRUCTION,
    tools=[create_draft_in_gmail],
)
```

### 5.8. `app/agent.py` (GmailCoordinator)

```python
from typing import AsyncGenerator  
from typing_extensions import override  
from google.adk.agents import BaseAgent, LlmAgent  
from google.adk.agents.invocation_context import InvocationContext  
from google.adk.events import Event  
from google.genai.types import Content, Part

# Import specialist agents and their outputs  
from app.sub_agents.categorization_agent.agent import categorization_agent, CategorizationOutput  
from app.sub_agents.drafting_agent.agent import drafting_agent, DraftOutput, _calendar_tool_caller  
from app.sub_agents.sender_agent.agent import sender_agent

class GmailCoordinator(BaseAgent):
    """A custom agent that orchestrates the Gmail workflow with conditional logic."""
    categorization_agent: LlmAgent  
    drafting_agent: LlmAgent  
    sender_agent: LlmAgent  
    calendar_tool_caller: LlmAgent # Add the new tool caller as a sub-agent

    model_config = {"arbitrary_types_allowed": True}

    def __init__(
        self,
        name: str = "GmailCoordinator",
        categorization_agent: LlmAgent = categorization_agent,
        drafting_agent: LlmAgent = drafting_agent,
        sender_agent: LlmAgent = sender_agent,
        calendar_tool_caller: LlmAgent = _calendar_tool_caller,
    ):
        sub_agents_list = [categorization_agent, drafting_agent, sender_agent, calendar_tool_caller]
        super().__init__(
            name=name,
            categorization_agent=categorization_agent,
            drafting_agent=drafting_agent,
            sender_agent=sender_agent,
            calendar_tool_caller=calendar_tool_caller,
            sub_agents=sub_agents_list,
        )

    @override
    async def _run_async_impl(
        self, ctx: InvocationContext
    ) -> AsyncGenerator[Event, None]:
        """Implements the custom orchestration logic for the Gmail workflow."""
        print(f"[{self.name}] Starting Gmail processing workflow.")

        # 1. Categorize the email  
        print(f"[{self.name}] Running CategorizationAgent...")  
        async for event in self.categorization_agent.run_async(ctx):
            yield event

        # Debug: Print categorization result  
categorization_dict = ctx.session.state.get("categorization_result")  
categorization_result = CategorizationOutput(**categorization_dict) if categorization_dict else None  
        print(f"[{self.name}] Debug: Categorization Result: {categorization_result}")

        # 2. Check the result and decide the next step  
        if categorization_result and categorization_result.requires_reply:
            print(f"[{self.name}] Email requires a reply. Running DraftingAgent...")  
drafting_event = None  
            async for event in self.drafting_agent.run_async(ctx):
                yield event  
                if event.content and event.content.parts:
                    # Assuming the last event from drafting_agent contains the final output  
                    drafting_event = event  
          
            drafting_result = None  
            if drafting_event and drafting_event.content and drafting_event.content.parts:
                # Extract the JSON string from the event content  
                drafting_json_str = drafting_event.content.parts[0].text  
                # Convert the JSON string to a dictionary and then to DraftOutput Pydantic model  
                import json # Import json here  
                drafting_result_dict = json.loads(drafting_json_str)
                drafting_result = DraftOutput(**drafting_result_dict)

            print(f"[{self.name}] Debug: Drafting Result: {drafting_result}")

            if drafting_result:
                # Debug: Print response body before calendar check  
                print(f"[{self.name}] Debug: Response Body (pre-calendar): {drafting_result.response_body}")

                # Check if the drafted response indicates a need for a calendar link  
                if "[CALENDAR_REQUEST]" in drafting_result.response_body:
                    print(f"[{self.name}] Draft indicates need for calendar link. Running CalendarToolCaller...")  
                    # The calendar_tool_caller will put its output directly into the session state  
                    # We need to provide a message to the calendar_tool_caller to guide it  
                    async for event in self.calendar_tool_caller.run_async(ctx, new_message=Content(parts=[Part(text="Generate a meeting link for the user. The meeting is about an AI audit for a plumbing business. The recipient is the sender of the original email.")])):
                        yield event  
                  
                    calendar_link_response = ctx.session.state.get("calendar_link_output") # Use the correct output_key  
                    print(f"[{self.name}] Debug: Calendar Link Response: {calendar_link_response}")

                    if calendar_link_response:
                        # Replace the placeholder with the actual link  
                        drafting_result.response_body = drafting_result.response_body.replace("[CALENDAR_REQUEST]", calendar_link_response)
                        print(f"[{self.name}] Injected calendar link into draft.")
                    else:
                        print(f"[{self.name}] Warning: Calendar link not generated or found in session state.")

                # Debug: Print response body after calendar check  
                print(f"[{self.name}] Debug: Response Body (post-calendar): {drafting_result.response_body}")

                # Now, call the SenderAgent with the (potentially modified) drafting_result  
                # The SenderAgent's tool expects subject, body, and to_address  
                print(f"[{self.name}] Running SenderAgent...")  
sender_message_content = Content(parts=[
                    Part(text=f"Subject: {drafting_result.subject}\  "),
                    Part(text=f"To: {drafting_result.to_address}\  "),
                    Part(text=f"Body: {drafting_result.response_body}")
                ])  
                async for event in self.sender_agent.run_async(ctx, new_message=sender_message_content):
                    yield event  
              
                print(f"[{self.name}] Draft saved to Gmail.")  
yield Event(author=self.name, content=Content(parts=[Part(text="Draft has been saved to Gmail.")]))
        else:
            print(f"[{self.name}] Email does not require a reply. Workflow finished.")  
            final_message = f"Email categorized with labels: {categorization_result.labels}. No reply needed."
            yield Event(author=self.name, content=Content(parts=[Part(text=final_message)]))

# Instantiate the custom agent  
root_agent = GmailCoordinator()

# 6. Running the Agent

Once all the setup is complete and the code files are in place, you can run the agent locally.

1.  **Install Dependencies:**
    Navigate to the project root directory (`gmail_manager/`) and run:
    ```bash
    make install
    ```
    This command uses `uv` to install all the necessary Python packages defined in `pyproject.toml`.

2.  **Start the Agent:**
    From the project root directory, run:
    ```bash
    make dev
    ```
    This will start the ADK web server.

**Important Note on First Run:**
The first time you run the agent, a browser window will open prompting you to authorize access to your Gmail account. After you approve, a `token.json` file will be created in the `gmail_manager/app/` directory, and the agent will be able to create drafts automatically in the future.

```
