# Central repository for all tools and tool-agents.
from google.adk.agents import Agent
from google.adk.tools import google_search

# --- Custom Function Tools ---

# Placeholder for Email Reading Tool
def read_email_content(email_id: str) -> str:
    """A placeholder tool to read the content of an email given its ID."""
    # In a real implementation, this would interact with a Gmail API or similar.
    return f"Content of email {email_id}: This is a sample email content."

# --- Agent-as-a-Tool Definitions ---

SearchAgent = Agent(
    name="SearchAgent",
    model="gemini-2.0-flash",
    description="Performs a Google search.",
    tools=[google_search],
)
