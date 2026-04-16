# prompt.py
# Name: [Your Full Name]
# Index Number: 10022300124

def build_context(chunks, max_words=2000):
    context_parts = []
    word_count = 0

    for i, chunk in enumerate(chunks):
        chunk_words = len(chunk["text"].split())
        if word_count + chunk_words > max_words:
            print(f"[PROMPT] Context window full at chunk {i+1}, truncating")
            break
        context_parts.append(
            f"[Source: {chunk['source']} | Score: {chunk['score']}]\n{chunk['text']}"
        )
        word_count += chunk_words

    print(f"[PROMPT] Built context with {len(context_parts)} chunks, ~{word_count} words")
    return "\n\n---\n\n".join(context_parts)


def build_prompt(query, chunks, template="default"):
    context = build_context(chunks)

    if template == "default":
        prompt = f"""You are an AI assistant for Academic City University with access to Ghana's 2025 Budget Statement and Ghana Election Results.

Use ONLY the context below to answer the question.
If the answer is not in the context, say: "I don't have that information in my documents."
Do NOT make up numbers, names, or facts.

CONTEXT:
{context}

QUESTION: {query}

ANSWER:"""

    elif template == "strict":
        prompt = f"""You are a factual assistant. Answer using ONLY the excerpts provided.
Do not use any outside knowledge. If unsure, say "Not found in documents."
Quote specific figures when available.

EXCERPTS:
{context}

QUESTION: {query}

ANSWER (cite your source):"""

    elif template == "conversational":
        prompt = f"""You are a helpful Academic City University chatbot.
Answer the question below in a friendly, clear way using only the provided context.
If the context doesn't contain the answer, politely say so.

Here is what I found in the documents:
{context}

User asked: {query}

Response:"""

    print(f"[PROMPT] Using template: '{template}'")
    print(f"[PROMPT] Final prompt length: {len(prompt.split())} words")
    return prompt


def compare_templates(query, chunks):
    print("\n" + "="*60)
    print(f"PROMPT EXPERIMENT — Query: {query}")
    print("="*60)

    for template in ["default", "strict", "conversational"]:
        prompt = build_prompt(query, chunks, template=template)
        print(f"\n[Template: {template}]")
        print(prompt[:300] + "...\n")

    print("→ Experiment: Send each to LLM and compare outputs in logs/experiment_log.md")


if __name__ == "__main__":
    mock_chunks = [
        {
            "text": "The 2025 budget allocates GH₵ 21.3 billion to the education sector representing 15% of total expenditure.",
            "score": 0.82,
            "source": "budget_pdf"
        },
        {
            "text": "Government spending on education includes salaries, infrastructure and capex for universities.",
            "score": 0.74,
            "source": "budget_pdf"
        }
    ]
    query = "What is the budget allocation for education?"
    compare_templates(query, mock_chunks)