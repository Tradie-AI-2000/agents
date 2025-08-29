# A specialist agent for categorizing emails.
from google.adk.agents import Agent
from gmail_manager import prompt

EmailCategorizer = Agent(
    name="EmailCategorizer",
    model="gemini-2.0-flash", # A focused, cost-effective model
    description="Categorizes incoming emails based on content and sender to determine if a response is required.",
    instruction=prompt.EMAIL_CATEGORIZER_PROMPT,
    tools=[] # Add any custom or built-in tools here.
)
