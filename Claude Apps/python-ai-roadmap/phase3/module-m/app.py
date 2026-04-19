"""Streamlit dashboard for Module M — Smart Summariser."""
import json
import streamlit as st
from client import summarise

st.set_page_config(page_title="Smart Summariser · Module M", layout="wide")
st.title("📄 Smart Summariser")
st.caption("Module M — Anthropic API · Phase 3")

with st.sidebar:
    st.header("Options")
    fmt = st.selectbox("Output format", ["plain", "markdown", "json"])
    st.markdown("---")
    st.markdown(
        "Add your API key to `.env`:\n```\nANTHROPIC_API_KEY=sk-ant-...\n```"
    )

text_input = st.text_area(
    "Paste text to summarise",
    height=300,
    placeholder="Paste any article, document, or notes here...",
)

col1, col2 = st.columns([1, 4])
with col1:
    run = st.button("Summarise ✨", use_container_width=True)

if run:
    if not text_input.strip():
        st.warning("Please paste some text first.")
    else:
        with st.spinner("Asking Claude..."):
            try:
                result = summarise(text_input)
            except EnvironmentError as e:
                st.error(str(e))
                st.stop()

        st.success("Done!")

        if fmt == "json":
            st.code(json.dumps(result, indent=2), language="json")
        elif fmt == "markdown":
            st.markdown(f"### Summary\n{result['summary']}")
            if result["key_points"]:
                st.markdown("### Key Points")
                for kp in result["key_points"]:
                    st.markdown(f"- {kp}")
            if result["action_items"]:
                st.markdown("### Action Items")
                for ai in result["action_items"]:
                    st.markdown(f"- [ ] {ai}")
            st.markdown(f"**TL;DR:** {result['tldr']}")
        else:
            col_a, col_b = st.columns(2)
            with col_a:
                st.subheader("Summary")
                st.write(result["summary"])
                st.subheader("TL;DR")
                st.info(result["tldr"])
            with col_b:
                if result["key_points"]:
                    st.subheader("Key Points")
                    for kp in result["key_points"]:
                        st.markdown(f"- {kp}")
                if result["action_items"]:
                    st.subheader("Action Items")
                    for ai in result["action_items"]:
                        st.checkbox(ai, key=ai)
