import chromadb
from notion_client import Client
import openai
import sys
import os
sys.path.append(os.path.dirname(os.path.dirname(os.path.abspath(__file__))))
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
        block_type = block.get('type', '')
        
        if block_type == 'paragraph':
            rich_text = block.get('paragraph', {}).get('rich_text', [])
            if rich_text:
                text.append(rich_text[0].get('plain_text', ''))
        
        elif block_type == 'heading_1':
            rich_text = block.get('heading_1', {}).get('rich_text', [])
            if rich_text:
                text.append(f"# {rich_text[0].get('plain_text', '')}")
        
        elif block_type == 'heading_2':
            rich_text = block.get('heading_2', {}).get('rich_text', [])
            if rich_text:
                text.append(f"## {rich_text[0].get('plain_text', '')}")
        
        elif block_type == 'heading_3':
            rich_text = block.get('heading_3', {}).get('rich_text', [])
            if rich_text:
                text.append(f"### {rich_text[0].get('plain_text', '')}")
        
        elif block_type == 'bulleted_list_item':
            rich_text = block.get('bulleted_list_item', {}).get('rich_text', [])
            if rich_text:
                text.append(f"• {rich_text[0].get('plain_text', '')}")
        
        elif block_type == 'numbered_list_item':
            rich_text = block.get('numbered_list_item', {}).get('rich_text', [])
            if rich_text:
                text.append(f"1. {rich_text[0].get('plain_text', '')}")
        
        elif block_type == 'to_do':
            rich_text = block.get('to_do', {}).get('rich_text', [])
            checked = block.get('to_do', {}).get('checked', False)
            if rich_text:
                checkbox = "☑" if checked else "☐"
                text.append(f"{checkbox} {rich_text[0].get('plain_text', '')}")
        
        elif block_type == 'code':
            rich_text = block.get('code', {}).get('rich_text', [])
            language = block.get('code', {}).get('language', '')
            if rich_text:
                text.append(f"```{language}\n{rich_text[0].get('plain_text', '')}\n```")
        
        elif block_type == 'quote':
            rich_text = block.get('quote', {}).get('rich_text', [])
            if rich_text:
                text.append(f"> {rich_text[0].get('plain_text', '')}")
    
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
