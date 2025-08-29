# The Root Coordinator Agent for the tradie_ai_marketing_manager system.
from google.adk.agents import Agent
from google.adk.tools.agent_tool import AgentTool

from . import prompt
# Import all specialist agents that you will define.
from .sub_agents.StrategyAgent import StrategyAgent
from .sub_agents.ContentAgent import ContentAgent
from .sub_agents.AnalyticsAgent import AnalyticsAgent

# The root_agent uses the AgentTool model to call specialists.
root_agent = Agent(
    name="MarketingCoordinator",
    model="gemini-2.5-flash", # Or another powerful model for orchestration
    description="A multi-agent system that acts as a marketing manager for tradespeople, handling strategy, content creation, and performance analytics.",
    instruction=prompt.COORDINATOR_PROMPT,
    tools=[
        AgentTool(agent=StrategyAgent),
        AgentTool(agent=ContentAgent),
        AgentTool(agent=AnalyticsAgent),
    ]
)
