# A specialist agent for creating sales proposals, presentations, and other client-facing documents.
from google.adk.agents import Agent
from bdm_assistant import prompt
from bdm_assistant.tools import my_custom_tool # Example: A custom tool for generating sales content

SalesMaterialAgent = Agent(
    name="SalesMaterialAgent",
    model="gemini-2.0-flash", # A focused, cost-effective model
    description="Assists in creating sales proposals, presentations, and other client-facing documents for a Business Development Manager.",
    instruction=prompt.SALES_MATERIAL_PROMPT,
    tools=[my_custom_tool] # Add any custom or built-in tools here.
)
