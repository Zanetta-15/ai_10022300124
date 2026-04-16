# retriever.py
# Name: [Your Full Name]
# Index Number: 10022300124

import chromadb

# ── connect to existing index ─────────────────────────────────────────────────

def get_collection():
    client = chromadb.PersistentClient(path="./chroma_db")
    return client.get_collection("acity_rag")

# ── query expansion ───────────────────────────────────────────────────────────

def expand_query(query):
    """
    Generate multiple versions of the query to improve retrieval coverage.
    This is manual query expansion - no LLM needed here.
    """
    expansions = [query]

    q = query.lower()

    # Budget-related expansions
    if any(w in q for w in ["budget", "spending", "expenditure", "fiscal"]):
        expansions.append(f"government spending allocation {query}")
        expansions.append(f"Ghana 2025 budget fiscal policy {query}")

    # Election-related expansions
    if any(w in q for w in ["election", "vote", "result", "winner", "candidate", "won", "party", "npp", "ndc", "region"]):
        expansions.append(f"Ghana election results votes constituency {query}")
        expansions.append(f"parliamentary presidential results {query}")

    # Economic expansions
    if any(w in q for w in ["economy", "gdp", "growth", "inflation", "revenue"]):
        expansions.append(f"Ghana economic performance indicators {query}")
        expansions.append(f"macroeconomic policy Ghana {query}")

    # Generic fallback expansion
    expansions.append(f"Ghana {query}")

    print(f"[RETRIEVER] Expanded into {len(expansions)} queries")
    return expansions

# ── top-k retrieval ───────────────────────────────────────────────────────────

def retrieve(query, k=5):
    collection = get_collection()
    expanded_queries = expand_query(query)

    seen_ids = set()
    all_results = []

    for eq in expanded_queries:
        results = collection.query(
            query_texts=[eq],
            n_results=k,
            include=["documents", "distances", "metadatas"]
        )

        docs = results["documents"][0]
        distances = results["distances"][0]
        metadatas = results["metadatas"][0]
        ids = results["ids"][0]

        for doc, dist, meta, doc_id in zip(docs, distances, metadatas, ids):
            if doc_id not in seen_ids:
                seen_ids.add(doc_id)
                similarity = round(1 - dist, 4)
                all_results.append({
                    "id": doc_id,
                    "text": doc,
                    "score": similarity,
                    "source": meta.get("source", "unknown")
                })

    # Re-rank by similarity score (highest first)
    all_results.sort(key=lambda x: x["score"], reverse=True)

    # Return top-k after re-ranking
    top_results = all_results[:k]

    print(f"\n[RETRIEVER] Top {k} chunks retrieved:")
    for i, r in enumerate(top_results):
        print(f"  [{i+1}] score={r['score']} | source={r['source']} | id={r['id']}")
        print(f"       {r['text'][:80]}...")

    return top_results

# ── failure case demo ─────────────────────────────────────────────────────────

def show_failure_case():
    print("\n[FAILURE CASE] Ambiguous query: 'Who won?'")
    results = retrieve("Who won?", k=3)
    print("→ Problem: Too vague, retrieves mixed irrelevant chunks")
    print("→ Fix: Query expansion adds 'Ghana election results votes constituency'")
    print()

if __name__ == "__main__":
    # Test normal retrieval
    test_query = "What is the total budget allocation for education in 2025?"
    print(f"[TEST] Query: {test_query}\n")
    results = retrieve(test_query, k=5)

    print("\n" + "="*60)

    # Show failure case
    show_failure_case()