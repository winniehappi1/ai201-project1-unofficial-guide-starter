from sentence_transformers import SentenceTransformer
import chromadb

model = SentenceTransformer("all-MiniLM-L6-v2")

client = chromadb.PersistentClient(path="chroma_db")
collection = client.get_collection("msds_reviews")

query = input("Enter query: ")

query_embedding = model.encode(query).tolist()

results = collection.query(
    query_embeddings=[query_embedding],
    n_results=5
)

print("\nTop Results:\n")

for i, doc in enumerate(results["documents"][0]):
    print("=" * 60)
    print(f"Result {i+1}")
    print(doc[:800])
    print()