from agents.base import BaseAgent
from message_bus import AgentMessage


class WriterAgent(BaseAgent):
    def __init__(self):
        super().__init__(
            name="writer",
            system_prompt=(
                "You are a professional report writer. Given research analysis, "
                "produce a well-structured report with: Executive Summary, Key Findings "
                "(bullet points), Detailed Analysis (paragraphs), and Conclusions. "
                "Write clearly for a non-specialist audience. Use markdown formatting."
            ),
        )

    async def handle(self, message: AgentMessage) -> AgentMessage:
        result = await self.call_claude(
            f"Write a structured research report from this analysis:\n\n{message.content}",
            max_tokens=2000,
        )
        return AgentMessage(
            sender=self.name,
            recipient=message.sender,
            content=result,
            message_type="result",
        )
