# pipeline_cloud.py
# Name: Zanetta Crentsil
# Index Number: 10022300124

import os
import json
import datetime
import requests
from retriever import retrieve
from prompt import build_prompt

OPENROUTER_KEY = os.environ.get("OPENROUTER_KEY", "")

def generate(prompt):
    response = requests.post(
        "https://openrouter.ai/api/v1/chat/completions",
        headers={
            "Authorization": f"Bearer {OPENROUTER_KEY}",
            "Content-Type": "application/json"
        },
        json={
            "model": "google/gemma-3-4b-it:free",
            "messages": [{"role": "user", "content": prompt}]
        },
        timeout=60
    )
    result = response.json()
    if "choices" not in result:
        raise Exception(f"API error: {result}")
    return result["choices"][0]["message"]["content"]

def run_pipeline(query, k=5, template="default"):
    chunks = retrieve(query, k=k)
    prompt = build_prompt(query, chunks, template=template)
    answer = generate(prompt)
    return {
        "query": query,
        "chunks": chunks,
        "prompt": prompt,
        "response": answer
    }