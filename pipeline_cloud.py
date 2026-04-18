# pipeline_cloud.py
# Name: Zanetta Crentsil
# Index Number: 10022300124

import os
import requests
from retriever import retrieve
from prompt import build_prompt

GROQ_KEY = "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"

def generate(prompt):
    words = prompt.split()
    if len(words) > 500:
        prompt = " ".join(words[:500])

    response = requests.post(
        "https://api.groq.com/openai/v1/chat/completions",
        headers={
            "Authorization": f"Bearer {GROQ_KEY}",
            "Content-Type": "application/json"
        },
        json={
            "model": "mixtral-8x7b-32768",
            "messages": [{"role": "user", "content": prompt}],
            "max_tokens": 200
        },
        timeout=30
    )
    result = response.json()
    if "choices" not in result:
        raise Exception(f"Groq error: {result}")
    return result["choices"][0]["message"]["content"]


def is_election_query(query):
    q = query.lower()
    return any(w in q for w in [
        "election", "vote", "won", "winner", "candidate",
        "party", "npp", "ndc", "region", "2020", "2016",
        "2012", "2008", "2004", "2000", "1996", "president"
    ])


def run_pipeline(query, k=5, template="default"):
    chunks = retrieve(query, k=k)

    if is_election_query(query):
        election_chunks = [c for c in chunks if c["source"] == "election_csv"]
        budget_chunks = [c for c in chunks if c["source"] == "budget_pdf"]
        chunks = election_chunks + budget_chunks

    chunks = chunks[:2]

    prompt = build_prompt(query, chunks, template=template)
    answer = generate(prompt)
    return {
        "query": query,
        "chunks": chunks,
        "prompt": prompt,
        "response": answer
    }