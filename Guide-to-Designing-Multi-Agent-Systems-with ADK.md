# **A Comprehensive Guide to Designing Multi-Agent Systems with ADK**

This document synthesizes a full suite of examples and documentation to provide a master blueprint for designing, implementing, and deploying sophisticated multi-agent systems (MAS) using the Agent Development Kit (ADK).

## **1\. The Golden Path: Creating Your Multi-Agent Project**

This section provides the quickest path from idea to a deployed multi-agent system.

1. **`gcloud` Setup**: Run the commands in the **CLI-based Environment Setup** section below to configure your GCP project, APIs, and permissions.
2. **`make install`**: Run this once to install all project dependencies from `pyproject.toml`.
3. **Define Agents**: Create your specialist sub-agents and your root coordinator agent, following the project structure and patterns outlined in this guide.
4. **`make dev`**: Run the local web UI to test and debug your agent system interactively.
5. **`make deploy-adk`**: Deploy your agent to the production environment on Vertex AI Agent Engine.

**Note for Gemini CLI Users:** This guide is the conceptual blueprint. For a granular, step-by-step procedure designed for the Gemini CLI tool to follow, refer to the companion document: `gemini_cli_playbook.md`.

## **2\. Introduction to Multi-Agent Systems (MAS)**

A Multi-Agent System is an advanced architecture where multiple specialized agents collaborate to handle complex tasks that would be difficult for a single, monolithic agent. Each agent focuses on a specific domain, and they work together through delegation, tool usage, and shared state to solve problems.

**Key Advantages:**

* **Modularity:** Each agent is a self-contained component, making the system easier to understand, develop, and maintain.
* **Specialization:** Agents can be experts in a narrow domain (e.g., booking, technical support), leading to higher quality performance.
* **Reusability:** Specialized agents can be reused across different workflows or even different applications.
* **Scalability:** Work can be distributed across different agents, which can even be deployed as separate microservices.

## **3\. Core Architectural Patterns & Primitives**

ADK provides a clear set of primitives (building blocks) and patterns (blueprints) for constructing a MAS.

### **3.1 Foundational Primitives**

* **Agent Hierarchy:** The system is structured as a tree of agents. A parent agent lists other agents in its `sub_agents` parameter during initialization, establishing a formal hierarchy.
* **Workflow Agents:** For deterministic control flow, ADK provides:
  * `SequentialAgent`: Executes sub-agents in a fixed order.
  * `ParallelAgent`: Executes sub-agents concurrently to reduce latency.
  * `LoopAgent`: Executes sub-agents iteratively, ideal for refinement or polling until a condition is met.

### **3.2 Agent Communication & Interaction Models**

There are three primary ways for agents to interact:

1. **LLM-Driven Delegation (`sub_agents` model):** A parent agent's LLM decides to transfer control to a specialist sub-agent. The sub-agent then takes over the conversation. This is best for completely handing off a task.
2. **Explicit Invocation (`AgentTool` model):** A parent agent uses a specialist sub-agent as a callable `Tool`. The parent remains in control, receives a result from the sub-agent, and decides the next step. This is best when the parent needs a specific piece of information to continue its own work.
3. **Shared Session State (`ctx.session.state`):** Agents passively share information by writing to and reading from a shared dictionary. This is the primary method for passing data through a workflow.

### **3.3 Common Architectural Patterns**

By combining the primitives, you can implement these standard patterns:

* **Coordinator/Dispatcher:** A central root agent routes incoming requests to the appropriate specialist sub-agent. This is the most common top-level pattern.
* **Hierarchical Task Decomposition:** A high-level agent breaks a complex problem into smaller sub-tasks and delegates them to lower-level agents, often using the `AgentTool` model.
* **Sequential Pipeline / Generator-Critic:** A `SequentialAgent` executes a series of agents in order, such as a `Generator` agent creating content and a `Critic` agent reviewing it.
* **Iterative Refinement:** A `LoopAgent` is used to progressively improve a piece of work until it meets a quality standard.
* **Human-in-the-Loop:** A custom tool can be built to pause the workflow and request input or approval from a human user.

## **4\. Practical Implementation Guide**

### **4.1. Project Setup & Structure**

A strict project structure is required for ADK to discover and load all agents correctly.

