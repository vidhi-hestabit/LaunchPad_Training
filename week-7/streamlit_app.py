import streamlit as st
import requests
from deployment import app
import threading
import time


def run_api():
    import uvicorn
    uvicorn.run(app, host="0.0.0.0", port=8000)

# Start FastAPI in a daemon thread
threading.Thread(target=run_api, daemon=True).start()

# Wait a second to ensure the backend is ready
time.sleep(1)



API_BASE = "http://localhost:8000"

st.set_page_config(page_title="GenAI System", layout="wide")
st.title("RAG + SQL QA")


def safe_post(url, **kwargs):
    try:
        r = requests.post(url, timeout=120, **kwargs)
    except Exception as e:
        st.error(f"Connection error: {e}")
        st.stop()

    if r.status_code != 200:
        st.error(f"API Error {r.status_code}")
        try:
            st.json(r.json())
        except Exception:
            st.text(r.text)
        st.stop()

    try:
        return r.json()
    except ValueError:
        st.error("Response is not valid JSON")
        st.text(r.text)
        st.stop()


mode = st.sidebar.selectbox(
    "Choose Mode",
    ["Text RAG", "SQL QA"]
)

# ---------------- TEXT RAG ----------------
if mode == "Text RAG":
    st.subheader("Ask Documents")

    question = st.text_input("Ask a question")

    if st.button("Ask") and question:
        with st.spinner("Thinking..."):
            response = safe_post(
                f"{API_BASE}/ask",
                params={"question": question}
            )

        st.markdown("### Answer")
        st.write(response["answer"])

        st.markdown("### Evaluation")
        st.json(response["evaluation"])

# SQL QA
elif mode == "SQL QA":
    st.subheader("Ask Database")

    question = st.text_input("Ask a SQL question")

    if st.button("Run Query") and question:
        with st.spinner("Querying database..."):
            response = safe_post(
                f"{API_BASE}/ask-sql",
                params={"question": question}
            )


        st.markdown("### Generated SQL")
        st.code(response["sql"], language="sql")

        st.markdown("### Result Table")
        if response["rows"]:
            st.dataframe(
        [dict(zip(response["columns"], row)) for row in response["rows"]]
    )
        else:
            st.write("No rows returned.")

        st.markdown("### Answer")
        st.write(response["answer"])

