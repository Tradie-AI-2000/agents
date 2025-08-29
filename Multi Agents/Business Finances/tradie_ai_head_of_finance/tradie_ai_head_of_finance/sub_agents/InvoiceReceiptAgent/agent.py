# A specialist agent for Invoice and Receipt management.
from google.adk.agents import Agent
from google.adk.tools import FunctionTool # Import FunctionTool
from tradie_ai_head_of_finance import prompt
from tradie_ai_head_of_finance.tools import generate_invoice # Import the new tool

InvoiceReceiptAgent = Agent(
    name="InvoiceReceiptAgent",
    model="gemini-2.0-flash", # A focused, cost-effective model
    description="Manages the creation, tracking, and processing of all invoices and receipts.",
    instruction=prompt.SPECIALIST_INVOICE_RECEIPT_PROMPT,
    tools=[FunctionTool(generate_invoice)] # Use the new tool
)