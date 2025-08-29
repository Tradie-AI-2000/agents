# Central repository for all tools and tool-agents.

from google.adk.agents import Agent
from google.adk.tools import google_search

# --- Custom Function Tools --------------------------------------------------

def get_seo_keywords(topic: str) -> list[str]:
    """
    Gets a list of SEO keywords for a given topic.

    Args:
        topic: The topic to get SEO keywords for.

    Returns:
        A list of relevant SEO keywords.
    """
    # This is a simulated function. In a real application, this would
    # call a real SEO API.
    print(f"--- TOOL: Getting SEO keywords for {topic} ---")
    if "plumbing" in topic.lower():
        return ["emergency plumber", "blocked drain repair", "hot water cylinder", "Auckland plumbing services"]
    return ["local tradie marketing", "get more leads", "small business social media", f"{topic} marketing"]

def generate_placeholder_image(topic: str) -> str:
    """
    Generates a URL for a placeholder image based on a topic.

    Args:
        topic: The topic for the image, which will be used as text.

    Returns:
        A URL for a placeholder image.
    """
    print(f"--- TOOL: Generating placeholder image for {topic} ---")
    formatted_topic = topic.replace(" ", "+")
    return f"https://placehold.co/600x400?text={formatted_topic}"


# --- Agent-as-a-Tool Definitions ------------------------------------------

# Note: These agents are not intended to be called directly by the coordinator.
# They are used as tools by other specialist agents.

GoogleSearchAgent = Agent(
    name="GoogleSearchAgent",
    model="gemini-2.5-flash",
    description="Performs a Google search to find information on the web.",
    instruction="You are a search agent. Use the google_search tool to answer the user's query.",
    tools=[google_search],
)

def get_competitor_social_media(business_type: str, location: str) -> str:
    """
    Finds the social media links of competing businesses in a specific location.

    Args:
        business_type: The type of tradie business (e.g., 'plumber', 'electrician').
        location: The city or area to search in (e.g., 'Auckland', 'Wellington').

    Returns:
        A string containing a list of competitors and their social media URLs.
    """
    # This is a simulated function. In a real application, this would
    # call a real API like Google Places or a social media analytics service.
    print(f"--- TOOL: Searching for social media of {business_type}s in {location} ---")
    if business_type.lower() == 'plumber' and location.lower() == 'auckland':
        return (
            "Competitor Social Media Links:\n"
            "- Auckland Plumbers Ltd: facebook.com/aucklandplumbers\n"
            "- Drain-O-Rama: instagram.com/drainorama_akl\n"
            "- Pipe Dreams Plumbing: facebook.com/pipedreams"
        )
    return f"No specific social media data found for {business_type} in {location}. Try a broader search."

SocialMediaAgent = Agent(
    name="SocialMediaAgent",
    model="gemini-2.5-flash",
    description="Finds the social media links of competing businesses in a specific location.",
    instruction="You are a social media intelligence agent. Use the get_competitor_social_media tool to find competitor information.",
    tools=[get_competitor_social_media],
)
