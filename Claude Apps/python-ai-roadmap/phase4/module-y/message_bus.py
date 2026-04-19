import asyncio
from dataclasses import dataclass, field
from typing import Optional
import time

@dataclass
class AgentMessage:
    sender: str
    recipient: str
    content: str
    message_type: str          # "task" | "result" | "error"
    timestamp: float = field(default_factory=time.time)
    metadata: dict = field(default_factory=dict)


class MessageBus:
    """Simple in-process message bus – one queue per agent."""

    def __init__(self):
        self._queues: dict[str, asyncio.Queue] = {}
        self.history: list[AgentMessage] = []

    def register(self, agent_name: str) -> None:
        if agent_name not in self._queues:
            self._queues[agent_name] = asyncio.Queue()

    async def send(self, message: AgentMessage) -> None:
        self.history.append(message)
        if message.recipient in self._queues:
            await self._queues[message.recipient].put(message)

    async def receive(self, agent_name: str, timeout: float = 30.0) -> Optional[AgentMessage]:
        try:
            return await asyncio.wait_for(self._queues[agent_name].get(), timeout=timeout)
        except asyncio.TimeoutError:
            return None
