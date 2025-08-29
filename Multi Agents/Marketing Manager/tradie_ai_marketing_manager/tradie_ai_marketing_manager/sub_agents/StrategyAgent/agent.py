# The StrategyAgent, now using other agents as tools.
from google.adk.agents import Agent
from google.adk.tools.agent_tool import AgentTool
from tradie_ai_marketing_manager import prompt
from tradie_ai_marketing_manager.tools import GoogleSearchAgent, SocialMediaAgent

StrategyAgent = Agent(
    name="StrategyAgent",
    model="gemini-2.5-flash",
    description="Conducts market research, analyzes competitors, and develops marketing strategies and plans by delegating to specialized research agents.",
    instruction=prompt.SPECIALIST_1_PROMPT,
    tools=[
        AgentTool(agent=GoogleSearchAgent),
        AgentTool(agent=SocialMediaAgent),
    ],
)
