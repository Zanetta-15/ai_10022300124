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
    if len(words) > 400:
        prompt = " ".join(words[:400])

    response = requests.post(
        "https://api.groq.com/openai/v1/chat/completions",
        headers={
            "Authorization": f"Bearer {GROQ_KEY}",
            "Content-Type": "application/json"
        },
        json={
            "model": "llama-3.1-8b-instant",
            "messages": [{"role": "user", "content": prompt}],
            "max_tokens": 200
        },
        timeout=30
    )
    result = response.json()
    if "choices" not in result:
        raise Exception(f"Groq error: {result}")
    return result["choices"][0]["message"]["content"]


def run_pipeline(query, k=2, template="default"):
    chunks = retrieve(query, k=k)
    prompt = build_prompt(query, chunks, template=template)
    answer = generate(prompt)
    return {
        "query": query,
        "chunks": chunks,
        "prompt": prompt,
        "response": answer
    }