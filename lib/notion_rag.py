import chromadb
import openai

from settings import CHROMA_DB_PATH, CHROMA_COLLECTION_NAME, OPENAI_API_KEY

# --- Initialization in your bot file ---
openai.api_key = OPENAI_API_KEY
chroma_client = chromadb.PersistentClient(path=CHROMA_DB_PATH) # Connect to the same local folder
collection = chroma_client.get_collection(name=CHROMA_COLLECTION_NAME)

# --- The Updated RAG Function ---
def retrieve_from_knowledge_base(query: str) -> str:
    """
    Searches the ChromaDB vector store for relevant context.
    """
    print(f"Searching knowledge base for: {query}")
    
    # 1. Create an embedding for the user's query
    query_embedding = openai.embeddings.create(
        input=query,
        model="text-embedding-3-small"
    ).data[0].embedding
    
    # 2. Query ChromaDB for the 3 most relevant chunks
    results = collection.query(
        query_embeddings=[query_embedding],
        n_results=3
    )
    
    # 3. Format the results into a context string
    context = "Context from Notion:\n"
    for doc, meta in zip(results['documents'][0], results['metadatas'][0]):
        context += f"- Source: {meta['title']} ({meta['source_url']})\n"
        context += f"  Content: {doc}\n\n"
        
    return context
