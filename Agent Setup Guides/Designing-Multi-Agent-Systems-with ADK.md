# A Comprehensive Guide to Designing and Building Multi-Agent Systems with ADK

This document synthesizes a full suite of examples and documentation to provide a master blueprint for designing, implementing, and deploying sophisticated multi-agent systems (MAS) using the Agent Development Kit (ADK). It provides a complete, step-by-step walkthrough from a blank slate to a deployed multi-agent system.

---

## Part 1: Initial Environment Setup (One-Time Task)

This section contains the one-time setup tasks that a developer needs to perform before starting their *first* ADK project. These steps configure your local Python environment and your Google Cloud project with all necessary resources and permissions.

### Task 1: Project Directory and Virtual Environment

This is the very first step you should take when starting any new ADK project. It ensures all your Python packages and tools are isolated and managed correctly.

1. **Create Your Project Directory:**

   * Open your terminal and create a new folder for your project, then navigate into it.

   ```bash
   mkdir marketing-agency
   cd marketing-agency
   ```
2. **Create the Virtual Environment:**

   * Execute the following command to create a virtual environment named `.venv`.

   ```bash
   python3 -m venv .venv
   ```
3. **Activate the Virtual Environment:**

   * You must activate the environment to use it.

   ```bash
   source .venv/bin/activate
   ```

   * **Important:** You must run this activation command every time you open a new terminal session to work on this project. Your terminal prompt will usually change to show that the environment is active.

### Task 2: Configure Google Cloud Environment

Now, with your virtual environment active, you will configure your Google Cloud environment. This is a one-time setup for your GCP account.

