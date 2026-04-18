# Manual Experiment Log
## Student: Zanetta Crentsil | Index: 10022300124
## Course: CS4241 - Introduction to Artificial Intelligence

---

## Experiment 1: Prompt Template Comparison
**Date:** April 16, 2026
**Query:** "What is Ghana's GDP growth target for 2025?"

### Default Template
- Response: "4%"
- Retrieved chunks: 5 from budget_pdf
- Top score: 0.8137
- Observation: Short and direct but slightly imprecise. Actual answer is 4.8%

### Strict Template
- Response: Gave GDP figures but cited wrong source
- Observation: More verbose, attempts citation but hallucinates source name
- Conclusion: Strict template causes more hallucination on numerical data

### Conversational Template
- Response: Said it couldn't find the answer and suggested checking GSS website
- Observation: Most cautious response, avoids hallucination but too conservative

### Conclusion
Default template gives best balance between accuracy and brevity for factual queries.

---

## Experiment 2: Retrieval Quality Test
**Query:** "Who won in the Brong Ahafo region in 2020?"

- Top retrieved chunk: election_csv (score 0.53)
- Response: Nana Akufo-Addo, NPP
- Observation: Election data correctly retrieved when query contains region name
- Issue found: Budget chunks ranked higher than election chunks initially
- Fix applied: Added "won", "region", "party" as election trigger words in query expansion

---

## Experiment 3: Adversarial Testing (Part E)

### Test 1 - Out of scope query
- Query: "What will Ghana's budget be in 2030?"
- RAG Response: "I don't have that information in my documents"
- Pure LLM Response: Made up future projections
- Conclusion: RAG correctly refused to hallucinate. Pure LLM hallucinated future data ✅

### Test 2 - Ambiguous query
- Query: "Who won?"
- RAG Response: Asked for clarification, couldn't determine context
- Pure LLM Response: Confused, gave unrelated answer
- Conclusion: Both struggled but RAG was more honest about ambiguity ✅

---

## Experiment 4: Chunking Impact
- Chunk size 512 tokens with 64 overlap
- Observation: Budget PDF produces dense numerical chunks that reduce retrieval precision
- Fix: Increased context window to include more chunks per query
- Result: More relevant context passed to LLM

---

## Experiment 5: Failure Case Analysis
- Query: "Who won in Tarkwa?"
- Result: Retrieved budget chunks instead of election data (score 0.47)
- Reason: "Tarkwa" is a constituency not in this dataset
- Fix: Dataset only contains regional presidential results, not constituency data
- Documented as known limitation