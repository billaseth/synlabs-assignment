import os
import hashlib
from typing import List
import chromadb
from chromadb.utils import embedding_functions

# Configuration Constants
CHUNK_SIZE = 500
CHUNK_OVERLAP = 50
DATA_DIR = "./data"
DB_PATH = "./chroma_db"

def get_file_hash(file_path: str) -> str:
    """Generates an MD5 hash of a file to check for changes/duplicates."""
    hasher = hashlib.md5()
    with open(file_path, "rb") as f:
        buf = f.read()
        hasher.update(buf)
    return hasher.hexdigest()

def chunk_text(text: str, chunk_size: int = CHUNK_SIZE, overlap: int = CHUNK_OVERLAP) -> List[str]:
    """Simple text chunker with size and overlap."""
    chunks = []
    start = 0
    while start < len(text):
        end = start + chunk_size
        chunks.append(text[start:end])
        start += chunk_size - overlap
    return chunks

def ingest_documents():
    # Initialize ChromaDB client (local persistent storage)
    client = chromadb.PersistentClient(path=DB_PATH)
    
    # Using default sentence transformer or OpenAI embeddings
    # (Make sure to install chromadb and sentence-transformers)
    collection = client.get_or_create_collection(name="synlabs_rag_corpus")

    if not os.path.exists(DATA_DIR):
        os.makedirs(DATA_DIR)
        print(f"Created {DATA_DIR}. Please put your PDF/TXT/MD files inside it.")
        return

    files = os.listdir(DATA_DIR)
    if not files:
        print(f"No files found in {DATA_DIR}. Add some documents first!")
        return

    for file in files:
        file_path = os.path.join(DATA_DIR, file)
        if os.path.isfile(file_path):
            with open(file_path, "r", encoding="utf-8", errors="ignore") as f:
                content = f.read()
            
            file_hash = get_file_hash(file_path)
            chunks = chunk_text(content)
            
            print(f"Processing {file}: {len(chunks)} chunks created.")
            
            for i, chunk in enumerate(chunks):
                # Unique ID per chunk based on file hash and index to ensure idempotency
                chunk_id = f"{file_hash}_chunk_{i}"
                
                # Check if chunk already exists to maintain idempotent re-ingest
                existing = collection.get(ids=[chunk_id])
                if existing and existing['ids']:
                    continue  # Skip if already exists
                
                collection.add(
                    ids=[chunk_id],
                    documents=[chunk],
                    metadatas=[{"source_file": file, "chunk_index": i, "file_hash": file_hash}]
                )
    
    print(f"Ingestion complete. Total vectors in store: {collection.count()}")

if __name__ == "__main__":
    ingest_documents()