# pipeline_cloud.py
# Name: Zanetta Crentsil
# Index Number: 10022300124

import requests
from retriever import retrieve

GROQ_KEY = "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"

def generate(context, query):
    prompt = f"""Based on this data, answer the question directly and concisely.

DATA:
{context}

QUESTION: {query}

ANSWER:"""

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
            "max_tokens": 150
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

    context = "\n\n".join([c["text"][:300] for c in chunks])
    answer = generate(context, query)

    return {
        "query": query,
        "chunks": chunks,
        "prompt": f"Context: {context}\nQuestion: {query}",
        "response": answer
    }