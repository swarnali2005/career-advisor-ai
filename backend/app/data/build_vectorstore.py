import json
import chromadb

INPUT_FILE = "career_kb.jsonl"
CHROMA_PATH = "../chroma_db"
COLLECTION_NAME = "careers"

def load_documents():
    docs = []
    with open(INPUT_FILE, "r", encoding="utf-8") as f:
        for line in f:
            docs.append(json.loads(line))
    return docs

def build_vectorstore(docs):
    client = chromadb.PersistentClient(path=CHROMA_PATH)

    # Delete old collection if it exists, so we rebuild cleanly
    try:
        client.delete_collection(COLLECTION_NAME)
    except Exception:
        pass

    collection = client.create_collection(name=COLLECTION_NAME)

    ids = [doc["id"] for doc in docs]
    texts = [doc["text"] for doc in docs]
    metadatas = [{"title": doc["title"]} for doc in docs]

    batch_size = 100
    for i in range(0, len(docs), batch_size):
        collection.add(
            ids=ids[i:i+batch_size],
            documents=texts[i:i+batch_size],
            metadatas=metadatas[i:i+batch_size]
        )
        print(f"Embedded {min(i+batch_size, len(docs))}/{len(docs)} documents")

    print(f"\nVectorstore built successfully with {collection.count()} documents.")

if __name__ == "__main__":
    docs = load_documents()
    build_vectorstore(docs)