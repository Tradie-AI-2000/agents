# The Root Coordinator Agent for the gmail_manager system.
from google.adk.agents import Agent
from google.adk.tools.agent_tool import AgentTool

from . import prompt
# Import all specialist agents that you will define.
from .sub_agents.email_categorizer import EmailCategorizer
from .sub_agents.email_drafter import EmailDrafter
from .sub_agents.booking_link_inserter import BookingLinkInserter

# The root_agent uses the AgentTool model to call specialists.
root_agent = Agent(
    name="GmailManager",
    model="gemini-2.5-pro", # Or another powerful model for orchestration
    description="Orchestrates email management, delegating tasks to specialist agents for categorization, drafting, and booking link insertion.",
    instruction=prompt.COORDINATOR_PROMPT,
    tools=[
        AgentTool(agent=EmailCategorizer),
        AgentTool(agent=EmailDrafter),
        AgentTool(agent=BookingLinkInserter),
    ]
)
