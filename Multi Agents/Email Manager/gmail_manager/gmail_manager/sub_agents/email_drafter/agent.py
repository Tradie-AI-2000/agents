# A specialist agent for drafting email replies.
from google.adk.agents import Agent
from gmail_manager import prompt

EmailDrafter = Agent(
    name="EmailDrafter",
    model="gemini-2.0-flash", # A focused, cost-effective model
    description="Drafts personalized email replies, considering the user's tone of voice, and intelligently decides whether a reply is necessary.",
    instruction=prompt.EMAIL_DRAFTER_PROMPT,
    tools=[] # Add any custom or built-in tools here.
)
