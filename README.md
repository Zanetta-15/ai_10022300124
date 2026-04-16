# Academic City RAG Chatbot

**Name:** Zanetta Crentsil
**Index Number:** 10022300124  
**Course:** CS4241 - Introduction to Artificial Intelligence  
**Lecturer:** Godwin N. Danso  
**Date:** April 2026

---

## Project Overview
A Retrieval-Augmented Generation (RAG) chatbot built for Academic City University. 
It answers questions about Ghana's 2025 Budget Statement and Ghana Election Results 
using only information from the provided documents.

## Live Demo
🔗 https://ai10022300124-mpuascqqdmcgecyb6xkldt.streamlit.app

## GitHub Repository
🔗 https://github.com/Zanetta-15/ai_10022300124

---

## Architecture
User Query → Query Expansion → ChromaDB Retrieval → Context Selection → Prompt Builder → LLM → Response

## Tech Stack
- Embeddings: ChromaDB (all-MiniLM-L6-v2)
- Vector Store: ChromaDB with cosine similarity
- LLM (local): Ollama llama3.2:1b
- LLM (cloud): Groq llama-3.1-8b-instant
- UI: Streamlit
- Data: PyMuPDF (PDF), Pandas (CSV)

---

## Design Decisions

### Chunking Strategy
- PDF: 512 token chunks with 64 token overlap
- Justification: Budget documents have dense cross-references so overlap prevents losing context at section boundaries
- CSV: One row per chunk converted to natural language sentences
- Justification: Makes constituency/region names searchable by the embedding model

### Retrieval
- Query expansion generates 2-4 variants of each query
- Top-k=5 retrieval with cosine similarity re-ranking
- Hybrid keyword detection routes queries to budget or election data

### Prompt Engineering
- 3 templates tested: default, strict, conversational
- Default template performed best overall
- Hallucination control: "Use ONLY the context below"

---

## How to Run Locally

### Prerequisites
- Python 3.11+
- Ollama installed with llama3.2:1b model

### Setup
```bash
git clone https://github.com/Zanetta-15/ai_10022300124
cd ai_10022300124
python3 -m venv venv
source venv/bin/activate
pip install -r requirements.txt
python3 ingest.py
streamlit run app.py
```

---

## Files
- `ingest.py` — Data cleaning, chunking, embedding and indexing
- `retriever.py` — Query expansion, top-k retrieval, re-ranking
- `prompt.py` — Prompt templates and context window management
- `pipeline.py` — Full RAG pipeline with logging (local)
- `pipeline_cloud.py` — Cloud pipeline using Groq API
- `app.py` — Streamlit UI (local, uses Ollama)
- `app_cloud.py` — Streamlit UI (cloud deployment)

---

## Limitations
- Free LLM models have rate limits on cloud deployment
- Budget PDF contains many numerical tables which reduce retrieval precision
- Election dataset contains regional presidential results only, not constituency data