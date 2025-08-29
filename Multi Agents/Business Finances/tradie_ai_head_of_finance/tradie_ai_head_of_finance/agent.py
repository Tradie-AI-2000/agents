# The Root Coordinator Agent for the tradie_ai_head_of_finance system.
from google.adk.agents import Agent
from google.adk.tools.agent_tool import AgentTool

from . import prompt
# Import all specialist agents that you will define.
from .sub_agents.InvoiceReceiptAgent import InvoiceReceiptAgent
from .sub_agents.TaxComplianceAgent import TaxComplianceAgent
from .sub_agents.FinancialAnalysisAgent import FinancialAnalysisAgent
from .sub_agents.ForecastingWealthAgent import ForecastingWealthAgent
from .sub_agents.DataIntegrationAgent import DataIntegrationAgent

# The root_agent uses the AgentTool model to call specialists.
root_agent = Agent(
    name="TradieAIFinanceCoordinator",
    model="gemini-2.5-pro", # Or another powerful model for orchestration
    description="A multi-agent system for comprehensive financial management for TradieAI, acting as a personal accountant, wealth manager, and financial virtual assistant.",
    instruction=prompt.COORDINATOR_PROMPT,
    tools=[
        AgentTool(agent=InvoiceReceiptAgent),
        AgentTool(agent=TaxComplianceAgent),
        AgentTool(agent=FinancialAnalysisAgent),
        AgentTool(agent=ForecastingWealthAgent),
        AgentTool(agent=DataIntegrationAgent),
    ]
)
