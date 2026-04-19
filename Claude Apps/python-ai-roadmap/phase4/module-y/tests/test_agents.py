import asyncio
import sys
import pathlib
import pytest

sys.path.insert(0, str(pathlib.Path(__file__).parent.parent))

from message_bus import AgentMessage, MessageBus


# ── MessageBus ────────────────────────────────────────────────────────────────

def test_message_bus_register_and_send():
    bus = MessageBus()
    bus.register("agent_a")
    msg = AgentMessage("sender", "agent_a", "hello", "task")
    asyncio.run(bus.send(msg))
    assert bus._queues["agent_a"].qsize() == 1


def test_message_bus_history():
    bus = MessageBus()
    bus.register("agent_b")
    msg = AgentMessage("x", "agent_b", "content", "result")
    asyncio.run(bus.send(msg))
    assert len(bus.history) == 1
    assert bus.history[0].content == "content"


def test_message_bus_receive():
    bus = MessageBus()
    bus.register("agent_c")
    msg = AgentMessage("src", "agent_c", "data", "task")

    async def run():
        await bus.send(msg)
        received = await bus.receive("agent_c", timeout=1.0)
        return received

    result = asyncio.run(run())
    assert result is not None
    assert result.content == "data"


def test_message_bus_timeout():
    bus = MessageBus()
    bus.register("empty_agent")

    async def run():
        return await bus.receive("empty_agent", timeout=0.1)

    result = asyncio.run(run())
    assert result is None


# ── AgentMessage ──────────────────────────────────────────────────────────────

def test_agent_message_fields():
    msg = AgentMessage("alice", "bob", "test content", "task")
    assert msg.sender == "alice"
    assert msg.recipient == "bob"
    assert msg.content == "test content"
    assert msg.message_type == "task"
    assert msg.timestamp > 0


def test_agent_message_metadata_default():
    msg = AgentMessage("a", "b", "c", "result")
    assert msg.metadata == {}


def test_agent_message_custom_metadata():
    msg = AgentMessage("a", "b", "c", "task", metadata={"priority": "high"})
    assert msg.metadata["priority"] == "high"


# ── Message types ─────────────────────────────────────────────────────────────

@pytest.mark.parametrize("msg_type", ["task", "result", "error"])
def test_message_types(msg_type):
    msg = AgentMessage("s", "r", "body", msg_type)
    assert msg.message_type == msg_type


# ── Multiple queues ───────────────────────────────────────────────────────────

def test_multiple_agents_independent_queues():
    bus = MessageBus()
    for name in ["a1", "a2", "a3"]:
        bus.register(name)

    async def run():
        await bus.send(AgentMessage("src", "a1", "msg1", "task"))
        await bus.send(AgentMessage("src", "a2", "msg2", "task"))
        r1 = await bus.receive("a1", timeout=1.0)
        r2 = await bus.receive("a2", timeout=1.0)
        r3 = await bus.receive("a3", timeout=0.1)
        return r1, r2, r3

    r1, r2, r3 = asyncio.run(run())
    assert r1.content == "msg1"
    assert r2.content == "msg2"
    assert r3 is None


def test_bus_history_multiple_messages():
    bus = MessageBus()
    bus.register("agent")
    messages = [AgentMessage("s", "agent", f"msg{i}", "task") for i in range(5)]

    async def run():
        for m in messages:
            await bus.send(m)

    asyncio.run(run())
    assert len(bus.history) == 5


# ── Orchestrator (no API calls) ───────────────────────────────────────────────

def test_orchestrator_imports():
    from orchestrator import ResearchOrchestrator
    orch = ResearchOrchestrator()
    assert orch.searcher.name == "searcher"
    assert orch.analyst.name == "analyst"
    assert orch.writer.name == "writer"
    assert orch.checker.name == "checker"


def test_orchestrator_progress_callback():
    from orchestrator import ResearchOrchestrator
    logs = []
    orch = ResearchOrchestrator(progress_cb=logs.append)
    orch._log("test message")
    assert "test message" in logs


def test_agent_names():
    from agents.searcher import SearcherAgent
    from agents.analyst import AnalystAgent
    from agents.writer import WriterAgent
    from agents.checker import CheckerAgent
    assert SearcherAgent().name == "searcher"
    assert AnalystAgent().name == "analyst"
    assert WriterAgent().name == "writer"
    assert CheckerAgent().name == "checker"


def test_agent_message_ordering():
    bus = MessageBus()
    bus.register("ordered")

    async def run():
        for i in range(3):
            await bus.send(AgentMessage("s", "ordered", f"item{i}", "task"))
        results = []
        for _ in range(3):
            r = await bus.receive("ordered", timeout=1.0)
            results.append(r.content)
        return results

    results = asyncio.run(run())
    assert results == ["item0", "item1", "item2"]
