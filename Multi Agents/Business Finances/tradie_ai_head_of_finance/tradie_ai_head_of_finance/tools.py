from google.adk.agents import Agent
from google.adk.tools import google_search, FunctionTool
import datetime # Import datetime module

# --- Custom Function Tools ---

def generate_invoice(client_name: str, amount: float, description: str) -> str:
    """Generates a new invoice for a client.

    Args:
        client_name: The name of the client.
        amount: The amount of the invoice.
        description: A description of the work done.
    """
    invoice_id = f"INV-{datetime.datetime.now().strftime('%Y%m%d%H%M%S')}"
    invoice_date = datetime.date.today().strftime('%Y-%m-%d')

    invoice_details = f"""
--- INVOICE ---
Invoice ID: {invoice_id}
Date: {invoice_date}
Client: {client_name}
-----------------
Description: {description}
Amount: ${amount:,.2f} NZD
-----------------
Status: Generated
"""
    print(f"DEBUG: Invoice generated: {invoice_details}") # For debugging purposes
    return invoice_details

# --- Agent-as-a-Tool Definitions ---

SearchAgent = Agent(
    name="SearchAgent",
    model="gemini-2.0-flash",
    description="Performs a Google search.",
    tools=[google_search],
)
