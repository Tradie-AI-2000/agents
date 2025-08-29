# A specialist agent for Data Integration.
from google.adk.agents import Agent
from tradie_ai_head_of_finance import prompt
DataIntegrationAgent = Agent(
    name="DataIntegrationAgent",
    model="gemini-2.0-flash", # A focused, cost-effective model
    description="Securely integrates with and retrieves financial data from various external sources.",
    instruction=prompt.SPECIALIST_DATA_INTEGRATION_PROMPT,
    # tools=[] # Add any custom or built-in tools here.
)
