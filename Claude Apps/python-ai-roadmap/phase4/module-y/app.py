import streamlit as st
import asyncio
import sys
import pathlib

# Make sure local modules are importable
sys.path.insert(0, str(pathlib.Path(__file__).parent))

from orchestrator import ResearchOrchestrator

st.set_page_config(page_title="Module Y — Research Crew", page_icon="🤖", layout="wide")

st.title("🤖 Module Y — Autonomous Research Crew")
st.caption("Multi-agent system: Searcher → Analyst → Writer → Fact-checker")

with st.sidebar:
    st.header("How it works")
    st.markdown("""
1. **Searcher** + **Analyst** run in parallel  
2. **Analyst** refines with search results  
3. **Writer** drafts the report  
4. **Fact-checker** annotates the draft  
    """)
    st.divider()
    st.info("Each agent is a specialised Claude call with a focused system prompt.")

question = st.text_area(
    "Research question",
    placeholder="e.g. What are the main causes and consequences of the 2008 financial crisis?",
    height=80,
)

if st.button("🚀 Run Research Crew", type="primary", disabled=not question.strip()):
    log_box = st.empty()
    logs: list[str] = []

    def update_log(msg: str):
        logs.append(msg)
        log_box.markdown("\n".join(f"- {l}" for l in logs))

    with st.spinner("Agents working…"):
        result = asyncio.run(
            ResearchOrchestrator(progress_cb=update_log).research(question.strip())
        )

    st.success("Done!")

    tab1, tab2, tab3, tab4 = st.tabs(
        ["📋 Verified Report", "✍️ Draft", "📊 Analysis", "🔍 Search"]
    )
    with tab1:
        st.markdown(result["verified_report"])
    with tab2:
        st.markdown(result["report"])
    with tab3:
        st.markdown(result["analysis"])
    with tab4:
        st.markdown(result["search"])
