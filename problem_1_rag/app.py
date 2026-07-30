import os
import chromadb

# Configuration Constants
DB_PATH = "./chroma_db"
client = chromadb.PersistentClient(path=DB_PATH)
collection = client.get_or_create_collection(name="synlabs_rag_corpus")

def retrieve_chunks(query: str, k: int = 3):
    """Retrieves top-k relevant chunks from ChromaDB locally."""
    results = collection.query(
        query_texts=[query],
        n_results=k
    )
    
    chunks = []
    if results and 'documents' in results and results['documents']:
        docs = results['documents'][0]
        metadatas = results['metadatas'][0] if 'metadatas' in results else [{}] * len(docs)
        for doc, meta in zip(docs, metadatas):
            chunks.append({"text": doc, "metadata": meta})
            
    return chunks

def generate_rag_answer(query: str, k: int = 3):
    """Generates an extractive grounded answer locally without internet/API."""
    retrieved_chunks = retrieve_chunks(query, k=k)
    
    if not retrieved_chunks:
        return "I found no relevant context in the documents to answer your question.", []
    
    # Properly accessing the first element of the retrieved list
    best_chunk = retrieved_chunks[0]
    source = best_chunk['metadata'].get('source_file', 'unknown')
    
    answer = f"Based on source [{source}]: {best_chunk['text']}"
    return answer, retrieved_chunks

if __name__ == "__main__":
    print("--- Local Offline RAG Application Initialized ---")
    query = input("Enter your query: ")
    answer, chunks = generate_rag_answer(query)
    
    print("\n=== Answer ===")
    print(answer)
    
    print("\n=== Retrieved Chunks & Citations ===")
    for idx, c in enumerate(chunks):
        print(f"[{idx+1}] File: {c['metadata'].get('source_file')} | Content snippet: {c['text'][:100]}...")