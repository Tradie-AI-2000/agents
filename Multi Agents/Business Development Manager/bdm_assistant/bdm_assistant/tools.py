# Central repository for all tools and tool-agents.
import requests
from bs4 import BeautifulSoup
from google.adk.agents import Agent
from google.adk.tools import google_search
from google.adk.tools.agent_tool import AgentTool # Import AgentTool for agent-as-a-tool pattern

# --- Custom Function Tools ---

def my_custom_tool(param: str) -> str:
    """A brief description of what this tool does."""
    # Tool logic goes here
    return f"Input was {param}"

def companies_office_direct_search(query: str) -> str:
    """Performs a direct search on the New Zealand Companies Office website for company information.

    Args:
        query: The search query (e.g., company name, director name).

    Returns:
        A string containing the search results, or an error message.
    """
    base_url = "https://www.companiesoffice.govt.nz/"
    search_url = f"{base_url}companies/search?q={requests.utils.quote(query)}"

    try:
        response = requests.get(search_url, timeout=10)
        response.raise_for_status()  # Raise an HTTPError for bad responses (4xx or 5xx)

        soup = BeautifulSoup(response.text, 'html.parser')

        # Attempt to find search results. This part is highly dependent on the website's HTML structure.
        # This is a simplified example and may need adjustment based on actual Companies Office HTML.
        results = soup.find_all('div', class_='search-result') # Example class, inspect actual site

        if not results:
            return f"No direct search results found on Companies Office for '{query}'."

        output = []
        for result in results:
            title = result.find('h3').text.strip() if result.find('h3') else 'N/A'
            link = result.find('a')['href'] if result.find('a') else 'N/A'
            description = result.find('p').text.strip() if result.find('p') else 'N/A'
            output.append(f"Title: {title}\nLink: {base_url}{link}\nDescription: {description}\n---")

        return "\n".join(output)

    except requests.exceptions.RequestException as e:
        return f"Error during Companies Office direct search: {e}"
    except Exception as e:
        return f"An unexpected error occurred during Companies Office direct search: {e}"

# --- Agent-as-a-Tool Definitions ---

SearchAgent = Agent(
    name="SearchAgent",
    model="gemini-2.0-flash",
    description="Performs a general Google web search.",
    tools=[google_search],
)

# New Agent for Companies Office Search (Google indexed)
CompaniesOfficeSearchAgent = Agent(
    name="CompaniesOfficeSearchAgent",
    model="gemini-2.0-flash",
    description="Performs a targeted search within the New Zealand Companies Office website (companiesoffice.govt.nz) using Google's index.",
    instruction="When using this tool, append 'site:companiesoffice.govt.nz' to your search query to ensure results are limited to the Companies Office website.",
    tools=[google_search], # Still uses google_search, but the prompt will guide its usage
)

# New Agent for Companies Office Direct Search
CompaniesOfficeDirectSearchAgent = Agent(
    name="CompaniesOfficeDirectSearchAgent",
    model="gemini-2.0-flash",
    description="Performs a direct search on the New Zealand Companies Office website for company information, such as registration details or director information.",
    tools=[companies_office_direct_search],
)
