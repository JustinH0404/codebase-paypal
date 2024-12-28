from crewai import Agent, Task
from dotenv import load_dotenv
import os
from tools import SlackMessageRetrieverTool

# Load environment variables
load_dotenv()
# SLACK_TOKEN = os.getenv('SLACK_TOKEN')
SLACK_TOKEN = "fake-token"

# Initialize the tool
slack_tool = SlackMessageRetrieverTool(slack_token=SLACK_TOKEN)

# Create an agent that uses the tool
slack_agent = Agent(
    role='Slack Message Retriever',
    goal='Retrieve and analyze Slack messages',
    backstory='I help retrieve and analyze messages from Slack channels',
    tools=[slack_tool]
)

# Create a task for the agent
task = Task(
    description='Retrieve the last 10 messages from channel C123ABC456',
    agent=slack_agent
)