```
/my_agent_project
└── /my_root_agent_name                # Root agent package
   ├── __init__.py                    # Must import agent.py
   ├── agent.py                       # Must define the `root_agent` variable
   ├── .env                           # Environment variables
   └── /sub_agents/                   # Directory for all sub-agents
       ├── __init__.py
       ├── /specialist_agent_one/
       │   ├── __init__.py
       │   └── agent.py               # Defines the agent variable
       └── /specialist_agent_two/
           ├── __init__.py
           └── agent.py

```

### **4.2. Automating Workflows with `pyproject.toml` and `Makefile`**

For a professional, hassle-free development experience, using `pyproject.toml` and a `Makefile` is highly recommended.

#### **`pyproject.toml`: The Unified Project Definition**

This file is the standard for modern Python projects. It acts as a single source of truth for:

* **Project Dependencies:** Replaces `requirements.txt` for cleaner dependency management.
* **Tool Configuration:** Centralizes settings for linters (`Ruff`), type checkers (`Mypy`), and testers (`Pytest`).

**Benefit:** Ensures every developer has a consistent, reproducible environment, which drastically reduces setup time and bugs.

```
# Example from pyproject.toml

[project]
name = "adk-fullstack"
# Core dependencies for the agent
dependencies = [
   "google-adk==1.7.0",
   "python-dotenv",
]

# Optional dependencies for development (e.g., linting)
[project.optional-dependencies]
lint = [
   "ruff>=0.4.6",
   "mypy~=1.15.0",
]

# Centralized configuration for the linter
[tool.ruff.lint]
select = ["E", "F", "W", "I", "UP", "RUF"]
ignore = ["E501"]

```

#### **`Makefile`: The Developer's Shortcut**

This file defines short, memorable commands to automate complex developer workflows.

**Benefit:** Simplifies common tasks, ensures consistency across the team, and makes onboarding new developers much faster.

```
# Example from Makefile

# Install all python and npm dependencies with one command
install:
   uv sync && npm --prefix nextjs install

# Run backend and frontend servers concurrently for development
dev:
   make dev-backend & make dev-frontend

# Run all code quality checks with one command
lint:
   uv run ruff check . --diff
   uv run mypy .

# Automate the deployment process
deploy-adk:
   uv export --no-hashes --no-header --no-dev --no-emit-project --no-annotate > .requirements.txt && uv run python -m app.agent_engine_app

```

### **4.3. Defining Agents**

#### **The Root Agent (Coordinator)**

The root agent acts as the entry point and dispatcher. Its `instruction` prompt is critical for routing.

**The Hybrid Interaction Model** A powerful and common pattern is to use **both** delegation and tool-based invocation in the same root agent.

**Example (`MANAGER_AGENT_EXAMPLE.md`):** This manager agent delegates tasks to `stock_analyst` and `funny_nerd`, but calls `news_analyst` as a tool to get information back before formulating its own response.

```
from google.adk.agents import Agent
from google.adk.tools.agent_tool import AgentTool

# Import all specialists
from .sub_agents.funny_nerd.agent import funny_nerd
from .sub_agents.news_analyst.agent import news_analyst
from .sub_agents.stock_analyst.agent import stock_analyst

root_agent = Agent(
   name="manager",
   model="gemini-2.0-flash",
   instruction="""
   You are a manager... Always delegate the task to the appropriate agent.
   You are responsible for delegating tasks to: stock_analyst, funny_nerd
   You also have access to the following tools: news_analyst, get_current_time
   """,
   # Agents for DELEGATION
   sub_agents=[stock_analyst, funny_nerd],
   # Agents for INFORMATION RETRIEVAL
   tools=[
       AgentTool(news_analyst),
       get_current_time,
   ],
)

```

#### **Specialized Sub-Agents**

Sub-agents should have a narrow focus, a clear `description`, and use `output_schema` with Pydantic models for reliable, structured output.

**Note on Model Availability:** The specific model versions (e.g., `gemini-2.5-pro`, `gemini-2.0-flash`) used in the agent examples may not be available in all Google Cloud regions or for all projects. Always verify model availability in your target region and project, and adjust the `model` parameter in your agent definitions accordingly.

### **4.4. Critical Limitations and Best Practices for Tools and `output_schema`**

