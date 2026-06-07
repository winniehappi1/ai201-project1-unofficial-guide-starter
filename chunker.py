from pathlib import Path


def load_documents(folder="documents"):
    docs = []

    for file in Path(folder).glob("*.txt"):
        with open(file, "r", encoding="utf-8") as f:
            text = f.read().strip()

            docs.append({
                "source": file.name,
                "text": text
            })

    return docs


def chunk_text(text, chunk_size=800, overlap=150):
    chunks = []

    start = 0

    while start < len(text):
        end = start + chunk_size

        chunk = text[start:end]

        if len(chunk.strip()) > 0:
            chunks.append(chunk)

        start += chunk_size - overlap

    return chunks


def create_chunks(documents):
    all_chunks = []

    for doc in documents:
        chunks = chunk_text(doc["text"])

        for i, chunk in enumerate(chunks):
            all_chunks.append({
                "source": doc["source"],
                "chunk_id": i,
                "text": chunk
            })

    return all_chunks


if __name__ == "__main__":
    docs = load_documents()

    print(f"Loaded {len(docs)} documents")

    chunks = create_chunks(docs)

    print(f"Created {len(chunks)} chunks")

    print("\nSample chunks:\n")

    for chunk in chunks[:5]:
        print("=" * 50)
        print(chunk["source"])
        print(chunk["text"][:300])
        print()