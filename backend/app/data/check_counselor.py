import chromadb

client = chromadb.PersistentClient(path="../chroma_db")
collection = client.get_collection("careers")

results = collection.get(
    where_document={"$contains": "Counselor"},
    limit=10
)

for m in results["metadatas"]:
    print(m["title"])