import streamlit as st
import requests

API_BASE = "http://localhost:8000"

st.set_page_config(page_title="GenAI System", layout="wide")
st.title("RAG + SQL + Image QA")


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
    ["Text RAG", "SQL QA", "Image RAG"]
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

### Image RAG
elif mode == "Image RAG":
    st.subheader("Ask Image")

    uploaded_file = st.file_uploader(
        "Upload an image",
        type=["png", "jpg", "jpeg"]
    )

    question = st.text_input("Ask about the image")

    if uploaded_file and st.button("Ask Image") and question:
        with st.spinner("Analyzing image..."):
            response = requests.post(
                f"{API_BASE}/ask-image",
                params={"question": question},
                files={
                    "file": (
                        uploaded_file.name,
                        uploaded_file.getvalue(),
                        uploaded_file.type
                    )
                }
            )

        if response.status_code != 200:
            st.error(response.text)
        else:
            st.markdown("### Answer")
            st.write(response.json()["answer"])
