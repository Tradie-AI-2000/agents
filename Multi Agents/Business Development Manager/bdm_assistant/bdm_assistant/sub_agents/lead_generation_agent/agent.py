# A specialist agent for identifying and qualifying potential leads.
from google.adk.agents import Agent
from bdm_assistant import prompt
from bdm_assistant.tools import SearchAgent # Import tools from the central file
from google.adk.tools.agent_tool import AgentTool

LeadGenerationAgent = Agent(
    name="LeadGenerationAgent",
    model="gemini-2.0-flash", # A focused, cost-effective model
    description="Identifies and qualifies potential leads for a Business Development Manager.",
    instruction=prompt.LEAD_GENERATION_PROMPT,
    tools=[
        AgentTool(agent=SearchAgent) # Example: Lead generation often involves searching
    ]
)
