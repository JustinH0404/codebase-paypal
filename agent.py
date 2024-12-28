from crewai.agent import Agent
from tools import SlackRetrievalTool

# Instantiate the tool
slack_tool = SlackRetrievalTool(token="your-slack-token")

# Create the agent and register the tool
agent = Agent(tools=[slack_tool])
