import streamlit as st
import asyncio
from datetime import datetime

from main import run_nexus

st.set_page_config(
    page_title="Nexus AI",
    layout="wide",
)

st.title("Nexus AI — Autonomous Multi-Agent System")


st.sidebar.header("Configuration")

enable_reflection = st.sidebar.checkbox("Enable Reflection (Critic)", value=True)
enable_optimization = st.sidebar.checkbox("Enable Optimization", value=True)
max_iterations = st.sidebar.number_input(
    "Max Iterations",
    min_value=1,
    max_value=10,
    value=3,
    step=1
)

query = st.text_area(
    "Enter your query",
    height=120,
    placeholder="Example: Build a scalable multi-agent architecture for data analysis"
)

run_btn = st.button("Run Nexus AI")

if run_btn and query.strip():
    with st.spinner("Nexus AI is thinking..."):
        start = datetime.now()

        try:
            result = asyncio.run(
                run_nexus(
                    query=query,
                    enable_reflection=enable_reflection,
                    enable_optimization=enable_optimization,
                    max_iterations=max_iterations,
                )
            )

            duration = (datetime.now() - start).total_seconds()

            st.success(f"Completed in {duration:.2f}s")

            st.subheader("Final Answer")
            st.markdown(result["answer"])

            st.subheader("Validation")
            col1, col2, col3 = st.columns(3)
            col1.metric("Verdict", result["verdict"])
            col2.metric("Score", result["score"])
            col3.metric("Tasks", f'{result["tasks_completed"]}/{result["total_tasks"]}')

            if result.get("issues"):
                st.subheader("Issues")
                for issue in result["issues"]:
                    st.write(f"- {issue}")

            if result.get("suggestions"):
                st.subheader("Suggestions")
                for s in result["suggestions"]:
                    st.write(f"- {s}")

            with st.expander("System Details"):
                st.json({
                    "execution_time": result["execution_time"],
                    "memory_stats": result["memory_stats"],
                })

        except Exception as e:
            st.error(f"Execution failed: {str(e)}")

else:
    st.info("Enter a query and click **Run Nexus AI**.")
