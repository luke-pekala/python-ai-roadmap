from agents.base import BaseAgent
from message_bus import AgentMessage


class AnalystAgent(BaseAgent):
    def __init__(self):
        super().__init__(
            name="analyst",
            system_prompt=(
                "You are a critical analyst. You receive raw research and identify: "
                "1) The 3-5 most important insights. "
                "2) Gaps or conflicting evidence. "
                "3) A confidence rating (low/medium/high) for each claim. "
                "Be concise and structured. Output in plain text with clear sections."
            ),
        )

    async def handle(self, message: AgentMessage) -> AgentMessage:
        result = await self.call_claude(
            f"Analyse this research and extract key insights:\n\n{message.content}",
            max_tokens=1000,
        )
        return AgentMessage(
            sender=self.name,
            recipient=message.sender,
            content=result,
            message_type="result",
        )
