# A specialist agent for researching target markets, industry trends, and potential opportunities.
from google.adk.agents import Agent
from bdm_assistant import prompt
from bdm_assistant.tools import SearchAgent, CompaniesOfficeDirectSearchAgent # Import both search agents
from google.adk.tools.agent_tool import AgentTool

MarketResearchAgent = Agent(
    name="MarketResearchAgent",
    model="gemini-2.0-flash", # A focused, cost-effective model
    description="Researches target markets, industry trends, and potential opportunities for a Business Development Manager.",
    instruction=prompt.MARKET_RESEARCH_PROMPT,
    tools=[
        AgentTool(agent=SearchAgent), # General web search
        AgentTool(agent=CompaniesOfficeDirectSearchAgent) # Targeted Companies Office direct search
    ]
)
