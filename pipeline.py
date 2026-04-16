# pipeline.py
# Name: Zanetta Crentsil
# Index Number: 10022300124

import os
import json
import datetime
import requests
from dotenv import load_dotenv
from retriever import retrieve
from prompt import build_prompt

load_dotenv()


# ── LLM call via Ollama (local, free) ────────────────────────────────────────

def generate(prompt):
    response = requests.post(
        "http://localhost:11434/api/generate",
        json={
            "model": "llama3.2:1b",
            "prompt": prompt,
            "stream": False
        },
        timeout=300
    )
    result = response.json()
    if "response" not in result:
        raise Exception(f"Ollama error: {result}")
    return result["response"]


# ── logging ───────────────────────────────────────────────────────────────────

def log_pipeline(query, expanded_queries, chunks, prompt, response, template):
    os.makedirs("logs", exist_ok=True)
    log_entry = {
        "timestamp": datetime.datetime.now().isoformat(),
        "query": query,
        "template": template,
        "expanded_queries": expanded_queries,
        "retrieved_chunks": [
            {"id": c["id"], "score": c["score"], "source": c["source"]}
            for c in chunks
        ],
        "prompt_word_count": len(prompt.split()),
        "response": response
    }
    log_path = "logs/pipeline_log.json"
    logs = []
    if os.path.exists(log_path):
        with open(log_path, "r") as f:
            try:
                logs = json.load(f)
            except:
                logs = []
    logs.append(log_entry)
    with open(log_path, "w") as f:
        json.dump(logs, f, indent=2)
    print(f"[PIPELINE] Log saved to {log_path}")


# ── main pipeline ─────────────────────────────────────────────────────────────

def run_pipeline(query, k=5, template="default"):
    print("\n" + "="*60)
    print(f"[PIPELINE] Query: {query}")
    print("="*60)

    # Stage 1: Retrieve
    print("\n[STAGE 1] Retrieving chunks...")
    chunks = retrieve(query, k=k)

    # Stage 2: Build prompt
    print("\n[STAGE 2] Building prompt...")
    prompt = build_prompt(query, chunks, template=template)

    # Stage 3: Generate
    print("\n[STAGE 3] Sending to Ollama (llama3.2:1b)...")
    print(f"[PIPELINE] Prompt sent:\n{prompt[:200]}...\n")

    answer = generate(prompt)

    print(f"[PIPELINE] Response received:\n{answer}")

    # Stage 4: Log everything
    print("\n[STAGE 4] Logging...")
    from retriever import expand_query
    expanded = expand_query(query)
    log_pipeline(query, expanded, chunks, prompt, answer, template)

    return {
        "query": query,
        "chunks": chunks,
        "prompt": prompt,
        "response": answer
    }


# ── RAG vs pure LLM comparison (Part E) ──────────────────────────────────────

def compare_rag_vs_llm(query):
    print("\n" + "="*60)
    print(f"[COMPARISON] RAG vs Pure LLM")
    print(f"[COMPARISON] Query: {query}")
    print("="*60)

    # RAG response
    print("\n--- RAG RESPONSE ---")
    rag_result = run_pipeline(query)
    rag_answer = rag_result["response"]

    # Pure LLM response (no retrieval)
    print("\n--- PURE LLM RESPONSE (no retrieval) ---")
    bare_prompt = f"Answer this question about Ghana: {query}"
    llm_answer = generate(bare_prompt)
    print(llm_answer)

    # Save comparison
    os.makedirs("logs", exist_ok=True)
    with open("logs/rag_vs_llm.txt", "a") as f:
        f.write(f"\n{'='*60}\n")
        f.write(f"Query: {query}\n")
        f.write(f"Timestamp: {datetime.datetime.now().isoformat()}\n")
        f.write(f"\nRAG Answer:\n{rag_answer}\n")
        f.write(f"\nPure LLM Answer:\n{llm_answer}\n")

    print("\n[COMPARISON] Saved to logs/rag_vs_llm.txt")
    return rag_answer, llm_answer


# ── run ───────────────────────────────────────────────────────────────────────

if __name__ == "__main__":
    run_pipeline("What is the total revenue target in the 2025 budget?")
    print("\n\n")
    compare_rag_vs_llm("What will Ghana's budget be in 2030?")