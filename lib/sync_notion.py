import chromadb
from notion_client import Client
import openai
from settings import CHROMA_COLLECTION_NAME, CHROMA_DB_PATH, NOTION_API_TOKEN, NOTION_DATABASE_ID, OPENAI_API_KEY


notion = Client(auth=NOTION_API_TOKEN)
openai.api_key = OPENAI_API_KEY
chroma_client = chromadb.PersistentClient(path=CHROMA_DB_PATH) # This will save the DB to a local folder
collection = chroma_client.get_or_create_collection(name=CHROMA_COLLECTION_NAME)

# --- FUNCTIONS ---
def get_text_from_blocks(blocks):
    """Extracts plain text from a list of Notion block objects."""
    text = []
    for block in blocks:
        if block['type'] == 'paragraph':
            text.append(block['paragraph']['rich_text'][0]['plain_text'])
    return "\n".join(text)

def chunk_text(text, chunk_size=1000):
    """Simple function to break text into smaller chunks."""
    return [text[i:i+chunk_size] for i in range(0, len(text), chunk_size)]

# --- MAIN SYNC LOGIC ---
if __name__ == "__main__":
    print("Starting Notion sync...")
    db_pages = notion.databases.query(database_id=NOTION_DATABASE_ID).get("results")
    
    for page in db_pages:
        page_id = page['id']
        page_title = page['properties']['Name']['title'][0]['text']['content']
        page_url = page['url']
        
        print(f"Processing page: {page_title}")
        
        blocks = notion.blocks.children.list(block_id=page_id).get('results')
        page_text = get_text_from_blocks(blocks)
        
        chunks = chunk_text(page_text)
        
        for i, chunk in enumerate(chunks):
            # Generate embedding for the chunk
            embedding = openai.embeddings.create(
                input=chunk,
                model="text-embedding-3-small"
            ).data[0].embedding
            
            # Store the chunk, embedding, and metadata in ChromaDB
            doc_id = f"{page_id}_{i}"
            collection.add(
                embeddings=[embedding],
                documents=[chunk],
                metadatas=[{"source_url": page_url, "title": page_title}],
                ids=[doc_id]
            )

    print("Notion sync complete!")
    print(f"Total documents in knowledge base: {collection.count()}")
