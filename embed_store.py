import shutil
from pathlib import Path
from sentence_transformers import SentenceTransformer
import chromadb


DB_PATH = "chroma_db"
COLLECTION_NAME = "msds_reviews"

if Path(DB_PATH).exists():
    shutil.rmtree(DB_PATH)

model = SentenceTransformer("all-MiniLM-L6-v2")

with open("chunks.txt", "r", encoding="utf-8") as f:
    raw_text = f.read()

chunks = [
    chunk.strip()
    for chunk in raw_text.split("\n\n==========\n\n")
    if chunk.strip()
]

client = chromadb.PersistentClient(path=DB_PATH)
collection = client.get_or_create_collection(COLLECTION_NAME)

for i, chunk in enumerate(chunks):
    embedding = model.encode(chunk).tolist()

    source = "unknown"
    for line in chunk.splitlines():
        if line.startswith("Source:"):
            source = line.replace("Source:", "").strip()
            break

    collection.add(
        ids=[str(i)],
        embeddings=[embedding],
        documents=[chunk],
        metadatas=[{"chunk_id": i, "source": source}]
    )

print(f"Stored {len(chunks)} chunks in ChromaDB")