For detailed rules and best practices regarding tool usage and `output_schema`, refer to [7.1. The `output_schema` and `tools` Constraint: A Fundamental Rule](#71-the-output_schema-and-tools-constraint-a-fundamental-rule).

#### **4.4.1. Separation of Concerns: Tools and Delegation**

A key principle in ADK is the clear separation between an agent's ability to *delegate* tasks to sub-agents and its ability to *use tools*. This distinction is particularly important when dealing with built-in tools (like `google_search`) or tools that require specific environmental contexts.

**Important:** For detailed rules regarding `output_schema` and tool usage, refer to [4.4.2. Leveraging `output_schema` for Structured Output](#442-leveraging-output_schema-for-structured-output-a-critical-constraint).

**Example of Separation:**

Consider a `knowledge_agent` that uses `google_search`. In app/agent.py (Root Coordinator) from google.adk.agents import Agent from google.adk.tools.agent\_tool import AgentTool from google.adk.tools import google\_search \# Built-in tool

Define an agent that needs a built-in tool This agent is designed to be called as a tool, not delegated to. knowledge\_agent \= Agent( name="knowledge\_agent", model="gemini-2.0-flash", description="Answers technical questions by searching the web.", tools=\[google\_search\] )

The root\_agent uses the hybrid model root\_agent \= Agent( name="TradieMateCoordinator", model="gemini-2.5-pro", instruction=prompts.COORDINATOR\_INSTRUCTION, Use AgentTool for the agent with a built-in tool tools=\[ AgentTool(knowledge\_agent) \# knowledge\_agent is called as a tool \], Use sub\_agents for direct delegation sub\_agents=\[ quoting\_agent \# quoting\_agent is delegated to \] )

In this example, `knowledge_agent` is designed to be a tool. The `root_agent` calls `knowledge_agent` as an `AgentTool` when it needs to perform a web search. Conversely, `quoting_agent` is designed for delegation, meaning the `root_agent` can hand off the entire quoting task to it. This clear distinction prevents issues with tool availability and ensures predictable agent behavior.

#### **4.4.2. Leveraging `output_schema` for Structured Output: A Critical Constraint**

For specialist sub-agents, defining a clear `output_schema` using Pydantic models is a best practice. This ensures that the agent's output is consistently structured, making it easier for other agents or downstream systems to consume and process the information.

**CRITICAL CONSTRAINT:** An `LlmAgent` (or `Agent` alias) that defines an `output_schema` (for structured output) **MUST NOT** have any `tools` defined in its `tools` parameter. Using `output_schema` enables controlled generation within the LLM but **disables the agent's ability to use tools or transfer control to other agents**.

**Implication for Gemini CLI:** If an `LlmAgent` needs to produce structured output AND its logic requires a tool call, the tool call **MUST** be orchestrated by a higher-level `CustomAgent`. The `LlmAgent` itself should only output a specific, easily parsable flag or placeholder (e.g., `"[CALENDAR_REQUEST]"`) in its structured output to signal the need for a tool call.

Example of a specialist agent with output\_schema from google.adk.agents import Agent from pydantic import BaseModel, Field

class QuoteOutput(BaseModel): material\_cost: float \= Field(..., description="The calculated cost of materials.") labor\_cost: float \= Field(..., description="The estimated labor cost.") total\_cost: float \= Field(..., description="The total estimated cost for the job.") currency: str \= Field("USD", description="The currency of the quote.") notes: str \= Field(None, description="Any additional notes or disclaimers.")

quoting\_agent \= Agent( name="quoting\_agent", model="gemini-2.0-flash", description="Creates quotes for jobs.", instruction=prompts.QUOTING\_INSTRUCTION, tools=\[get\_material\_cost\], output\_schema=QuoteOutput \# Ensure structured output )

By explicitly defining the `output_schema`, you guide the LLM to produce output that conforms to a predictable structure, significantly reducing parsing errors and improving the reliability of your multi-agent system.

### **4.5. Running ADK Commands: Context and Arguments**

When executing ADK commands, especially those involving file paths or project structures, it's important to understand the context in which these commands run and how arguments are interpreted.

**Working Directory:** Most ADK commands assume they are being run from the root of your ADK project. This means that relative paths provided as arguments will be resolved against this root directory. If you run an ADK command from a subdirectory, you might need to adjust your paths accordingly or specify the project root explicitly if the command supports it.

**Argument Interpretation:** Pay close attention to how ADK commands interpret their arguments:

* **Agent Paths:** When specifying an agent for commands like `adk run <agent_path>`, the `agent_path` typically refers to the Python module path (e.g., `app.agent` for `app/agent.py`) relative to your project's root, not a file system path.
* **Directory Arguments:** For commands like `adk web [agents_dir]`, `agents_dir` usually expects a path to a directory containing your agent modules. This path can be relative to your current working directory or an absolute path.
* **Glob Patterns:** Some ADK tools or underlying utilities might support glob patterns (e.g., `**/*.py`) for specifying multiple files or directories. Always consult the specific command's documentation or help output (`adk <command> --help`) for details on argument interpretation.

Understanding these nuances will help you avoid common errors related to file not found, module not found, or incorrect command execution.

## **5\. Agent-to-Agent (A2A) Communication**

For agents that need to communicate across network boundaries, the ADK uses the A2A protocol.

### **5.1. When to Use A2A vs. Local Sub-Agents**

* **Use Local Sub-Agents for:** Internal code organization, performance-critical operations, and workflows requiring shared memory.
* **Use A2A for:** Integrating with external/third-party agents, building a microservices architecture, or connecting agents written in different languages.

### **5.2. The A2A Workflow**

1. **Exposing an Agent:** Make an agent accessible over the network. The simplest method is to use the `adk` CLI:

```
adk api_server --a2a --port 8001 /path/to/your/agents_dir

```

2. **Consuming a Remote Agent:** Use the `RemoteA2aAgent` class in your consuming agent's code, pointing it to the exposed agent's `agent.json` card URL.

```
from google.adk.a2a import RemoteA2aAgent

remote_prime_agent = RemoteA2aAgent(
   name="prime_agent",
   description="Agent that handles checking if numbers are prime.",
   agent_card="http://localhost:8001/a2a/check_prime_agent/.well-known/agent.json"
)

```

## **6\. The Full Lifecycle: From Local Testing to Production Deployment**

## **7. Strict ADK Design Principles for Gemini CLI**

This section outlines critical, non-negotiable rules and best practices specifically for the Gemini CLI tool when designing and implementing ADK agents. Adhering to these principles is paramount to ensure a "one-shot success" in agent building, minimizing debugging cycles and maximizing efficiency.

### **7.1. The `output_schema` and `tools` Constraint: A Fundamental Rule**

**Rule:** An `LlmAgent` (or `Agent` alias) that defines an `output_schema` (for structured output) **MUST NOT** have any `tools` defined in its `tools` parameter. This is a strict ADK framework limitation.

**Implication for Gemini CLI:**

* **DO NOT** create an `LlmAgent` with both `output_schema` and `tools`.
* If an `LlmAgent` needs to produce structured output AND its logic requires a tool call, the tool call **MUST** be orchestrated by a higher-level `CustomAgent`. The `LlmAgent` itself should only output a specific, easily parsable flag or placeholder in its structured output to signal the need for a tool call.

### **7.2. Custom Agents: The Orchestration Powerhouse**

**Rule:** For any complex, conditional, or multi-step workflow that involves inspecting the output of one agent to decide the next action (especially when `LlmAgent`s with `output_schema` are involved), a `CustomAgent` is the required pattern.

**Implication for Gemini CLI:**

* **PRIORITIZE** `CustomAgent` for root coordinators or any agent responsible for conditional branching, dynamic tool invocation based on sub-agent output, or complex state manipulation.
* **DO NOT** attempt to force complex conditional logic into an `LlmAgent`'s `instruction` if it involves dynamic tool calls or branching based on structured outputs from other `LlmAgent`s.

### **7.3. Meticulous State and Event Handling**

**Rule:** Data transfer between agents, especially from `LlmAgent`s with `output_schema`, and event propagation must be handled precisely.

**Implication for Gemini CLI:**

* **ALWAYS** assume that the output of an `LlmAgent` with an `output_schema` will be a JSON string within the `Event` object's content (e.g., `event.content.parts[0].text`).
* **ALWAYS** parse this JSON string into the corresponding Pydantic model (e.g., `MyOutputModel(**json.loads(json_string))`) for type-safe access.
* **LEVERAGE `output_key`:** For any `LlmAgent` (with or without `output_schema`), use the `output_key` parameter to automatically save the agent's final text response to the session's state dictionary. This is crucial for subsequent agents or custom logic to access the result.
* **ENSURE** that `CustomAgent`s correctly yield all events from their sub-agents (`async for event in sub_agent.run_async(ctx): yield event`) to ensure proper propagation and debugging visibility.
* **BE PRECISE** when constructing `Event` objects for custom observations or final responses. Refer to the ADK API documentation for the exact constructor arguments (e.g., `Event(author=..., content=...)`).

### **7.4. Model Naming and Environment Verification**

**Rule:** Model identifiers are exact and environment-specific.

**Implication for Gemini CLI:**

* **ALWAYS** verify the exact model identifier string (e.g., `gemini-2.5-flash-lite`) directly from the Vertex AI console for the target project and region.
* **ANTICIPATE** potential environment or caching issues. If a model `404 NOT_FOUND` error persists despite correct code, advise the user to:
  * Clear Python virtual environment cache (`rm -rf .venv` and `make install`).
  * Verify model availability in the specific GCP project/region.
  * Refresh `gcloud` credentials.

### **7.5. General Agent Building Workflow for Gemini CLI**

To achieve "one-shot success":

1. **Design First:** Before writing code, clearly define each agent's role, its inputs, its expected outputs (including `output_schema` if applicable), and its tool usage.
2. **Identify Orchestrators:** Determine which agents will be `CustomAgent`s responsible for conditional logic and data flow.
3. **Separate Concerns:** Ensure `LlmAgent`s either produce structured output OR use tools, but not both. If both are needed, use a `CustomAgent` to orchestrate.
4. **Test Incrementally:** Build and test agents one by one, starting from the lowest-level specialists.
5. **Log Verbose:** Use extensive `print` statements (or proper logging) within `CustomAgent`s to trace execution flow, inspect state, and verify data transformations.
6. **Consult Docs:** Refer to the official ADK documentation for precise API signatures and best practices.

### **7.6. Effective `LlmAgent` Instruction Crafting**

**Rule:** `LlmAgent` instructions are the primary mechanism for guiding LLM behavior. Well-crafted instructions are crucial for predictable and accurate agent responses.

**Implication for Gemini CLI:**

* **BE CLEAR AND SPECIFIC:** Avoid ambiguity. Clearly state the desired actions, goals, and constraints.
* **USE MARKDOWN:** Employ Markdown (headings, lists, bolding) within instructions to improve readability and structure for complex prompts.
* **PROVIDE FEW-SHOT EXAMPLES:** For complex tasks or specific output formats, include concrete examples directly in the instruction to guide the LLM's generation.
* **GUIDE TOOL USE:** Don't just list tools; explain *when* and *why* the agent should use them within the instruction, supplementing any tool descriptions.
* **LEVERAGE DYNAMIC VALUES:** Use the `{var}` syntax within instructions to inject dynamic values from the session state (e.g., `{ctx.session.state["user_name"]}`).

### **7.7. `LlmAgent` Advanced Configuration Best Practices**

**Rule:** Advanced `LlmAgent` parameters offer fine-grained control over LLM behavior and context management.

**Implication for Gemini CLI:**

* **`generate_content_config`:** Use this parameter to control LLM generation aspects like `temperature` (for randomness/determinism), `max_output_tokens` (for response length), `top_p`, and `top_k`. Adjust `temperature` to lower values (e.g., 0.0-0.2) for more deterministic and factual responses.
* **`include_contents`:** Carefully consider this parameter:
  * Use `'default'` (the default) when the agent needs conversation history for context.
  * Use `'none'` for stateless tasks or when you want the agent to operate solely on the current turn's input, ignoring prior conversation history. This can reduce token usage and prevent context drift.

### **6.1. Local Development & Testing**

* **`adk create <app_name>`**: Creates a new project with a boilerplate agent template.
* **`adk web [agents_dir]`**: Starts a local web UI for interactive development and debugging.
* **`adk run <agent_path>`**: Runs a single agent in an interactive CLI.
* **`adk eval <agent_module> [eval_set_paths...]`**: Evaluates an agent against predefined datasets.

### **6.2. Production Deployment: From Manual CLI to Automated Scripting**

While using `adk deploy` is great for getting started, production-grade systems benefit from a programmatic and automated deployment script. This provides reliability, reproducibility, and allows for advanced customization.

#### **6.2.1. Environment Setup via Google Cloud CLI**

Before your first deployment, run these commands in your terminal to configure the necessary cloud infrastructure. This is a one-time setup.

**Step 1: Authenticate and Set Project**

```
# Log in to Google Cloud
gcloud auth login

# Set up Application Default Credentials for libraries
gcloud auth application-default login

# Set your target project
gcloud config set project YOUR_PROJECT_ID

```

**Step 2: Enable Required APIs**

```
# This command enables all 5 necessary APIs at once
gcloud services enable aiplatform.googleapis.com storage.googleapis.com cloudbuild.googleapis.com run.googleapis.com artifactregistry.googleapis.com

```

**Step 3: Link Billing Account (If not already enabled)**

```
# Note: Billing account IDs are sensitive and should not be hardcoded in scripts.

# First, run this command to find your available billing account ID:
gcloud billing accounts list

# The output will look something like this:
# ACCOUNT_ID            NAME                OPEN
# 012345-67890A-BCDEF1  My Billing Account  True
#
# Copy the full ID from the ACCOUNT_ID column.

# Then, use that ID to link it to your project in the next command:
gcloud billing projects link YOUR_PROJECT_ID --billing-account=012345-67890A-BCDEF1

```

**Step 4: Create GCS Staging Bucket**

```
# Use your project ID to create a globally unique bucket name
# Replace YOUR_PROJECT_ID and YOUR_LOCATION (e.g., us-central1)
gcloud storage buckets create gs://YOUR_PROJECT_ID-adk-staging --project=YOUR_PROJECT_ID --location=YOUR_LOCATION

```

**Step 5: Grant Required IAM Permissions**

```
# Get your email address
export USER_EMAIL=$(gcloud config get-value account)

# Grant the necessary roles to your user account
gcloud projects add-iam-policy-binding YOUR_PROJECT_ID --member="user:$USER_EMAIL" --role="roles/aiplatform.user"
gcloud projects add-iam-policy-binding YOUR_PROJECT_ID --member="user:$USER_EMAIL" --role="roles/iam.serviceAccountTokenCreator"

```

**Step 6: Create `.env` File** With the infrastructure now created, copy the `.env.example` file in your project to `.env` and fill in the values for `GOOGLE_CLOUD_PROJECT`, `GOOGLE_CLOUD_LOCATION`, and `GOOGLE_CLOUD_STAGING_BUCKET`.

#### **6.2.2. The Professional Path: Automated Deployment Script**

An advanced deployment script (`agent_engine_app.py`) provides more control and automation. Key principles from this approach include:

* **Extending `AdkApp`**: Create a custom class that inherits from `AdkApp` to add production-grade features like structured cloud logging, performance tracing, and custom API operations (e.g., for user feedback).
* **Idempotent Logic**: The script should first check if an agent with the same name already exists. If so, it should **update** the agent; otherwise, it should **create** a new one. This makes the script safe to run repeatedly.

```
# Snippet of update-or-create logic
existing_agents = list(
   agent_engines.list(filter=f'display_name={deployment_config.agent_name}')
)

if existing_agents:
   print(f"🔄 Updating existing agent: {deployment_config.agent_name}")
   remote_agent = existing_agents[0].update(**agent_config)
else:
   print(f"🆕 Creating new agent: {deployment_config.agent_name}")
   remote_agent = agent_engines.create(**agent_config)

```

* **Persistent Artifacts**: Programmatically configure a `GcsArtifactService` to ensure any files generated by or uploaded to your agent are stored in a persistent Cloud Storage bucket.
* **Metadata Logging**: After a successful deployment, save the output `remote_agent.resource_name` to a local file. This ID is essential for integrating the agent into CI/CD pipelines and other applications.

### **6.3. Common Troubleshooting**

* **Development-Time Issues:**
  * *Malformed JSON / Pydantic Errors*: The LLM failed to generate valid output. Try simplifying the `output_schema`, improving the prompt, or telling the agent to "try again".
  * *Wrong Tool Called*: The agent chose the wrong tool. Improve the tool `description` and the agent's `instruction` to be more specific.
  * *Agent Stops*: If an agent stops mid-flow, you can often nudge it by asking "what's next?".
* **Deployment-Time Issues:**
  * *Permission Errors*: Double-check that all 5 required APIs are enabled and your account has the correct IAM roles.
  * *Staging Bucket Errors*: Ensure the bucket exists and its region matches your deployment region.

## **Appendix: Complete Project Example**

This section provides a complete, file-by-file blueprint for a production-ready multi-agent system. It demonstrates how all the concepts in this guide fit together.

### **1\. Project Structure**

```
/tradie_mate/
├── Makefile
├── pyproject.toml
└── /app/
   ├── __init__.py
   ├── agent.py                 # Root Coordinator Agent
   ├── agent_engine_app.py      # Professional Deployment Script
   ├── config.py                # Structured Configuration
   ├── prompts.py               # Centralized Prompts
   ├── .env.example             # Environment Variable Template
   └── /sub_agents/
       ├── __init__.py
       └── /quoting_agent/
           ├── __init__.py
           └── agent.py         # Specialist Agent Example

```

### **2\. Core Files**

**`Makefile`**

```
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

**`pyproject.toml`**

```
[project]
name = "tradie-mate"
version = "0.1.0"
dependencies = [
   "google-adk==1.7.0",
   "python-dotenv",
   "google-cloud-logging",
   "opentelemetry-sdk",
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

**`.env.example`**

**Note:** This file acts as a template. Copy it to a `.env` file for local development and add your secret values. The `.env` file should **never** be committed to version control.

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

### **3\. Application Logic**

**`app/prompts.py`**

```
# Centralized place for all agent instruction prompts

COORDINATOR_INSTRUCTION = """
   You are the coordinator for TradieMate, an AI assistant for tradespeople.
   - For any requests about quotes, pricing, or estimates, delegate to the `quoting_agent`.
   - For any technical questions about building codes or materials, use the `knowledge_agent` tool to get information, then provide the final answer.
"""

QUOTING_INSTRUCTION = "You are a quoting specialist. Use the tools provided to calculate the cost and provide a quote."


```

**`app/config.py`**

```
# Handles structured configuration
import os
from dotenv import load_dotenv
from pydantic import BaseModel

load_dotenv()

class DeploymentConfig(BaseModel):
   agent_name: str = "tradie-mate-agent"
   project: str = os.environ["GOOGLE_CLOUD_PROJECT"]
   location: str = os.environ["GOOGLE_CLOUD_LOCATION"]
   staging_bucket: str = os.environ["GOOGLE_CLOUD_STAGING_BUCKET"]
   requirements_file: str = ".requirements.txt"
   extra_packages: list[str] = ["./app"]

def get_deployment_config() -> DeploymentConfig:
   return DeploymentConfig()

```

**`app/agent.py` (Root Coordinator)**

```
# The Root Coordinator Agent
from google.adk.agents import Agent
from google.adk.tools.agent_tool import AgentTool
from google.adk.tools import google_search # Built-in tool

# Import prompts and specialist agents
from app import prompts
from app.sub_agents.quoting_agent.agent import quoting_agent

# Define an agent that needs a built-in tool
knowledge_agent = Agent(
   name="knowledge_agent",
   model="gemini-2.0-flash",
   description="Answers technical questions by searching the web.",
   tools=[google_search]
)

# The root_agent uses the hybrid model
root_agent = Agent(
   name="TradieMateCoordinator",
   model="gemini-2.5-pro",
   instruction=prompts.COORDINATOR_INSTRUCTION,
   # Use AgentTool for the agent with a built-in tool
   tools=[
       AgentTool(knowledge_agent)
   ],
   # Use sub_agents for direct delegation
   sub_agents=[
       quoting_agent
   ]
)

```

**`app/sub_agents/quoting_agent/agent.py` (Specialist)**

```
# A specialist agent for providing quotes
from google.adk.agents import Agent
from app import prompts

def get_material_cost(material: str) -> float:
   """A dummy tool to get material costs."""
   return 150.0

quoting_agent = Agent(
   name="quoting_agent",
   model="gemini-2.0-flash",
   description="Creates quotes for jobs.",
   instruction=prompts.QUOTING_INSTRUCTION,
   tools=[get_material_cost]
)

```

**`app/agent_engine_app.py` (Deployment Script)**

```
# Production-grade deployment script
import json
from pathlib import Path
import vertexai
from vertexai import agent_engines
from vertexai.preview.reasoning_engines import AdkApp

from app.agent import root_agent
from app.config import get_deployment_config

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
       requirements = f.read().strip().split("\n")

   # The agent object is the first positional argument.
   agent_to_deploy = root_agent

   # The rest of the config is passed as keyword arguments.
   deployment_kwargs = {
       "display_name": config.agent_name,
       "description": "TradieMate Assistant",
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

if __name__ == "__main__":
   deploy_agent_engine_app()
```

# Interacting with Your Deployed Agent via Command Line

This guide documents the `interact_agent.py` script, which allows you to send queries to your deployed Agent Engine agent directly from your command line.

## 1. The `interact_agent.py` Script

This Python script was created to facilitate command-line interaction with your agent. It handles session creation, sending queries, and printing the agent's response.

```python
import vertexai
from vertexai import agent_engines
from google.genai import types # For multimodal queries, if needed
import sys

# --- Configuration ---
PROJECT_ID = "609773120808" # Your Google Cloud Project ID
LOCATION = "us-central1" # Your Google Cloud Location
# This is the full resource name obtained from your deployment output
AGENT_RESOURCE_NAME = "projects/609773120808/locations/us-central1/reasoningEngines/7012953442792505344"

# --- Initialize Vertex AI ---
vertexai.init(project=PROJECT_ID, location=LOCATION)

# --- Get a reference to your deployed agent ---
remote_app = agent_engines.get(AGENT_RESOURCE_NAME)

# --- Interact with the agent ---

# Get query from command line arguments
if len(sys.argv) < 2:
    print("Usage: python interact_agent.py \"Your query here\"")
    sys.exit(1)

query_message = sys.argv[1]

# 1. Create a session (or reuse an existing one if you manage session IDs)
# For simplicity, we'll create a new session for each command-line interaction.
# For multi-turn conversations, you'd need to persist and reuse the session_id.
print("Creating a new session for this query...")
remote_session = remote_app.create_session(user_id="cli_user")
print(f"Session ID: {remote_session['id']}")

# 2. Send the query
print(f"\nSending query: \"{query_message}\"\n")

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

print("\nInteraction complete.")
```

### Key Configuration Variables:

* `PROJECT_ID`: Your Google Cloud Project ID.
* `LOCATION`: The Google Cloud region where your agent is deployed (e.g., `us-central1`).
* `AGENT_RESOURCE_NAME`: The unique identifier for your deployed agent on Agent Engine. This was provided in the deployment output (e.g., `projects/609773120808/locations/us-central1/reasoningEngines/7012953442792505344`).

## 2. Prerequisites

Before using the script, ensure you have:

* **`google-cloud-aiplatform` installed:** If you haven't already, install it in your Python environment:
  ```bash
  pip install google-cloud-aiplatform
  ```
* **Authenticated `gcloud` Application Default Credentials:** Your script needs to authenticate with Google Cloud. If you encounter authentication errors, run the following command and follow the prompts:
  ```bash
  gcloud auth application-default login
  ```

## 3. How to Use the `interact_agent.py` Script

Follow these steps to send test questions to your deployed agent:

**Step 1: Open Your Terminal**

You can be in any directory in your terminal.

**Step 2: Run the Script with Your Query**

Use the following command format. **Always enclose your question in double quotes (`"`)** to ensure it's passed as a single argument.

```bash
/Users/joeward/agent-test3/tradie_ai/.venv/bin/python /Users/joeward/agent-test3/tradie_ai/interact_agent.py "Your test question here"
```

**Example Test Questions:**

* **To test the `quoting_agent` (business operations):**

  ```bash
  /Users/joeward/agent-test3/tradie_ai/.venv/bin/python /Users/joeward/agent-test3/tradie_ai/interact_agent.py "Can you give me a quote for 50 square meters of tiling?"
  ```
* **To test the `knowledge_agent` (technical questions/search):**

  ```bash
  /Users/joeward/agent-test3/tradie_ai/.venv/bin/python /Users/joeward/agent-test3/tradie_ai/interact_agent.py "What are the latest building regulations for fire safety in commercial buildings?"
  ```
* **A general knowledge question (expected to be declined by this agent):**

  ```bash
  /Users/joeward/agent-test3/tradie_ai/.venv/bin/python /Users/joeward/agent-test3/tradie_ai/interact_agent.py "Who won the last football World Cup?"
  ```

## 4. Troubleshooting

* **`python: command not found` or similar errors:**
  This usually means the `python` executable is not in your system's PATH, or you're not using the correct Python environment. The command provided above uses the full path to the Python executable within your project's virtual environment (`.venv`), which should resolve this.
* **Authentication Errors (`Reauthentication is needed`):**
  As mentioned in the prerequisites, your Google Cloud credentials might have expired. Run `gcloud auth application-default login` to refresh them.
* **Agent Response is unexpected:**
  Review your agent's `instruction` prompt and the `description` of its tools and sub-agents. Ensure they clearly guide the agent to handle the types of queries you are sending. You can also check the detailed logs in the [Google Cloud Console](https://console.cloud.google.com/logs/query) for your Agent Engine instance to understand the agent's reasoning process.
