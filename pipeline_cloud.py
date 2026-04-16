# pipeline_cloud.py
# Name: Zanetta Crentsil
# Index Number: 10022300124

import os
import requests
from retriever import retrieve
from prompt import build_prompt

OPENROUTER_KEY = os.environ.get("OPENROUTER_KEY", "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")

def generate(prompt):
    models = [
        "mistralai/mistral-small-3.1-24b-instruct:free",
        "deepseek/deepseek-r1-0528-qwen3-8b:free",
        "google/gemma-3-4b-it:free",
        "google/gemma-3-1b-it:free",
        "qwen/qwen3-4b:free",
        "meta-llama/llama-3.2-1b-instruct:free",
    ]
    for model in models:
        try:
            response = requests.post(
                "https://openrouter.ai/api/v1/chat/completions",
                headers={
                    "Authorization": f"Bearer {OPENROUTER_KEY}",
                    "Content-Type": "application/json",
                    "HTTP-Referer": "https://acity.edu.gh",
                    "X-Title": "ACity RAG Chatbot"
                },
                json={
                    "model": model,
                    "messages": [{"role": "user", "content": prompt}],
                    "max_tokens": 500
                },
                timeout=30
            )
            result = response.json()
            if "choices" in result:
                print(f"[LLM] Used model: {model}")
                return result["choices"][0]["message"]["content"]
            else:
                print(f"[LLM] Model {model} failed: {result}")
        except Exception as e:
            print(f"[LLM] Model {model} error: {e}")
            continue
    return "All AI models are temporarily busy. Your retrieved documents show: " + prompt[-500:]

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