import streamlit as st
from llm.ollama_llm import OllamaLLM
from agents.research_agent import ResearchAgent
from agents.summarizer_agent import SummarizerAgent
from agents.answer_agent import AnswerAgent
from orchestrator import Orchestrator


llm = OllamaLLM()
research_agent = ResearchAgent(llm)
summarizer_agent = SummarizerAgent(llm)
answer_agent = AnswerAgent(llm)

orchestrator = Orchestrator(
    research_agent,
    summarizer_agent,
    answer_agent
)

st.title("Manual AutoGen Multi-Agent Demo")
st.write("Ask a question and get Research → Summary → Answer")

user_query = st.text_input("Enter your query:")

if st.button("Submit") and user_query:
    result = orchestrator.run(user_query)

    st.subheader("Research Agent Output")
    st.write(result["research"])

    st.subheader("Summarizer Agent Output")
    st.write(result["summary"])

    st.subheader("Answer Agent Output")
    st.write(result["answer"])
