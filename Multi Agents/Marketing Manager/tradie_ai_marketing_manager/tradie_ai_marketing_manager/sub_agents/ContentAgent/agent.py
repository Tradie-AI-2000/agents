# A specialist agent for creating marketing content.
from google.adk.agents import Agent
from tradie_ai_marketing_manager import prompt
from tradie_ai_marketing_manager.tools import (
    get_seo_keywords,
    generate_placeholder_image,
)

# Define any custom Python tool functions here if needed.

ContentAgent = Agent(
    name="ContentAgent",
    model="gemini-2.5-flash", # A focused, cost-effective model
    description="Generates marketing content, including social media posts, email campaigns, blog articles, and ad copy.",
    instruction=prompt.SPECIALIST_2_PROMPT,
    tools=[get_seo_keywords, generate_placeholder_image],
)