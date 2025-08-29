# A specialist agent for tracking performance and analytics.
from google.adk.agents import Agent
from tradie_ai_marketing_manager import prompt
# from google.adk.tools import ... # Import any built-in tools if needed.

# Define any custom Python tool functions here if needed.

AnalyticsAgent = Agent(
    name="AnalyticsAgent",
    model="gemini-2.5-flash", # A focused, cost-effective model
    description="Tracks marketing campaign performance, analyzes key metrics (KPIs), and generates reports with data-driven insights.",
    instruction=prompt.SPECIALIST_3_PROMPT,
    # tools=[...] # Add any custom or built-in tools here.
)
