import os
from dotenv import load_dotenv
from groq import Groq
from sentence_transformers import SentenceTransformer
import chromadb

load_dotenv()

GROQ_API_KEY = os.getenv("GROQ_API_KEY")

if not GROQ_API_KEY:
    raise ValueError("Missing GROQ_API_KEY in .env file")

client = Groq(api_key=GROQ_API_KEY)

model = SentenceTransformer("all-MiniLM-L6-v2")

chroma_client = chromadb.PersistentClient(path="chroma_db")
collection = chroma_client.get_collection("msds_reviews")


def retrieve_chunks(question, top_k=4):
    query_embedding = model.encode(question).tolist()

    results = collection.query(
        query_embeddings=[query_embedding],
        n_results=top_k
    )

    chunks = []

    for doc, metadata, distance in zip(
        results["documents"][0],
        results["metadatas"][0],
        results["distances"][0]
    ):
        chunks.append({
            "text": doc,
            "source": metadata.get("source", "unknown"),
            "distance": distance
        })

    return chunks


def ask(question):
    chunks = retrieve_chunks(question)

    context = "\n\n---\n\n".join(
        [f"Source: {chunk['source']}\n{chunk['text']}" for chunk in chunks]
    )

    prompt = f"""
You are answering questions using ONLY the retrieved documents below.

Rules:
- Do not use outside knowledge.
- If the documents do not contain enough information, say: "I don't have enough information on that."
- Cite the source filenames used in your answer.

Retrieved documents:
{context}

Question:
{question}

Answer:
"""

    response = client.chat.completions.create(
        model="llama-3.3-70b-versatile",
        messages=[
            {"role": "system", "content": "You are a grounded RAG assistant. Answer only from retrieved context."},
            {"role": "user", "content": prompt}
        ],
        temperature=0.2
    )

    answer = response.choices[0].message.content

    sources = sorted(set(chunk["source"] for chunk in chunks))

    return {
        "answer": answer,
        "sources": sources,
        "chunks": chunks
    }


if __name__ == "__main__":
    question = input("Ask a question: ")
    result = ask(question)

    print("\nAnswer:\n")
    print(result["answer"])

    print("\nSources retrieved:")
    for source in result["sources"]:
        print(f"- {source}")