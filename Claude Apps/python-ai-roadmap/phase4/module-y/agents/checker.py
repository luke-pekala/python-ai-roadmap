from agents.base import BaseAgent
from message_bus import AgentMessage


class CheckerAgent(BaseAgent):
    def __init__(self):
        super().__init__(
            name="checker",
            system_prompt=(
                "You are a fact-checker and editor. Review the report for: "
                "1) Unsupported or dubious claims — flag them clearly. "
                "2) Internal contradictions. "
                "3) Missing caveats on uncertain claims. "
                "Return the FULL report with your corrections/annotations inline "
                "using [FACT-CHECK: note] markers. Keep all original content intact."
            ),
        )

    async def handle(self, message: AgentMessage) -> AgentMessage:
        result = await self.call_claude(
            f"Fact-check and annotate this report:\n\n{message.content}",
            max_tokens=2500,
        )
        return AgentMessage(
            sender=self.name,
            recipient=message.sender,
            content=result,
            message_type="result",
        )
