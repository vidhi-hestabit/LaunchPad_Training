import asyncio
import streamlit as st
from orchestrator.planner import Planner


def run_planner_sync(query: str):
    loop = asyncio.new_event_loop()
    asyncio.set_event_loop(loop)
    planner = Planner()
    final_answer, tree = loop.run_until_complete(planner.run(query))
    loop.close()
    return final_answer, tree


st.set_page_config(
    page_title="AutoGen Multi-Agent System",
    layout="wide",
)

st.title("AutoGen Multi-Agent Orchestrator")

query = st.text_area(
    "Enter your query:",
    height=150,
    placeholder="Ask something complex that can be broken into sub-tasks...",
)

run_button = st.button("Run Agents")

if run_button:
    if not query.strip():
        st.warning("Please enter a query.")
    else:
        with st.spinner("Running multi-agent workflow..."):
            try:
                final_answer, execution_tree = run_planner_sync(query)

                st.success("Done!")

                st.subheader("Final Answer")
                st.markdown(final_answer)

                st.subheader("Execution Tree")

                for node_id, node_data in execution_tree.items():
                    with st.expander(f"Node: {node_id}"):

                        st.write("**Task:**", node_data.get("task", ""))
                        st.write("**Dependencies:**", node_data["deps"])

                        preview = (
                            node_data["output"][:300] + "..."
                            if len(node_data["output"]) > 300
                            else node_data["output"]
                        )

                        st.write("**Output (preview):**")
                        st.markdown(preview)

            except Exception as e:
                st.error(f"Error: {str(e)}")
