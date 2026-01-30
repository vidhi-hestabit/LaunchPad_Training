import streamlit as st
import asyncio
from main import run_pipeline

st.set_page_config(page_title="DAY-2", layout="wide")

st.title("Autonomous Multi-Agent System")

query = st.text_area(
    "Enter your query",
    placeholder=""
)

run_btn = st.button("Run Agents")

log_box = st.empty()
logs = []


def logger(msg):
    logs.append(msg)
    log_box.markdown(
        "### Execution Log\n" + "\n".join(f"- {l}" for l in logs)
    )


if run_btn and query.strip():
    with st.spinner("Agents are thinking..."):
        result = asyncio.run(run_pipeline(query, logger))

    st.divider()

    st.subheader("Final Answer")
    st.write(result["answer"])

    st.subheader("Validation")
    st.success(result["verdict"])
    st.caption(result["reason"])
