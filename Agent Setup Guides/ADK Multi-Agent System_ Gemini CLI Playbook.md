# ADK Multi-Agent System: Gemini CLI Playbook

This document outlines the precise, step-by-step procedures for the Gemini CLI tool to follow when executing common development, testing, and deployment tasks for an ADK multi-agent system.

---

## Best Practices: Virtual Environments

Proper virtual environment management is crucial for a consistent and reproducible development experience.

*   **Create a Virtual Environment:** Always create a virtual environment for your project to isolate dependencies.
    ```bash
    python3 -m venv .venv
    ```
*   **Proper Virtual Environment Activation:** To ensure your virtual environment is correctly activated and recognized, always follow these steps:
    1.  **Navigate to your project directory:**
        ```bash
        cd /path/to/your/project
    ```
    2.  **Activate the virtual environment:**
        -   **For `venv` (standard Python virtual environments):**
            ```bash
            source .venv/bin/activate
            ```
        -   **For `uv` (if you are using `uv` for dependency management):**
            `uv` automatically manages the virtual environment. When you run commands like `uv run <command>`, `uv` ensures the command is executed within the project's virtual environment. However, if you need to activate it explicitly for other tools or direct Python execution, you can still use the `source` command as above after `uv sync` has created the `.venv` directory.
*   **Deactivate When Done:** When you're finished working on a project, deactivate its virtual environment.
    ```bash
    deactivate
    ```

---

### **Task 1: New Project Creation**

*Goal: Create a complete, production-ready project structure from scratch.*

1.  **Ask the user for the `<project_name>`** (e.g., `tradie_social_media_manager`).
2.  **Execute shell command:** `adk create <project_name>`
3.  **Navigate into the new directory:** `cd <project_name>`
4.  **Activate the project's virtual environment:**
    ```bash
    source .venv/bin/activate
    ```
5.  **Create the professional project structure** by creating the following files with the content specified in the main design guide's Appendix:
    - `Makefile`
    - `pyproject.toml`
    - `app/prompts.py`
    - `app/config.py`
    - `app/agent_engine_app.py`
    - `.env`
    - Boilerplate for `app/agent.py` and `app/sub_agents/`.
6.  **Inform the user** that the project structure is created and that they must populate the`.env` file.

---

### **Task 2: First-Time GCP Environment Setup**

*Goal: Configure the Google Cloud environment with all necessary resources and permissions.*

1.  **Inform the user** that this is a one-time setup and requires them to provide their `PROJECT_ID`, when prompted by the CLI commands.
2.  **Execute `gcloud auth login`** and instruct the user to follow the browser-based authentication flow.
3.  **Execute `gcloud auth application-default login`**.
4.  **Execute `gcloud config set project <PROJECT_ID>`**.
5.  **Execute `gcloud services enable aiplatform.googleapis.com storage.googleapis.com cloudbuild.googleapis.com run.googleapis.com artifactregistry.googleapis.com`**.
6.  **Execute `gcloud billing projects link <PROJECT_ID> --billing-account=<BILLING_ACCOUNT_ID>`**.
7.  **Execute `gcloud storage buckets create gs://<PROJECT_ID>-adk-staging --project=<PROJECT_ID> --location=<LOCATION>`**.
8.  **Execute `gcloud projects add-iam-policy-binding <PROJECT_ID> --member="user:$(gcloud config get-value account)" --role="roles/aiplatform.user"`**.
9.  **Execute `gcloud projects add-iam-policy-binding <PROJECT_ID> --member="user:$(gcloud config get-value account)" --role="roles/iam.serviceAccountTokenCreator"`**.
10. **Confirm to the user** that the cloud environment has been configured.

---

### **Task 3: Add a New Specialist Agent**

*Goal: Add a new, empty specialist agent to the project.*

**IMPORTANT: Before creating any new agent, you MUST consult and strictly adhere to the "7. Strict ADK Design Principles for Gemini CLI" section in the `Guide-to-Designing-Multi-Agent-Systems-with ADK.md` document. Pay particular attention to the rules regarding `output_schema` and `tools` to ensure a "one-shot success" in agent design.**

