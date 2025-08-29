# A specialist agent for managing client communications and relationships.
from google.adk.agents import Agent
from bdm_assistant import prompt
from bdm_assistant.tools import my_custom_tool # Example: A custom tool for CRM interaction or email drafting

ClientEngagementAgent = Agent(
    name="ClientEngagementAgent",
    model="gemini-2.0-flash", # A focused, cost-effective model
    description="Helps manage client communications and relationships for a Business Development Manager.",
    instruction=prompt.CLIENT_ENGAGEMENT_PROMPT,
    tools=[my_custom_tool] # Add any custom or built-in tools here.
)
