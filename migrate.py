import chromadb
from settings import CHROMA_API_KEY, CHROMA_API_TENANT, CHROMA_API_DATABASE
  
client = chromadb.CloudClient(
  api_key=CHROMA_API_KEY,
  tenant=CHROMA_API_TENANT,
  database=CHROMA_API_DATABASE
)

collection = client.get_collection(name="notion-knowledge-base")

def test_migrate():
    print("Total documents in knowledge base:", collection.count())

    docs = [
        "We are prioritizing hiring two senior backend engineers and one product marketing manager in Q4.",
        "The budget for Q4 has been approved and is available for allocation.",
        "The new product launch is scheduled for November 15th, with marketing campaigns starting two weeks prior."
    ]

    for doc in docs:
        results = collection.query(
            query_texts=[doc],
            n_results=2
        )
        print(f"Query: {doc}")
        for i in range(len(results['documents'][0])):
            print(f"- Result {i+1}: {results['documents'][0][i]} (Score: {results['distances'][0][i]})")
        print()


if __name__ == "__main__":
    test_migrate()