1.  **Ask the user for the new `<agent_name>`** (e.g., `image_generation_agent`).
2.  **Create the directory structure:** `app/sub_agents/<agent_name>/`.
3.  **Create `app/sub_agents/<agent_name>/__init__.py`**.
4.  **Create `app/sub_agents/<agent_name>/agent.py`** with boilerplate agent definition code, ensuring it complies with ADK design principles.
5.  **Remind the user** to update the root `app/agent.py` to import and use the new agent in its `sub_agents` list or `tools` list.

---

### **Task 4: Local Development & Testing**

*Goal: Run the agent system locally for interactive testing.*

1.  **Ensure you are in the project's root directory** (e.g., `/path/to/your/project_name`). This is crucial for ADK to correctly locate your `root_agent`.
2.  Upon user request to test, **execute `make dev`**.
3.  **Provide the local URL** (`http://localhost:8000` or as specified in the `Makefile`) to the user.
### Task 4.1: Understanding ADK Command Context

When executing ADK commands, especially those involving file paths or project structures, it's important to understand the context in which these commands run and how arguments are interpreted.

*   **Working Directory:** Most ADK commands assume they are being run from the root of your ADK project. This means that relative paths provided as arguments will be resolved against this root directory. If you run an ADK command from a subdirectory, you might need to adjust your paths accordingly or specify the project root explicitly if the command supports it.

*   **Argument Interpretation:** Pay close attention to how ADK commands interpret their arguments:
    *   **Agent Paths:** When specifying an agent for commands like `adk run <agent_path>`, the `agent_path` typically refers to the Python module path (e.g., `app.agent` for `app/agent.py`) relative to your project's root, not a file system path.
    *   **Directory Arguments:** For commands like `adk web [agents_dir]`, `agents_dir` usually expects a path to a directory containing your agent modules. This path can be relative to your current working directory or an absolute path.
    *   **Glob Patterns:** Some ADK tools or underlying utilities might support glob patterns (e.g., `**/*.py`) for specifying multiple files or directories. Always consult the specific command's documentation or help output (`adk <command> --help`) for details on argument interpretation.

Understanding these nuances will help you avoid common errors related to file not found, module not found, or incorrect command execution.

---

#### Troubleshooting Local Development

Encountering issues during local development is common. Here are solutions for frequently observed problems:

*   **Port Conflicts (`address already in use`):**
    If `make dev` fails with an error like `[Errno 48] address already in use`, it means another process is using the default port (8000).
    *   **Solution:**
        1.  **Identify the process:** Use `lsof -i :8000` (replace `8000` with the conflicting port if different) to find the PID (Process ID).
        2.  **Terminate the process:** Use `kill -9 <PID>` to forcefully stop it.
        3.  **Run on a different port:** Alternatively, you can run `adk web` on a different port directly:
            ```bash
            uv run adk web app --port 8001
            ```

*   **`adk web` `[WIP] _load_from_yaml_config` Error:**
    This error indicates that `adk web` is attempting to load agents from a YAML configuration, a feature that is still under development. This is typically an internal ADK issue and not a problem with your Python agent definitions or folder structure.
    *   **Solution:**
        *   **Verify Agent Definitions:** Ensure all your `LlmAgent` definitions adhere to the `output_schema` and `tools` constraint (see next point). Sometimes, resolving these `ValidationError`s can implicitly resolve this `[WIP]` error.
        *   **Use `adk run`:** If the `adk web` UI consistently fails with this error, use `adk run` for CLI-based interaction, which is more robust:
            ```bash
            uv run adk run app
            ```
        *   **Report to ADK Maintainers:** Consider reporting this bug to the ADK project maintainers.

