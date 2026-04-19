import asyncio
from message_bus import AgentMessage, MessageBus
from agents.searcher import SearcherAgent
from agents.analyst import AnalystAgent
from agents.writer import WriterAgent
from agents.checker import CheckerAgent
from typing import Callable, Optional


class ResearchOrchestrator:
    """
    Coordinates 4 specialist agents to produce a verified research report.
    searcher + analyst run in parallel, then writer, then checker.
    """

    def __init__(self, progress_cb: Optional[Callable[[str], None]] = None):
        self.bus = MessageBus()
        self.searcher = SearcherAgent()
        self.analyst = AnalystAgent()
        self.writer = WriterAgent()
        self.checker = CheckerAgent()
        self._progress = progress_cb or (lambda msg: print(f"[orchestrator] {msg}"))

    def _log(self, msg: str) -> None:
        self._progress(msg)

    async def _run_agent(self, agent, content: str, max_retries: int = 2) -> str:
        msg = AgentMessage(
            sender="orchestrator",
            recipient=agent.name,
            content=content,
            message_type="task",
        )
        for attempt in range(1, max_retries + 1):
            try:
                result = await agent.handle(msg)
                if result.message_type == "error":
                    raise RuntimeError(result.content)
                return result.content
            except Exception as exc:
                self._log(f"  ⚠ {agent.name} attempt {attempt} failed: {exc}")
                if attempt == max_retries:
                    return f"[{agent.name} unavailable after {max_retries} attempts: {exc}]"
                await asyncio.sleep(1)

    async def research(self, question: str) -> dict:
        """
        Returns a dict with keys: search, analysis, report, verified_report, question.
        Progress updates via self._progress callback.
        """
        self._log("🔍 Starting parallel search + analysis…")

        # Phase 1 – parallel: searcher and analyst both get the raw question
        search_task = self._run_agent(self.searcher, question)
        # analyst gets the question too — it will analyse it independently first
        analyst_task = self._run_agent(
            self.analyst,
            f"Research question: {question}\n\nAnalyse what we know about this topic "
            "and what the key sub-questions are.",
        )
        search_result, analysis_seed = await asyncio.gather(search_task, analyst_task)

        self._log("📊 Analyst refining with search results…")
        combined = f"RESEARCH QUESTION:\n{question}\n\nSEARCH FINDINGS:\n{search_result}\n\nINITIAL ANALYSIS:\n{analysis_seed}"
        analysis = await self._run_agent(self.analyst, combined)

        self._log("✍️  Writer drafting report…")
        draft = await self._run_agent(
            self.writer,
            f"QUESTION:\n{question}\n\nANALYSIS:\n{analysis}",
        )

        self._log("✅ Fact-checker reviewing…")
        verified = await self._run_agent(self.checker, draft)

        self._log("🎉 Research complete!")
        return {
            "question": question,
            "search": search_result,
            "analysis": analysis,
            "report": draft,
            "verified_report": verified,
        }
