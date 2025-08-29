# A specialist agent for Tax and Compliance.
from google.adk.agents import Agent
from tradie_ai_head_of_finance import prompt
TaxComplianceAgent = Agent(
    name="TaxComplianceAgent",
    model="gemini-2.0-flash", # A focused, cost-effective model
    description="Handles tax calculations, ensures compliance with New Zealand tax laws, and prepares tax-related reports.",
    instruction=prompt.SPECIALIST_TAX_COMPLIANCE_PROMPT,
    # tools=[] # Add any custom or built-in tools here.
)
