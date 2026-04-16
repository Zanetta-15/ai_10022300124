# ingest.py
# Name: [Your Full Name]
# Index Number: 10022300124

import fitz  # pymupdf
import pandas as pd
import chromadb
import os
import re

# ── helpers ──────────────────────────────────────────────────────────────────

def clean_text(text):
    text = re.sub(r'\s+', ' ', text)
    text = re.sub(r'[^\x00-\x7F]+', ' ', text)
    text = text.strip()
    return text

def chunk_text(text, chunk_size=512, overlap=64):
    """Split text into overlapping word-level chunks."""
    words = text.split()
    chunks = []
    start = 0
    while start < len(words):
        end = start + chunk_size
        chunk = ' '.join(words[start:end])
        if len(chunk.strip()) > 50:  # skip tiny chunks
            chunks.append(chunk)
        start += chunk_size - overlap
    return chunks

# ── PDF ingestion ─────────────────────────────────────────────────────────────

def load_pdf(path):
    print(f"[INGEST] Loading PDF: {path}")
    doc = fitz.open(path)
    full_text = ""
    for page_num, page in enumerate(doc):
        text = page.get_text()
        full_text += f"\n[Page {page_num+1}]\n{text}"
    doc.close()
    return clean_text(full_text)

# ── CSV ingestion ─────────────────────────────────────────────────────────────

def load_csv(path):
    print(f"[INGEST] Loading CSV: {path}")
    df = pd.read_csv(path)
    df = df.fillna("unknown")

    print(f"[INGEST] CSV columns: {list(df.columns)}")

    chunks = []
    for _, row in df.iterrows():
        # Build a natural language sentence per row
        row_text = "Ghana Election Result: "
        for col in df.columns:
            row_text += f"{col} is {row[col]}. "
        chunks.append(clean_text(row_text))

    return chunks

# ── index builder ─────────────────────────────────────────────────────────────

def build_index():
    client = chromadb.PersistentClient(path="./chroma_db")

    # Delete existing collection if rebuilding
    try:
        client.delete_collection("acity_rag")
    except:
        pass

    collection = client.create_collection(
        name="acity_rag",
        metadata={"hnsw:space": "cosine"}
    )

    all_chunks = []
    all_ids = []
    all_metadata = []

    # --- PDF ---
    pdf_path = "data/2025-Budget-Statement-and-Economic-Policy_v4.pdf"
    if os.path.exists(pdf_path):
        pdf_text = load_pdf(pdf_path)
        pdf_chunks = chunk_text(pdf_text, chunk_size=512, overlap=64)
        print(f"[INGEST] PDF produced {len(pdf_chunks)} chunks")
        for i, chunk in enumerate(pdf_chunks):
            all_chunks.append(chunk)
            all_ids.append(f"pdf_{i}")
            all_metadata.append({"source": "budget_pdf", "chunk_id": i})
    else:
        print(f"[WARNING] PDF not found at {pdf_path}")

    # --- CSV ---
    csv_path = "data/Ghana_Election_Result.csv"
    if os.path.exists(csv_path):
        csv_chunks = load_csv(csv_path)
        print(f"[INGEST] CSV produced {len(csv_chunks)} chunks")
        for i, chunk in enumerate(csv_chunks):
            all_chunks.append(chunk)
            all_ids.append(f"csv_{i}")
            all_metadata.append({"source": "election_csv", "chunk_id": i})
    else:
        print(f"[WARNING] CSV not found at {csv_path}")

    # --- Add to ChromaDB in batches ---
    batch_size = 100
    for i in range(0, len(all_chunks), batch_size):
        batch_chunks = all_chunks[i:i+batch_size]
        batch_ids = all_ids[i:i+batch_size]
        batch_meta = all_metadata[i:i+batch_size]
        collection.add(
            documents=batch_chunks,
            ids=batch_ids,
            metadatas=batch_meta
        )
        print(f"[INGEST] Indexed batch {i//batch_size + 1} ({len(batch_chunks)} chunks)")

    print(f"\n[INGEST] Done! Total chunks indexed: {len(all_chunks)}")
    return collection

if __name__ == "__main__":
    build_index()