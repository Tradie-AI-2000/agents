# The Root Coordinator Agent for the bdm_assistant system.
from google.adk.agents import Agent
from google.adk.tools.agent_tool import AgentTool

from . import prompt
# Import all specialist agents that you will define.
from .sub_agents.market_research_agent import MarketResearchAgent
from .sub_agents.lead_generation_agent import LeadGenerationAgent
from .sub_agents.sales_material_agent import SalesMaterialAgent
from .sub_agents.client_engagement_agent import ClientEngagementAgent

# The root_agent uses the AgentTool model to call specialists.
root_agent = Agent(
    name="BDMAssistantCoordinator",
    model="gemini-2.5-pro", # Or another powerful model for orchestration
    description="A multi-agent system designed to assist Business Development Managers in New Zealand by automating and streamlining key tasks, allowing them to focus on generating new business.",
    instruction=prompt.COORDINATOR_PROMPT,
    tools=[
        AgentTool(agent=MarketResearchAgent),
        AgentTool(agent=LeadGenerationAgent),
        AgentTool(agent=SalesMaterialAgent),
        AgentTool(agent=ClientEngagementAgent),
    ]
)
