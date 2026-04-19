from agents.base import BaseAgent
from message_bus import AgentMessage


class SearcherAgent(BaseAgent):
    def __init__(self):
        super().__init__(
            name="searcher",
            system_prompt=(
                "You are a research specialist. Given a question, produce a thorough "
                "summary of what is publicly known about it: key facts, major sources, "
                "recent developments, and open questions. Be specific and cite types of "
                "sources (academic papers, news, official reports). Output plain text."
            ),
        )

    async def handle(self, message: AgentMessage) -> AgentMessage:
        result = await self.call_claude(
            f"Research this question thoroughly:\n\n{message.content}",
            max_tokens=1500,
        )
        return AgentMessage(
            sender=self.name,
            recipient=message.sender,
            content=result,
            message_type="result",
        )
