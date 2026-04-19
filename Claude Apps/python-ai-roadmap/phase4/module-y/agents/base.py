from dotenv import load_dotenv 
load_dotenv() 
from abc import ABC, abstractmethod
from message_bus import AgentMessage
import anthropic
import os


class BaseAgent(ABC):
    def __init__(self, name: str, system_prompt: str):
        self.name = name
        self.system_prompt = system_prompt
        self.client = anthropic.Anthropic(api_key=os.environ["ANTHROPIC_API_KEY"])

    @abstractmethod
    async def handle(self, message: AgentMessage) -> AgentMessage:
        pass

    async def call_claude(self, prompt: str, max_tokens: int = 1024) -> str:
        import asyncio
        loop = asyncio.get_event_loop()
        response = await loop.run_in_executor(
            None,
            lambda: self.client.messages.create(
                model="claude-sonnet-4-5",
                max_tokens=max_tokens,
                system=self.system_prompt,
                messages=[{"role": "user", "content": prompt}],
            )
        )
        return response.content[0].text