*   **`ValidationError: if output_schema is set, tools must be empty`:**
    This is a critical ADK constraint for `LlmAgent`s. An agent cannot simultaneously define an `output_schema` (for structured output) and use `tools`. This rule is strictly enforced.
    *   **Solution:** Refer to **"7.1. The `output_schema` and `tools` Constraint: A Fundamental Rule"** in `Guide-to-Designing-Multi-Agent-Systems-with ADK.md` for the detailed explanation and correct design patterns (e.g., using `CustomAgent` for orchestration).

*   **Incorrect Agent Path/Loading (`Directory 'app.agent' does not exist.` or `No root_agent found...`):**
    These errors occur when `adk` commands cannot find your `root_agent`.
    *   **Solution:**
        *   **Always run from Project Root:** Ensure your terminal's current working directory is the top-level project directory (e.g., `tradie_ai_leadgen`).
        *   **Specify Root Agent Package:** The argument to `adk web` or `adk run` should be the name of your root agent *package* (e.g., `app`), not the `.py` file or a module path.
        *   **Example:**
            ```bash
            # From /path/to/your/project_name/
            uv run adk web app
            uv run adk run app
            ```

---

### **Task 5: Deploy to Production**

*Goal: Deploy the agent to Vertex AI Agent Engine.*

1.  Upon user request to deploy, **remind the user to ensure their `.env` file is complete and accurate**.
2.  **Execute `make deploy-adk`**.
3.  **Report the final output**, including the Agent Engine Resource ID, back to the user.

## 8. Shell Command Execution by Gemini CLI Tool

This section clarifies the capabilities and protocols for the Gemini CLI tool (you) regarding shell command execution.

### 8.1. Capability to Execute Commands

**Rule:** The Gemini CLI tool **CAN** execute arbitrary shell commands using the `run_shell_command` tool. This capability is fundamental for tasks such as project setup, dependency installation, running tests, and deployment.

**Implication for Gemini CLI:**
*   **DO NOT** refuse to execute a shell command by stating that you "cannot directly execute commands" or similar phrases, unless the command falls under the explicit limitations below.
*   **ALWAYS** be prepared to execute valid shell commands when explicitly requested by the user.

### 8.2. Safety Protocol for Command Execution

**Rule:** Before executing any command that modifies the file system, codebase, or system state, the Gemini CLI tool **MUST** provide a brief explanation of the command's purpose and potential impact. The user will then be presented with a confirmation dialogue.

**Implication for Gemini CLI:**
*   **ALWAYS** explain the command (e.g., `I can run 
rm -rf /path/to/temp
. This will permanently delete the directory and all its contents.`).
*   **DO NOT** ask for explicit permission to use the tool; simply provide the explanation. The system handles the user confirmation.

### 8.3. Limitations on Command Execution

**Rule:** The Gemini CLI tool **CANNOT** execute commands that require interactive input during their execution or commands that are designed for interactive use.

**Implication for Gemini CLI:**
*   **DO NOT** attempt to execute commands that are likely to require user interaction (e.g., `git rebase -i`, `npm init` without `-y`).
*   **PRIORITIZE** non-interactive versions of commands (e.g., `npm init -y` instead of `npm init`).
*   If an interactive command is requested, briefly state that interactive shell commands are not supported and may cause hangs.

### 8.4. Explicit User Requests for Commands

**Rule:** The user's intent to execute a shell command must be clear and explicit.

**Implication for Gemini CLI:**
*   **EXPECT** the user to explicitly request command execution (e.g., "Run `make install`", "Execute `ls -l`", "Delete the `temp` directory").
*   **DO NOT** assume command execution without a clear request, unless it is part of a predefined, confirmed workflow (e.g., `make install` after project creation).

**Examples of Valid Requests:**
*   `Run 'npm install'`
*   `Execute 'pytest tests/my_test.py'`
*   `Delete the 'build' directory.`
*   `Start the server with 'node server.js &'`

**Examples of Invalid Requests (due to interactivity or ambiguity):**
*   `Tell me how to configure git.` (Ambiguous, asks for explanation, not execution)
*   `Can you help me with an interactive rebase?` (Interactive command)
