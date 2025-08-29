\# Interacting with Your Deployed Agent via Command Line  
This guide documents the \`interact\_agent.py\` script, which allows you to send queries to your deployed Agent Engine agent directly from your command line.  
\#\# 1\. The \`interact\_agent.py\` Script  
This Python script was created to facilitate command-line interaction with your agent. It handles session creation, sending queries, and printing the agent's response.  
\`\`\`python  
import vertexai  
from vertexai import agent\_engines  
from google.genai import types \# For multimodal queries, if needed  
import sys  
\# \--- Configuration \---  
PROJECT\_ID \= "609773120808" \# Your Google Cloud Project ID  
LOCATION \= "us-central1" \# Your Google Cloud Location  
\# This is the full resource name obtained from your deployment output  
AGENT\_RESOURCE\_NAME \= "projects/609773120808/locations/us-central1/reasoningEngines/7012953442792505344"  
\# \--- Initialize Vertex AI \---  
vertexai.init(project=PROJECT\_ID, location=LOCATION)  
\# \--- Get a reference to your deployed agent \---  
remote\_app \= agent\_engines.get(AGENT\_RESOURCE\_NAME)  
\# \--- Interact with the agent \---  
\# Get query from command line arguments  
if len(sys.argv) \< 2:  
    print("Usage: python interact\_agent.py \\"Your query here\\"")  
    sys.exit(1)  
query\_message \= sys.argv\[1\]  
\# 1\. Create a session (or reuse an existing one if you manage session IDs)  
\# For simplicity, we'll create a new session for each command-line interaction.  
\# For multi-turn conversations, you'd need to persist and reuse the session\_id.  
print("Creating a new session for this query...")  
remote\_session \= remote\_app.create\_session(user\_id="cli\_user")  
print(f"Session ID: {remote\_session\['id'\]}")  
\# 2\. Send the query  
print(f"\\nSending query: \\"{query\_message}\\"\\n")  
full\_response\_text \= ""  
for event in remote\_app.stream\_query(  
    user\_id="cli\_user",  
    session\_id=remote\_session\['id'\],  
    message=query\_message,  
):  
    if 'content' in event and 'parts' in event\['content'\]:  
        for part in event\['content'\]\['parts'\]:  
            if 'text' in part:  
                full\_response\_text \+= part\['text'\]  
print("Agent Response:")  
print(full\_response\_text)  
print("\\nInteraction complete.")  
\`\`\`  
\#\#\# Key Configuration Variables:  
\*   \`PROJECT\_ID\`: Your Google Cloud Project ID.  
\*   \`LOCATION\`: The Google Cloud region where your agent is deployed (e.g., \`us-central1\`).  
\*   \`AGENT\_RESOURCE\_NAME\`: The unique identifier for your deployed agent on Agent Engine. This was provided in the deployment output (e.g., \`projects/609773120808/locations/us-central1/reasoningEngines/7012953442792505344\`).  
\#\# 2\. Prerequisites  
Before using the script, ensure you have:  
\*   **\*\***\`**google-cloud-aiplatform**\` **installed:**\*\* If you haven't already, install it in your Python environment:  
    \`\`\`bash  
    pip install google-cloud-aiplatform  
    \`\`\`  
\*   \*\***Authenticated** \`**gcloud**\` **Application Default Credentials:**\*\* Your script needs to authenticate with Google Cloud. If you encounter authentication errors, run the following command and follow the prompts:  
    \`\`\`bash  
    gcloud auth application-default login  
    \`\`\`  
\#\# 3\. How to Use the \`interact\_agent.py\` Script  
Follow these steps to send test questions to your deployed agent:  
\*\***Step 1: Open Your Terminal**\*\*  
You can be in any directory in your terminal.  
\*\***Step 2: Run the Script with Your Query**\*\*  
Use the following command format. \*\***Always enclose your question in double quotes (**\`**"**\`**)**\*\* to ensure it's passed as a single argument.  
\`\`\`bash  
/Users/joeward/agent-test3/tradie\_ai/.venv/bin/python /Users/joeward/agent-test3/tradie\_ai/interact\_agent.py "Your test question here"  
\`\`\`  
\*\***Example Test Questions:**\*\*  
\*   \*\***To test the** \`**quoting\_agent**\` **(business operations):**\*\*  
    \`\`\`bash  
    /Users/joeward/agent-test3/tradie\_ai/.venv/bin/python /Users/joeward/agent-test3/tradie\_ai/interact\_agent.py "Can you give me a quote for 50 square meters of tiling?"  
    \`\`\`  
\*   \*\***To test the** \`**knowledge\_agent**\` **(technical questions/search):**\*\*  
    \`\`\`bash  
    /Users/joeward/agent-test3/tradie\_ai/.venv/bin/python /Users/joeward/agent-test3/tradie\_ai/interact\_agent.py "What are the latest building regulations for fire safety in commercial buildings?"  
    \`\`\`  
\*   \*\***A general knowledge question (expected to be declined by this agent):**\*\*  
    \`\`\`bash  
    /Users/joeward/agent-test3/tradie\_ai/.venv/bin/python /Users/joeward/agent-test3/tradie\_ai/interact\_agent.py "Who won the last football World Cup?"  
    \`\`\`  
\#\# 4\. Troubleshooting  
\*   **\*\***\`**python: command not found**\` **or similar errors:**\*\*  
    This usually means the \`python\` executable is not in your system's PATH, or you're not using the correct Python environment. The command provided above uses the full path to the Python executable within your project's virtual environment (\`.venv\`), which should resolve this.  
\*   \*\***Authentication Errors (**\`**Reauthentication is needed**\`**):**\*\*  
    As mentioned in the prerequisites, your Google Cloud credentials might have expired. Run \`gcloud auth application-default login\` to refresh them.  
\*   \*\***Agent Response is unexpected:**\*\*  
    Review your agent's \`instruction\` prompt and the \`description\` of its tools and sub-agents. Ensure they clearly guide the agent to handle the types of queries you are sending. You can also check the detailed logs in the \[Google Cloud Console\](https://console.cloud.google.com/logs/query) for your Agent Engine instance to understand the agent's reasoning process.  
