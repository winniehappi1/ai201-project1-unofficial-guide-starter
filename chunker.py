from pathlib import Path


def load_documents(folder="documents"):
    docs = []

    for file in Path(folder).glob("*.txt"):
        text = file.read_text(encoding="utf-8").strip()

        if text:
            docs.append({
                "source": file.name,
                "title": file.stem.replace("_", " "),
                "text": text
            })

    return docs


def chunk_text(text, chunk_size=800, overlap=150):
    paragraphs = [p.strip() for p in text.split("\n\n") if p.strip()]
    chunks = []
    current = ""

    for paragraph in paragraphs:
        if len(current) + len(paragraph) + 2 <= chunk_size:
            current += paragraph + "\n\n"
        else:
            if current.strip():
                chunks.append(current.strip())

            overlap_text = current[-overlap:] if current else ""
            current = overlap_text + "\n\n" + paragraph + "\n\n"

    if current.strip():
        chunks.append(current.strip())

    return chunks


def create_chunks(documents):
    all_chunks = []

    for doc in documents:
        chunks = chunk_text(doc["text"])

        for i, chunk in enumerate(chunks):
            chunk_with_source = (
                f"Source: {doc['source']}\n"
                f"Title: {doc['title']}\n\n"
                f"{chunk}"
            )

            all_chunks.append({
                "source": doc["source"],
                "title": doc["title"],
                "chunk_id": i,
                "text": chunk_with_source
            })

    return all_chunks


if __name__ == "__main__":
    docs = load_documents()
    print(f"Loaded {len(docs)} documents")

    chunks = create_chunks(docs)
    print(f"Created {len(chunks)} chunks")

    with open("chunks.txt", "w", encoding="utf-8") as f:
        for chunk in chunks:
            f.write(chunk["text"])
            f.write("\n\n==========\n\n")

    print("Saved chunks to chunks.txt")

    print("\nSample chunks:\n")
    for chunk in chunks[:5]:
        print("=" * 50)
        print(chunk["source"])
        print(chunk["text"][:400])
        print()