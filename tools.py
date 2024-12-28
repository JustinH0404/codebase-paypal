from crewai.tools import BaseTool
from slack_sdk import WebClient
from pydantic import Field, PrivateAttr

class SlackRetrievalTool(BaseTool):
    name: str = "SlackMessageRetriever"
    description: str = "A tool to retrieve Slack messages by channel ID and timestamp."
    client: WebClient = PrivateAttr()  # Exclude from Pydantic validation and schema

    def __init__(self, token: str):
        super().__init__()
        self._client = WebClient(token=token)

    def _run(self, channel_id: str, message_ts: str) -> str:
        """
        Retrieves a Slack message by channel ID and timestamp.

        Args:
            channel_id (str): The Slack channel ID.
            message_ts (str): The timestamp of the message.

        Returns:
            str: The content of the message or an error message.
        """
        try:
            response = self._client.conversations_history(
                channel=channel_id,
                inclusive=True,
                oldest=message_ts,
                latest=message_ts,
                limit=1,
            )
            messages = response.get("messages", [])
            if messages:
                return messages[0]["text"]
            return "No message found for the given timestamp."
        except Exception as e:
            return f"Error retrieving message: {str(e)}"
