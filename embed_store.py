from sentence_transformers import SentenceTransformer
import chromadb

# Load embedding model
model = SentenceTransformer("all-MiniLM-L6-v2")

# Read chunks from file
with open("chunks.txt", "r", encoding="utf-8") as f:
    text = f.read()

chunks = text.split("\n\n==========\n\n")

# Create ChromaDB database
client = chromadb.PersistentClient(path="chroma_db")
collection = client.get_or_create_collection("msds_reviews")

# Add chunks
for i, chunk in enumerate(chunks):
    embedding = model.encode(chunk).tolist()

    collection.add(
        ids=[str(i)],
        embeddings=[embedding],
        documents=[chunk],
        metadatas=[{"chunk_id": i}]
    )

print(f"Stored {len(chunks)} chunks in ChromaDB")