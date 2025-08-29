# A specialist agent for inserting booking links.
from google.adk.agents import Agent
from gmail_manager import prompt

BookingLinkInserter = Agent(
    name="BookingLinkInserter",
    model="gemini-2.0-flash", # A focused, cost-effective model
    description="Inserts a predefined Google Calendar booking link into an email draft.",
    instruction=prompt.BOOKING_LINK_INSERTER_PROMPT,
    tools=[] # Add any custom or built-in tools here.
)
