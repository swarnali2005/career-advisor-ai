import chromadb

CHROMA_PATH = "../chroma_db"
COLLECTION_NAME = "careers"

def query_vectorstore(query_text, n_results=5):
    client = chromadb.PersistentClient(path=CHROMA_PATH)
    collection = client.get_collection(name=COLLECTION_NAME)

    results = collection.query(
        query_texts=[query_text],
        n_results=n_results
    )

    print(f"\nQuery: {query_text}\n")
    for i, (doc_id, doc, meta, dist) in enumerate(zip(
        results["ids"][0],
        results["documents"][0],
        results["metadatas"][0],
        results["distances"][0]
    )):
        print(f"{i+1}. {meta['title']}  (distance: {dist:.4f})")
        print(f"   {doc[:150]}...")
        print()

if __name__ == "__main__":
    test_queries = [
        "I like coding and solving logical problems",
        "I enjoy helping people and listening to their problems",
        "I am good at drawing and visual design",
    ]

    for q in test_queries:
        query_vectorstore(q)
        print("-" * 80)