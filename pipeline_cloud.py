# pipeline_cloud.py
# Name: Zanetta Crentsil
# Index Number: 10022300124

import os
import requests
from retriever import retrieve
from prompt import build_prompt

OPENROUTER_KEY = os.environ.get("OPENROUTER_KEY", "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")

MODELS = [
    "google/gemma-3-4b-it:free",
    "meta-llama/llama-3.2-3b-instruct:free",
    "qwen/qwen2.5-vl-3b-instruct:free",
]

def generate(prompt):
    for model in MODELS:
        try:
            response = requests.post(
                "https://openrouter.ai/api/v1/chat/completions",
                headers={
                    "Authorization": f"Bearer {OPENROUTER_KEY}",
                    "Content-Type": "application/json"
                },
                json={
                    "model": model,
                    "messages": [{"role": "user", "content": prompt}]
                },
                timeout=60
            )
            result = response.json()
            if "choices" in result:
                return result["choices"][0]["message"]["content"]
        except Exception as e:
            continue
    return "I'm sorry, the AI model is temporarily unavailable. Please try again in a moment."

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