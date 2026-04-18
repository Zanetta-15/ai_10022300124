# pipeline_cloud.py
# Name: Zanetta Crentsil
# Index Number: 10022300124

import os
import requests
from retriever import retrieve
from prompt import build_prompt

GROQ_KEY = "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"

def generate(prompt):
    try:
        response = requests.post(
            "https://api.groq.com/openai/v1/chat/completions",
            headers={
                "Authorization": f"Bearer {GROQ_KEY}",
                "Content-Type": "application/json"
            },
            json={
                "model": "llama-3.1-8b-instant",
                "messages": [{"role": "user", "content": prompt}],
                "max_tokens": 500
            },
            timeout=30
        )
        result = response.json()
        if "choices" in result:
            return result["choices"][0]["message"]["content"]
        elif "error" in result:
            error_msg = result["error"].get("message", "Unknown error")
            if "rate" in error_msg.lower():
                return "⚠️ Rate limit reached. Please wait 10 seconds and try again."
            return f"⚠️ API error: {error_msg}"
        return "⚠️ Unexpected response from AI. Please try again."
    except Exception as e:
        return f"⚠️ Connection error: {str(e)}. Please try again."

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