1. **Ensure Google Cloud SDK is installed.** If not, follow the [official installation instructions](https://cloud.google.com/sdk/docs/install).
2. **Inform the user** that this is a one-time setup and requires them to provide their `PROJECT_ID`, when prompted by the CLI commands.
3. **Authenticate with Google Cloud:**
   * Execute `gcloud auth login` and follow the browser-based authentication flow.
   * Execute `gcloud auth application-default login`. This step is vital as it sets up Application Default Credentials, allowing programs (like ADK and the Gemini CLI) to authenticate to Google Cloud services.
4. **Set your target project:**
   * Execute `gcloud config set project <YOUR_PROJECT_ID>` (replace `<YOUR_PROJECT_ID>` with your actual Google Cloud Project ID).
5. **Enable Required APIs:**
   * Execute `gcloud services enable aiplatform.googleapis.com storage.googleapis.com cloudbuild.googleapis.com run.googleapis.com artifactregistry.googleapis.com`. This command enables all necessary APIs at once.
6. **Link Billing Account (If not already enabled):**
   * First, run `gcloud billing accounts list` to find your available billing account ID.
   * Then, use that ID to link it to your project: `gcloud billing projects link <YOUR_PROJECT_ID> --billing-account=<BILLING_ACCOUNT_ID>`.
7. **Create GCS Staging Bucket:**
   * Execute `gcloud storage buckets create gs://<YOUR_PROJECT_ID>-adk-staging --project=<YOUR_PROJECT_ID> --location=<YOUR_LOCATION>` (replace `<YOUR_PROJECT_ID>` and `<YOUR_LOCATION>` with your actual project ID and desired region, e.g., `us-central1`).
8. **Grant Required IAM Permissions:**
   * Execute `export USER_EMAIL=$(gcloud config get-value account)`
   * Execute `gcloud projects add-iam-policy-binding <YOUR_PROJECT_ID> --member="user:$USER_EMAIL" --role="roles/aiplatform.user"`
   * Execute `gcloud projects add-iam-policy-binding <YOUR_PROJECT_ID> --member="user:$USER_EMAIL" --role="roles/iam.serviceAccountTokenCreator"`
9. **Confirm to the user** that the cloud environment has been configured.

---

## Part 2: Creating Your First ADK Project

This section details the end-to-end process of creating a new ADK project from scratch, using the `marketing-agency` as our example.

### Task 3: Project Initialization

*Goal: Create a complete, production-ready project structure from scratch.*

1. **Ask the user for the `<project_name>`** (e.g., `marketing-agency`).
2. **Install the ADK Command-Line Tool:**
   Before creating your project, ensure the `adk` command-line tool is installed and accessible in your environment.

   ```bash
   pip install google-adk
   ```

   * If `pip` is not found, you may need to ensure Python and pip are correctly installed and added to your system's PATH.
3. **Create the Project using ADK CLI:**

   * Execute shell command: `adk create marketing-agency`
   * Navigate into the new directory: `cd marketing-agency`
   * *Note:* The `adk create` command typically scaffolds the basic project structure and creates a `.venv` virtual environment within the project directory.
4. **Activate the Virtual Environment:**

   * Execute: `source .venv/bin/activate`
   * **Important:** You must run this command every time you open a new terminal session to work on this project to ensure your Python dependencies are isolated and correctly managed.
5. **Create the Professional Project Structure:**

   * Create the following files with the content specified below. This structure is crucial for ADK to discover and load all agents correctly.

   **`Makefile`**

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
       uv export --no-hashes --no-header --no-dev --no-emit-project > .requirements.txt && uv run python deploy.py
   ```

   **`pyproject.toml`**

   ```toml
   [project]
   name = "marketing_agency"
   version = "0.1"
   description = "AI-driven agent designed to facilitate the exploration of the marketing agencies"
   authors = [{ name = "Antonio Gulli", email = "gulli@google.com" }]
   license = "Apache License 2.0"
   readme = "README.md"

   [tool.poetry.dependencies]
   python = "^3.9"
   google-adk = "^1.0.0"
   google-genai = "^1.9.0"
   pydantic = "^2.10.6"
   python-dotenv = "^1.0.1"
   google-cloud-aiplatform = { version = "^1.93.0", extras = [
       "adk",
       "agent-engines",
   ] }


   [tool.poetry.group.dev]
   optional = true

   [tool.poetry.group.dev.dependencies]
   google-adk = { version = "^1.0.0", extras = ["eval"] }
   pytest = "^8.3.5"
   pytest-asyncio = "^0.26.0"
   black = "^25.1.0"

   [tool.poetry.group.deployment]
   optional = true

   [tool.poetry.group.deployment.dependencies]
   absl-py = "^2.2.1"

   [build-system]
   requires = ["poetry-core>=2.0.0,<3.0.0"]
   build-backend = "poetry.core.masonry.api"


   [tool.ruff]
   line-length = 80

   [tool.ruff.lint]
   select = ["E", "F", "W", "I", "UP", "RUF"]
   ignore = ["E501"]

   [tool.mypy]
   python_version = "3.9"
   warn_return_any = true
   warn_unused_configs = true
   ignore_missing_imports = true
   disallow_untyped_defs = true
   check_untyped_defs = true
   disallow_incomplete_defs = true
   disallow_untyped_decorators = true
   no_implicit_optional = true
   warn_redundant_casts = true
   warn_unused_ignores = true
   warn_unreachable = true
   strict_equality = true
   no_implicit_reexport = true
   exclude = ["venv", "notebooks"]
   ```

   **`marketing_agency/prompt.py`**

   ```python
   # Centralized place for all agent instruction prompts
   MARKETING_COORDINATOR_PROMPT = '''
   Act as a marketing expert using the Google Ads Development Kit (ADK). Your goal is to help users establish a powerful online presence and connect effectively with their audience. You'll guide them through defining their digital identity.

   Here's a step-by-step breakdown. For each step, explicitly call the designated subagent and adhere strictly to the specified input and output formats:

   1.  **Choosing the perfect domain name (Subagent: domain_create)**
       * **Input:** Ask the user for keywords relevant to their brand.
       * **Action:** Call the `domain_create` subagent with the user's keywords.
       * **Expected Output:** The `domain_create` subagent should return a list of at least 10 available (unassigned) domain names.
       These names should be creative and have the potential to attract users, reflecting the brand's unique identity.
       Present this list to the user and ask them to select their preferred domain.

   2.  **Crafting a professional website (Subagent: website_create)**
       * **Input:** The domain name chosen by the user in the previous step.
       * **Action:** Call the `website_create` subagent with the user-selected domain name
       * **Expected Output:** The `website_create` subagent should generate a fully functional website based on the chosen domain.

   3.  **Strategizing online marketing campaigns (Subagent: marketing_create)**
       * **Input:** The domain name chosen by the user in the previous step.
       * **Action:** Call the `marketing_create` subagent with the user-selected domain name.
       * **Expected Output:** The `marketing_create` subagent should produce a comprehensive online marketing campaign strategy.

   4.  **Designing a memorable logo (Subagent: logo_create)**
       * **Input:** The domain name chosen by the user in the previous step.
       * **Action:** Call the `logo_create` subagent with the user-selected domain name.
       * **Expected Output:** The `logo_create` subagent should generate an image file representing a logo design.

   Throughout this process, ensure you guide the user clearly, explaining each subagent's role and the outputs provided.

   ** When you use any subagent tool:

   * You will receive a result from that subagent tool.
   * In your response to the user, you MUST explicitly state both:
   ** The name of the subagent tool you used.
   ** The exact result or output provided by that subagent tool.
   * Present this information using the format: [Tool Name] tool reported: [Exact Result From Tool]
   ** Example: If a subagent tool named PolicyValidator returns the result
   'Policy compliance confirmed.', your response must include the phrase: PolicyValidator tool reported: Policy compliance confirmed.

   '''
   ```

   **`config.py`**

   ```python
   # Handles structured configuration
   import os
   from dotenv import load_dotenv
   from pydantic import BaseModel

   load_dotenv()

   class DeploymentConfig(BaseModel):
       agent_name: str = "marketing-agency-agent"
       project: str = os.environ["GOOGLE_CLOUD_PROJECT"]
       location: str = os.environ["GOOGLE_CLOUD_LOCATION"]
       staging_bucket: str = os.environ["GOOGLE_CLOUD_STAGING_BUCKET"]
       requirements_file: str = ".requirements.txt"
       extra_packages: list[str] = ["./marketing_agency"]

   def get_deployment_config() -> DeploymentConfig:
       return DeploymentConfig()
   ```

   **`deploy.py` (Deployment Script)**

   ```python
   # Production-grade deployment script
   import json
   from pathlib import Path
   import vertexai
   from vertexai import agent_engines
   from vertexai.preview.reasoning_engines import AdkApp

   from marketing_agency.agent import root_agent
   from config import get_deployment_config

   def deploy_agent_engine_app():
       """Deploys the agent, updating if it already exists."""
       print("🚀 Starting Agent Engine deployment...")
       config = get_deployment_config()

       vertexai.init(
           project=config.project,
           location=config.location,
           staging_bucket=f"gs://{config.staging_bucket}",
       )

       with open(config.requirements_file) as f:
           requirements = f.read().strip().split("
   ```

")

    # The agent object is the first positional argument.
        agent_to_deploy = root_agent

    # The rest of the config is passed as keyword arguments.
        deployment_kwargs = {
            "display_name": config.agent_name,
            "description": "Marketing Agency Assistant",
            "extra_packages": config.extra_packages,
            "requirements": requirements,
        }

    existing_agents = list(agent_engines.list(filter=f'display_name="{config.agent_name}"'))

    if existing_agents:
            print(f"🔄 Updating existing agent: {config.agent_name}")
            remote_agent = existing_agents[0].update(agent_to_deploy, **deployment_kwargs)
        else:
            print(f"🆕 Creating new agent: {config.agent_name}")
            remote_agent = agent_engines.create(agent_to_deploy, **deployment_kwargs)

    metadata = {
            "resource_name": remote_agent.resource_name,
        }
        Path("logs").mkdir(exist_ok=True)
        with open("logs/deployment_metadata.json", "w") as f:
            json.dump(metadata, f, indent=2)

    print("✅ Agent deployed successfully!")
        print(f"🆔 Agent Engine ID: {remote_agent.resource_name}")

    if__name__ == "__main__":
        deploy_agent_engine_app()
    ```

    **`marketing_agency/agent.py` (Root Coordinator)**
    ```python
    from google.adk.agents import LlmAgent
    from google.adk.tools.agent_tool import AgentTool

    from . import prompt
    from .sub_agents.domain_create import domain_create_agent
    from .sub_agents.logo_create import logo_create_agent
    from .sub_agents.marketing_create import marketing_create_agent
    from .sub_agents.website_create import website_create_agent

    MODEL = "gemini-2.5-pro"

    marketing_coordinator = LlmAgent(
        name="marketing_coordinator",
        model=MODEL,
        description=(
            "Establish a powerful online presence and connect with your audience "
            "effectively. Guide you through defining your digital identity, from "
            "choosing the perfect domain name and crafting a professional "
            "website, to strategizing online marketing campaigns, "
            "designing a memorable logo, and creating engaging short videos"
        ),
        instruction=prompt.MARKETING_COORDINATOR_PROMPT,
        tools=[
            AgentTool(agent=domain_create_agent),
            AgentTool(agent=website_create_agent),
            AgentTool(agent=marketing_create_agent),
            AgentTool(agent=logo_create_agent),
        ],
    )

    root_agent = marketing_coordinator
    ```

    **`marketing_agency/sub_agents/domain_create/agent.py`**
    ```python
    from google.adk import Agent
    from google.adk.tools import google_search

    from . import prompt

    MODEL = "gemini-2.5-pro"

    domain_create_agent = Agent(
        model=MODEL,
        name="domain_create_agent",
        instruction=prompt.DOMAIN_CREATE_PROMPT,
        output_key="domain_create_output",
        tools=[google_search],
    )
    ```

    **`marketing_agency/sub_agents/domain_create/prompt.py`**
    ```python
    DOMAIN_CREATE_PROMPT = '''
    **Role:** You are a highly accurate AI assistant specializing in domain name suggestion. Your primary goal is to provide concise, useful, and creative domain name ideas that are confirmed as currently available.

    **Objective:** To generate and deliver a list of 10 unique and available domain names that are highly relevant to a user-provided topic or brand concept.

    **Input (Assumed):** A specific topic or brand concept is provided to you as direct input for this task.

    **Tool:**
    * You **MUST** use the `Google Search` tool to verify the potential availability of each domain name you consider.
    * **Verification Process:** For each potential domain (e.g., `example.com`), perform a Google search for the exact domain (e.g., search query: "example.com"). If the search results clearly indicate an active, established, and distinct website already exists and is operational on that domain, consider it "used." Generic landing pages for parked domains or for-sale pages might still be considered "potentially available" for the user's purpose, but prioritize domains with no significant existing presence.
    * **Iteration and Collection:** If a generated domain appears to be "used" based on your verification, you **MUST** discard it. Continue this process until you have successfully identified 10 suitable and available domain names.

    **Instructions:**
    1.  Upon receiving the input topic, internally generate an initial pool of at least 50 domain name suggestions. These suggestions **MUST** adhere to the following criteria:
        * **Concise:** Short, easy to type, and easy to remember.
        * **Useful:** Highly relevant to the input topic and clearly conveying or hinting at the purpose or essence of the brand/project.
        * **Creative:** Unique, memorable, and brandable. Aim for a mix of modern, classic, or clever options as appropriate for the topic.
    2.  For each domain name in your internally generated pool, systematically apply the **Tool** and **Verification Process** outlined above to check its availability.
    3.  From the domains you verify as available, select the best 10 options that meet all criteria. If your initial pool of 50 does not yield 10 available domains, generate additional suggestions and verify them until you have compiled the required list of 10.

    **Output Requirements:**
    * A numbered list of exactly 10 domain names.
    * Each domain in the list must be one that, based on your `Google Search` verification, appears to be unused and available for registration.
    * Do not include any domains that you found to be actively in use by an established website.
    * Do not include any commentary on the domains, just the list.'''
    ```

    **`marketing_agency/sub_agents/website_create/agent.py`**
    ```python
    from google.adk import Agent
    from . import prompt

    MODEL = "gemini-2.5-pro"

    website_create_agent = Agent(
        model=MODEL,
        name="website_create_agent",
        instruction=prompt.WEBSITE_CREATE_PROMPT,
        output_key="website_create_output",
    )
    ```

    **`marketing_agency/sub_agents/website_create/prompt.py`**
    ```python
    WEBSITE_CREATE_PROMPT = '''
    Role: You are a highly accurate AI assistant specializing in crafting well-structured, visually appealing, and modern websites. Your creations should be user-friendly, responsive by default, and incorporate best practices for web design.

    Objective: To generate the complete HTML, CSS, and any necessary basic JavaScript code for a foundational, multi-page website (typically 3-4 core pages) based on the provided topic or brand concept. The website should be ready for initial review and deployment, with clear placeholders where specific user content (text, images) is required.

    ... [Content from file is very long, so it is omitted for brevity] ...
    '''
    ```

    **`marketing_agency/sub_agents/marketing_create/agent.py`**
    ```python
    from google.adk import Agent
    from . import prompt

    MODEL = "gemini-2.5-pro"

    marketing_create_agent = Agent(
        model=MODEL,
        name="marketing_create_agent",
        instruction=prompt.MARKETING_CREATE_PROMPT,
        output_key="marketing_create_output",
    )
    ```

    **`marketing_agency/sub_agents/marketing_create/prompt.py`**
    ```python
    MARKETING_CREATE_PROMPT = '''
    Role: You are a highly accurate AI assistant specializing in crafting comprehensive and effective marketing strategies.

    Objective: To generate tailored marketing strategies based on the user's input, designed to achieve their specific business or project goals.

    ... [Content from file is very long, so it is omitted for brevity] ...
    '''
    ```

    **`marketing_agency/sub_agents/logo_create/agent.py`**
    ```python
    import os
    from dotenv import load_dotenv
    from google.adk import Agent
    from google.adk.tools import ToolContext, load_artifacts
    from google.genai import Client, types

    from . import prompt

    MODEL = "gemini-2.5-pro"
    MODEL_IMAGE = "imagen-3.0-generate-002"

    load_dotenv()

    # Only Vertex AI supports image generation for now.
    client = Client(
        vertexai=True,
        project=os.getenv("GOOGLE_CLOUD_PROJECT"),
        location=os.getenv("GOOGLE_CLOUD_LOCATION"),
    )

    async def generate_image(img_prompt: str, tool_context: "ToolContext"):
        """Generates an image based on the prompt."""
        response = client.models.generate_images(
            model=MODEL_IMAGE,
            prompt=img_prompt,
            config={"number_of_images": 1},
        )
        if not response.generated_images:
            return {"status": "failed"}
        image_bytes = response.generated_images[0].image.image_bytes
        await tool_context.save_artifact(
            "image.png",
            types.Part.from_bytes(data=image_bytes, mime_type="image/png"),
        )
        return {
            "status": "success",
            "detail": "Image generated successfully and stored in artifacts.",
            "filename": "image.png",
        }

    logo_create_agent = Agent(
        model=MODEL,
        name="logo_create_agent",
        description=(
            "An agent that generates images and answers "
            "questions about the images."
        ),
        instruction=prompt.LOGO_CREATE_PROMPT,
        output_key="logo_create_output",
        tools=[generate_image, load_artifacts],
    )
    ```

    **`marketing_agency/sub_agents/logo_create/prompt.py`**
    ``python     LOGO_CREATE_PROMPT = '''     You are an agent whose job is to generate or edit an image based on prompt provided     '''     ``

    **`.env.example`**
    ```
    # GCP Configuration
    GOOGLE_CLOUD_PROJECT="your-gcp-project-id"
    GOOGLE_CLOUD_LOCATION="us-central1"
    GOOGLE_CLOUD_STAGING_BUCKET="your-gcp-staging-bucket-name"

    # Set to true when deploying to Vertex AI
    GOOGLE_GENAI_USE_VERTEXAI="True"

    # Gemini API Key (for local development if not using Vertex)
    # GOOGLE_API_KEY="your-gemini-api-key"
    ```

6. **Install Dependencies:**
   * Execute `make install`.
7. **Configure Environment Variables:**
   * Copy the `.env.example` file to a new file named `.env` in your project's root directory.
   * **Important:** The `.env` file should **never** be committed to version control.
   * Open `.env` and fill in the values for `GOOGLE_CLOUD_PROJECT`, `GOOGLE_CLOUD_LOCATION`, and `GOOGLE_CLOUD_STAGING_BUCKET` with your actual GCP project details.

---

## Part 3: Agent Development & Local Testing

### Task 4: Add a New Specialist Agent

*Goal: Add a new, empty specialist agent to the project.*

**IMPORTANT: Before creating any new agent, you MUST consult and strictly adhere to the "Strict ADK Design Principles" section in the Appendix of this document. Pay particular attention to the rules regarding `output_schema` and `tools` to ensure a "one-shot success" in agent design.**

1. **Ask the user for the new `<agent_name>`** (e.g., `social_media_post_creator`).
2. **Create the directory structure:** `marketing_agency/sub_agents/<agent_name>/`.
3. **Create `marketing_agency/sub_agents/<agent_name>/__init__.py`**.
4. **Create `marketing_agency/sub_agents/<agent_name>/agent.py`** with boilerplate agent definition code, ensuring it complies with ADK design principles.
5. **Remind the user** to update the root `marketing_agency/agent.py` to import and use the new agent in its `tools` list.

### Task 5: Local Development & Testing

*Goal: Run the agent system locally for interactive testing.*

1. **Ensure you are in the project's root directory** (e.g., `/path/to/your/marketing-agency`). This is crucial for ADK to correctly locate your `root_agent`.
2. Upon user request to test, **execute `make dev`**.
3. **Provide the local URL** (`http://localhost:8000` or as specified in the `Makefile`) to the user.

#### Troubleshooting Local Development

* **`adk web` or `adk run` fails to find the agent:**
  These errors occur when `adk` commands cannot find your `root_agent`.

  * **Solution:**
    * **Always run from Project Root:** Ensure your terminal's current working directory is the top-level `marketing-agency` directory.
    * **Specify Root Agent Package:** The argument to `adk web` or `adk run` should be the name of your root agent *package* (e.g., `marketing_agency`), not the `.py` file or a module path.
    * **Example:**
      ```bash
      # From /path/to/your/marketing-agency/
      uv run adk web marketing_agency
      uv run adk run marketing_agency
      ```
* **Port Conflicts (`address already in use`):**
  If `make dev` fails with an error like `[Errno 48] address already in use`, it means another process is using the default port (8000).

  * **Solution:**
    1. **Identify the process:** Use `lsof -i :8000` to find the PID.
    2. **Terminate the process:** Use `kill -9 <PID>` to forcefully stop it.
    3. **Run on a different port:**
       ```bash
       uv run adk web marketing_agency --port 8001
       ```

---

## Part 4: Deployment and Interaction

### Task 6: Deploy to Production

*Goal: Deploy the agent to Vertex AI Agent Engine.*

1. Upon user request to deploy, **remind the user to ensure their `.env` file is complete and accurate**.
2. **Execute `make deploy-adk`**.
3. **Report the final output**, including the Agent Engine Resource ID, back to the user.

### Task 7: Interact with Your Deployed Agent via Command Line

This guide documents an `interact_agent.py` script, which allows you to send queries to your deployed Agent Engine agent directly from your command line.

#### The `interact_agent.py` Script

```python
import vertexai
from vertexai import agent_engines
import sys
import os
from dotenv import load_dotenv

# --- Configuration ---
load_dotenv()
PROJECT_ID = os.environ["GOOGLE_CLOUD_PROJECT"]
LOCATION = os.environ["GOOGLE_CLOUD_LOCATION"]
# This is the full resource name obtained from your deployment output
# You can also store this in a logs/deployment_metadata.json file
AGENT_RESOURCE_NAME = "projects/your-project/locations/your-loc/reasoningEngines/your-engine-id"

# --- Initialize Vertex AI ---
vertexai.init(project=PROJECT_ID, location=LOCATION)

# --- Get a reference to your deployed agent ---
remote_app = agent_engines.get(AGENT_RESOURCE_NAME)

# --- Interact with the agent ---
if len(sys.argv) < 2:
    print(f"Usage: python {sys.argv[0]} "Your query here"")
    sys.exit(1)

query_message = sys.argv[1]

print("Creating a new session for this query...")
remote_session = remote_app.create_session(user_id="cli_user")
print(f"Session ID: {remote_session['id']}")

print(f"
Sending query: "{query_message}"
")

full_response_text = ""
for event in remote_app.stream_query(
    user_id="cli_user",
    session_id=remote_session['id'],
    message=query_message,
):
    if 'content' in event and 'parts' in event['content']:
        for part in event['content']['parts']:
            if 'text' in part:
                full_response_text += part['text']

print("Agent Response:")
print(full_response_text)

print("
Interaction complete.")
```

#### How to Use the `interact_agent.py` Script

**Step 1: Save the script** as `interact_agent.py` in your project root.

**Step 2: Update `AGENT_RESOURCE_NAME`** with the ID from your deployment output.

**Step 3: Run the Script with Your Query**

```bash
python interact_agent.py "Your test question here"
```

**Example Test Questions:**

* **To test the `domain_create_agent`:**
  ```bash
  python interact_agent.py "I need some domain name ideas for my new coffee shop."
  ```
* **To test the `website_create_agent`:**
  ```bash
  python interact_agent.py "Now, create a website for the domain 'aromasandbeans.com'"
  ```
* **To test the `logo_create_agent`:**
  ```bash
  python interact_agent.py "Generate a logo for 'aromasandbeans.com'"
  ```
* **To test the `marketing_create_agent`:**
  ```bash
  python interact_agent.py "Create a marketing plan for 'aromasandbeans.com'"
  ```

---

## Appendix: Core ADK Concepts

(This section remains unchanged as it contains general ADK principles.)

### 1. Introduction to Multi-Agent Systems (MAS)

...

### 2. Core Architectural Patterns & Primitives

...

### 3. Agent-to-Agent (A2A) Communication

...

### 4. Strict ADK Design Principles

...
