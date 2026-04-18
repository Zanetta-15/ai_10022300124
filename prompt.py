# prompt.py
# Name: Zanetta Crentsil
# Index Number: 10022300124

def build_context(chunks, max_words=150):
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
        prompt = f"""You are an AI assistant with access to Ghana's 2025 Budget and Election Results.
Use ONLY the context below. If not in context say "I don't have that information."
Do NOT make up facts.

CONTEXT:
{context}

QUESTION: {query}

ANSWER:"""

    elif template == "strict":
        prompt = f"""Answer using ONLY the excerpts provided.
If unsure say "Not found in documents."

EXCERPTS:
{context}

QUESTION: {query}

ANSWER:"""

    elif template == "conversational":
        prompt = f"""You are a helpful chatbot. Answer using only the context below.
If not found, politely say so.

CONTEXT:
{context}

QUESTION: {query}

RESPONSE:"""

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