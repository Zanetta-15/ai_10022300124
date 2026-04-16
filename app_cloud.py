# app_cloud.py
# Name: Zanetta Crentsil
# Index Number: 10022300124

import streamlit as st
import os
from pipeline_cloud import run_pipeline

st.set_page_config(page_title="ACity RAG Chatbot", page_icon="🎓", layout="wide")

st.title("🎓 Academic City RAG Chatbot")
st.markdown("Ask questions about Ghana's **2025 Budget** or **Election Results**")

with st.sidebar:
    st.header("Settings")
    template = st.selectbox("Prompt Template", ["default", "strict", "conversational"])
    k = st.slider("Number of chunks to retrieve", 1, 10, 5)
    st.markdown("---")
    st.markdown("**Index:** 10022300124")
    st.markdown("**Model:** gemma-3-4b (OpenRouter)")

if "messages" not in st.session_state:
    st.session_state.messages = []

for message in st.session_state.messages:
    with st.chat_message(message["role"]):
        st.markdown(message["content"])

if query := st.chat_input("Ask about the budget or election results..."):
    st.session_state.messages.append({"role": "user", "content": query})
    with st.chat_message("user"):
        st.markdown(query)

    with st.chat_message("assistant"):
        with st.spinner("Searching documents and generating answer..."):
            result = run_pipeline(query, k=k, template=template)

        st.markdown(result["response"])

        with st.expander("📄 Retrieved Chunks"):
            for i, chunk in enumerate(result["chunks"]):
                st.markdown(f"**Chunk {i+1}** | Score: `{chunk['score']}` | Source: `{chunk['source']}`")
                st.text(chunk["text"][:300] + "...")
                st.markdown("---")

        with st.expander("📊 Similarity Scores"):
            for chunk in result["chunks"]:
                st.progress(chunk["score"], text=f"{chunk['id']} — {chunk['score']}")

    st.session_state.messages.append({"role": "assistant", "content": result["response"]})