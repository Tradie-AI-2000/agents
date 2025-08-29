# A specialist agent for Forecasting and Wealth Management.
from google.adk.agents import Agent
from tradie_ai_head_of_finance import prompt
ForecastingWealthAgent = Agent(
    name="ForecastingWealthAgent",
    model="gemini-2.0-flash", # A focused, cost-effective model
    description="Develops financial forecasts, assists with wealth management strategies, and provides high-level financial planning guidance.",
    instruction=prompt.SPECIALIST_FORECASTING_WEALTH_PROMPT,
    # tools=[] # Add any custom or built-in tools here.
)
