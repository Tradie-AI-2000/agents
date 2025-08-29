# TradieAI Head of Finance Multi-Agent System

This project implements a multi-agent system designed to act as a comprehensive financial manager for TradieAI. It aims to cover various financial aspects including tax, invoices, receipts, analysis, forecasting, and reporting, functioning as a personal accountant, wealth manager, and financial virtual assistant.

## Architecture

The system is built with a coordinator agent that delegates tasks to specialized sub-agents:

*   **`TradieAIFinanceCoordinator`**: The central hub for delegating financial queries.
*   **`InvoiceReceiptAgent`**: Manages invoice and receipt processing.
*   **`TaxComplianceAgent`**: Handles tax calculations and compliance.
*   **`FinancialAnalysisAgent`**: Performs financial analysis and generates reports.
*   **`ForecastingWealthAgent`**: Develops financial forecasts and wealth management strategies.
*   **`DataIntegrationAgent`**: Securely integrates and retrieves financial data from external sources.

## Setup and Installation

Follow these steps to set up and run the project locally.

### 1. Clone the Repository (if applicable)

```bash
# If this were a git repository, you would clone it here.
# For now, assume you are in the project root directory.
```

### 2. Create and Activate Virtual Environment

Navigate to the project root directory (`tradie_ai_head_of_finance`) and set up the virtual environment:

```bash
bash
cd tradie_ai_head_of_finance
python3 -m venv .venv
source .venv/bin/activate
```

### 3. Install Dependencies

Install the required Python packages:

```bash
make install
```

### 4. Google Cloud Configuration (One-Time Setup)

This project leverages Google Cloud services. Ensure you have the Google Cloud SDK installed. You will need to authenticate and enable necessary APIs.

```bash
gcloud auth login
gcloud auth application-default login
gcloud config set project YOUR_GCP_PROJECT_ID # Replace with your actual project ID
gcloud services enable aiplatform.googleapis.com storage.googleapis.com cloudbuild.googleapis.com run.googleapis.com artifactregistry.googleapis.com
```

### 5. Configure Environment Variables

Copy the example environment file and update it with your Google Cloud project details and API keys:

```bash
cp .env.example .env
```

Open the `.env` file and fill in the placeholder values:

```
# GCP Configuration
GOOGLE_CLOUD_PROJECT="your-gcp-project-id"
GOOGLE_CLOUD_LOCATION="us-central1" # Or your preferred region
GOOGLE_CLOUD_STAGING_BUCKET="your-gcp-staging-bucket-name" # Create a unique bucket name in GCP

# Set to true when deploying to Vertex AI
GOOGLE_GENAI_USE_VERTEXAI="True"

# Gemini API Key (for local development if not using Vertex)
# GOOGLE_API_KEY="your-gemini-api-key" # Uncomment and add your API key if not using Vertex AI
```

## Running the Development Server

To start the ADK web server with hot-reloading, run the following command from the `tradie_ai_head_of_finance` directory:

```bash
make dev
```

The server will typically be accessible at `http://localhost:8000`.

## Interacting with the Agent

Once the server is running, you can interact with the `TradieAIFinanceCoordinator` agent through its web interface or by sending requests to its API endpoints.

Example interactions might include:

*   "Generate a new invoice for [Client Name] for [Amount] for the work done on [Description]."
*   "What is my current tax liability for this quarter?"
*   "Generate a profit and loss report for the last fiscal year."
*   "Provide a financial forecast for the next 12 months."

## Power Up Your Agents: Expanding Functionality with Custom Tools

To massively increase the functionality of your Head of Finance agent, you can develop and integrate additional custom tools. These tools can interact with external APIs, perform complex calculations, or automate workflows. Here are some examples of powerful tools you could create:

### General Utility Tools

*   **`send_email(recipient: str, subject: str, body: str, attachment_paths: list[str] = None)`**
    *   **Description:** Sends an email to a specified recipient with a given subject, body, and optional attachments.
    *   **Impact:** Enables the agents to send automated invoices, reports, reminders, or notifications directly to clients or internal teams.

### Invoice & Receipt Management (`InvoiceReceiptAgent`)

*   **`parse_receipt_ocr(image_path: str) -> dict`**
    *   **Description:** Extracts key information (vendor, amount, date, items) from a receipt image using Optical Character Recognition (OCR).
    *   **Impact:** Automates expense tracking by processing physical or digital receipt images, reducing manual data entry.

### Tax & Compliance (`TaxComplianceAgent`)

*   **`fetch_tax_rates_nz(year: int) -> dict`**
    *   **Description:** Retrieves current and historical tax rates for New Zealand from a reliable government API or data source.
    *   **Impact:** Ensures tax calculations are always based on the most up-to-date regulations, improving accuracy and compliance.

### Financial Analysis & Reporting (`FinancialAnalysisAgent`)

*   **`generate_financial_report_pdf(report_data: dict, report_type: str, output_path: str)`**
    *   **Description:** Generates a professional PDF financial report (e.g., Profit & Loss, Balance Sheet) from structured data.
    *   **Impact:** Provides polished, shareable financial documents for stakeholders, enhancing professional presentation.

### Data Integration (`DataIntegrationAgent`)

*   **`connect_xero_api(api_key: str, client_id: str, client_secret: str) -> XeroClient`**
    *   **Description:** Establishes a connection to the Xero accounting software API, allowing for programmatic access to financial data.
    *   **Impact:** Enables seamless synchronization of invoices, transactions, and contacts with Xero, centralizing financial data management.

### How to Add New Tools:

1.  **Define the Tool Function:** Create your Python function in `tradie_ai_head_of_finance/tradie_ai_head_of_finance/tools.py`. Ensure it has clear type hints and a docstring describing its purpose and parameters.
2.  **Wrap with `FunctionTool`:** In the relevant specialist agent's `agent.py` file, import your new function and wrap it with `FunctionTool` (e.g., `tools=[FunctionTool(your_new_tool_function)]`).
3.  **Update Agent's Instruction:** Modify the specialist agent's prompt in `tradie_ai_head_of_finance/tradie_ai_head_of_finance/prompt.py` to instruct it on when and how to use the new tool.
4.  **Test:** Thoroughly test the new tool and the agent's ability to use it correctly.