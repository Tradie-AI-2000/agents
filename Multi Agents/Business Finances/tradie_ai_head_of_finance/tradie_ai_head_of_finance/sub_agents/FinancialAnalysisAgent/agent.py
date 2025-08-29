# A specialist agent for Financial Analysis and Reporting.
from google.adk.agents import Agent
from tradie_ai_head_of_finance import prompt
FinancialAnalysisAgent = Agent(
    name="FinancialAnalysisAgent",
    model="gemini-2.0-flash", # A focused, cost-effective model
    description="Performs in-depth financial analysis, generates various financial reports, and provides key insights.",
    instruction=prompt.SPECIALIST_FINANCIAL_ANALYSIS_PROMPT,
    # tools=[] # Add any custom or built-in tools here.
)
