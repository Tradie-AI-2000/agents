# BDM Assistant Multi-Agent System

## Overview

This is a multi-agent system designed to assist Business Development Managers (BDMs) in New Zealand, specifically tailored for TradieAI, an AI Consultancy. The system aims to automate and streamline key BDM tasks such as market research, lead generation, sales material creation, and client engagement, thereby allowing BDMs to concentrate purely on generating new business.

## Agents

The system comprises a root coordinator agent and several specialist sub-agents:

*   **`BDMAssistantCoordinator`**: The central orchestrator that understands user requests and delegates tasks to the most appropriate specialist sub-agent.
*   **`MarketResearchAgent`**: Focuses on researching market trends, industry adoption rates of AI, competitive landscapes, and potential opportunities for AI implementation in various sectors within New Zealand.
*   **`LeadGenerationAgent`**: Identifies and qualifies potential business leads for TradieAI, focusing on companies that show a propensity for AI adoption or digital transformation.
*   **`SalesMaterialAgent`**: Assists in creating tailored sales proposals, presentations, and other client-facing documents that highlight TradieAI's bespoke ADK agent solutions and AI consultancy services.
*   **`ClientEngagementAgent`**: Helps manage client communications, including drafting follow-up emails, scheduling, and nurturing relationships.

## Setup

Follow these steps to set up and run the BDM Assistant locally:

1.  **Clone the Repository (if applicable):**
    ```bash
    # If this project is part of a Git repository
    # git clone <your-repo-url>
    # cd bdm_assistant
    ```
    *(If you received this project directly, you are likely already in the `bdm_assistant` directory.)*

2.  **Create and Activate Virtual Environment:**
    ```bash
    python3 -m venv .venv
    source .venv/bin/activate
    ```
    *(Remember to activate the virtual environment for every new terminal session.)*

3.  **Configure Google Cloud Environment:**
    Ensure you have the Google Cloud SDK installed. Then, authenticate and enable necessary APIs:
    ```bash
    gcloud auth login
    gcloud auth application-default login
    gcloud config set project <YOUR_GCP_PROJECT_ID> # Replace with your actual GCP Project ID
    gcloud services enable aiplatform.googleapis.com storage.googleapis.com cloudbuild.googleapis.com run.googleapis.com artifactregistry.googleapis.com
    ```
    *(Follow any browser-based prompts for authentication.)*

4.  **Install Dependencies:**
    ```bash
    cd bdm_assistant # Ensure you are in the project root
    make install
    # If 'make install' fails, try direct pip install:
    # ./.venv/bin/pip install -e .[dev]
    ```

5.  **Configure Environment Variables:**
    Copy the example environment file and update it with your specific details:
    ```bash
    cp .env.example .env
    ```
    Open the newly created `.env` file and fill in your `GOOGLE_CLOUD_PROJECT`, `GOOGLE_CLOUD_LOCATION`, `GOOGLE_CLOUD_STAGING_BUCKET`, and optionally `GOOGLE_API_KEY`.

## Usage

Once set up, you can run the local development server and interact with the agents via a web UI.

1.  **Run the Local Development Server:**
    ```bash
    cd bdm_assistant # Ensure you are in the project root
    make dev
    ```
    The server will typically run on `http://localhost:8000`.

2.  **Interact with the Agents:**
    Open your web browser and navigate to `http://localhost:8000`. You can interact with the `BDMAssistantCoordinator` by typing your requests into the chat interface.

    Here are some example prompts from the perspective of Joe Ward, owner of TradieAI:

    *   **Market Research:** "Research the current adoption rates of AI solutions in the New Zealand construction industry, specifically identifying companies that might be early adopters of bespoke ADK agents."
    *   **Lead Generation:** "Find potential leads for manufacturing businesses in Waikato, NZ, that have recently posted job openings related to digital transformation or automation, indicating a need for AI implementation."
    *   **Sales Material:** "Draft a compelling sales proposal for a new client, 'NZ Logistics Solutions', outlining how our bespoke ADK agents can optimize their supply chain and reduce operational costs."
    *   **Client Engagement:** "Prepare a follow-up email for 'AgriTech Innovations Ltd.' after our initial consultation yesterday, summarizing the proposed AI solution and next steps for developing their custom ADK agent."

## Deployment

Deployment scripts are not yet fully configured. Refer to the `Makefile` and ADK documentation for future deployment options to platforms like Google Cloud Vertex AI.

## Powering Up Your Agents with Custom Tools

This multi-agent system is designed to be extensible. You can significantly enhance its capabilities by integrating custom tools and APIs. This involves creating new Python functions (like `companies_office_direct_search` for web scraping) and wrapping them in new ADK Agent definitions within `bdm_assistant/bdm_assistant/tools.py`.

Consider exploring integrations for:

*   **Direct Email Sending:** Automate sending emails directly from the `ClientEngagementAgent` using Python's `smtplib` or a transactional email API (e.g., SendGrid).
*   **Sentiment Analysis:** Analyze the emotional tone of client communications or market feedback using APIs like Google Cloud Natural Language API.
*   **CRM Integration:** Connect directly to your CRM (e.g., HubSpot, Salesforce) to automate lead updates, activity logging, and contact management.
*   **Lead Enrichment:** Use APIs (e.g., Hunter.io, Lusha) to automatically gather more data about leads.
*   **Automated Outreach:** Integrate with sales outreach platforms (e.g., Reply.io) to automate personalized communication sequences.
*   **Meeting Scheduling:** Use APIs (e.g., Calendly, Vyte) to automate meeting booking and calendar management.

These integrations can dramatically increase the agents' usability and performance, allowing your BDMs to focus even more on core business generation.
