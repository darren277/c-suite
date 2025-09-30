"""
Knowledge Base Creator for Notion
Reads knowledge_base.yaml and creates/updates Notion database and pages
"""

import yaml
import sys
import os
from datetime import datetime
from notion_client import Client
import sys
import os
sys.path.append(os.path.dirname(os.path.dirname(os.path.abspath(__file__))))
from settings import NOTION_API_TOKEN, NOTION_DOCUMENTATION_DB_ID

# Add parent directory to path for imports
sys.path.append(os.path.dirname(os.path.dirname(os.path.abspath(__file__))))

def load_knowledge_schema():
    """Load the knowledge base schema from YAML file"""
    with open('knowledge_base.yaml', 'r', encoding='utf-8') as file:
        return yaml.safe_load(file)

def create_database_properties(notion, schema):
    """Create or update the Notion database with the defined properties"""
    db_config = schema['database']
    
    # Define the properties structure for Notion API
    properties = {}
    
    for prop_name, prop_config in db_config['properties'].items():
        if prop_name == 'title':
            properties[prop_name] = {
                "title": {}
            }
        elif prop_config['type'] == 'select':
            properties[prop_name] = {
                "select": {
                    "options": [{"name": option} for option in prop_config['options']]
                }
            }
        elif prop_config['type'] == 'multi_select':
            properties[prop_name] = {
                "multi_select": {
                    "options": [{"name": option} for option in prop_config['options']]
                }
            }
        elif prop_config['type'] == 'date':
            properties[prop_name] = {
                "date": {}
            }
        elif prop_config['type'] == 'url':
            properties[prop_name] = {
                "url": {}
            }
    
    return properties

def create_database(notion, schema):
    """Create the main knowledge base database"""
    db_config = schema['database']
    
    try:
        # Try to get existing database
        database = notion.databases.retrieve(database_id=NOTION_DOCUMENTATION_DB_ID)
        print(f"✅ Found existing database: {database['title'][0]['plain_text']}")
        
        # Update properties if needed
        properties = create_database_properties(notion, schema)
        notion.databases.update(
            database_id=NOTION_DOCUMENTATION_DB_ID,
            properties=properties
        )
        print("✅ Updated database properties")
        
    except Exception as e:
        print(f"❌ Error accessing database: {e}")
        print("Please check your NOTION_DATABASE_ID in settings.py")
        return None

    return NOTION_DOCUMENTATION_DB_ID

def create_page_content(notion, page_data, database_id):
    """Create a page in the Notion database"""
    
    # Prepare properties
    properties = {
        "Title": {
            "title": [{"text": {"content": page_data['title']}}]
        },
        "Category": {
            "select": {"name": page_data['category']}
        },
        "Subcategory": {
            "select": {"name": page_data['subcategory']}
        },
        "Department": {
            "multi_select": [{"name": dept} for dept in page_data['department']]
        },
        "Document Type": {
            "select": {"name": page_data['document_type']}
        },
        "Priority": {
            "select": {"name": page_data['priority']}
        },
        "Status": {
            "select": {"name": page_data['status']}
        },
        "Last Updated": {
            "date": {"start": datetime.now().isoformat()}
        }
    }
    
    if 'tags' in page_data and page_data['tags']:
        properties["Tags"] = {
            "multi_select": [{"name": tag} for tag in page_data['tags']]
        }
    
    if 'url' in page_data and page_data['url']:
        properties["URL"] = {
            "url": page_data['url']
        }
    
    # Create the page
    try:
        page = notion.pages.create(
            parent={"database_id": database_id},
            properties=properties
        )
        
        # Add content to the page
        content_blocks = convert_markdown_to_blocks(page_data['content'])
        if content_blocks:
            notion.blocks.children.append(
                block_id=page['id'],
                children=content_blocks
            )
        
        print(f"✅ Created page: {page_data['title']}")
        return page
        
    except Exception as e:
        print(f"❌ Error creating page '{page_data['title']}': {e}")
        return None

def convert_markdown_to_blocks(content):
    """Convert markdown content to Notion blocks"""
    blocks = []
    lines = content.split('\n')
    
    for line in lines:
        line = line.rstrip()
        
        if not line:
            continue
            
        # Headers
        if line.startswith('# '):
            blocks.append({
                "object": "block",
                "type": "heading_1",
                "heading_1": {
                    "rich_text": [{"type": "text", "text": {"content": line[2:]}}]
                }
            })
        elif line.startswith('## '):
            blocks.append({
                "object": "block",
                "type": "heading_2",
                "heading_2": {
                    "rich_text": [{"type": "text", "text": {"content": line[3:]}}]
                }
            })
        elif line.startswith('### '):
            blocks.append({
                "object": "block",
                "type": "heading_3",
                "heading_3": {
                    "rich_text": [{"type": "text", "text": {"content": line[4:]}}]
                }
            })
        # Code blocks
        elif line.startswith('```'):
            continue  # Skip code block markers for now
        # Bullet points
        elif line.startswith('- '):
            blocks.append({
                "object": "block",
                "type": "bulleted_list_item",
                "bulleted_list_item": {
                    "rich_text": [{"type": "text", "text": {"content": line[2:]}}]
                }
            })
        # Checkboxes
        elif line.startswith('- [ ]'):
            blocks.append({
                "object": "block",
                "type": "to_do",
                "to_do": {
                    "rich_text": [{"type": "text", "text": {"content": line[5:]}}],
                    "checked": False
                }
            })
        elif line.startswith('- [x]'):
            blocks.append({
                "object": "block",
                "type": "to_do",
                "to_do": {
                    "rich_text": [{"type": "text", "text": {"content": line[5:]}}],
                    "checked": True
                }
            })
        # Regular paragraphs
        else:
            blocks.append({
                "object": "block",
                "type": "paragraph",
                "paragraph": {
                    "rich_text": [{"type": "text", "text": {"content": line}}]
                }
            })
    
    return blocks

def sync_knowledge_base():
    """Main function to sync knowledge base to Notion"""
    print("🚀 Starting Knowledge Base Sync...")
    
    # Load schema
    try:
        schema = load_knowledge_schema()
        print("✅ Loaded knowledge base schema")
    except Exception as e:
        print(f"❌ Error loading schema: {e}")
        return
    
    # Initialize Notion client
    try:
        notion = Client(auth=NOTION_API_TOKEN)
        print("✅ Connected to Notion API")
    except Exception as e:
        print(f"❌ Error connecting to Notion: {e}")
        return
    
    # Create/update database
    database_id = create_database(notion, schema)
    if not database_id:
        return
    
    # Create pages
    content = schema['content']
    total_pages = 0
    created_pages = 0
    
    for category, subcategories in content.items():
        print(f"\nProcessing category: {category.title()}")
        
        for subcategory, pages in subcategories.items():
            print(f"  Processing subcategory: {subcategory}")
            
            for page_data in pages:
                total_pages += 1
                page = create_page_content(notion, page_data, database_id)
                if page:
                    created_pages += 1
    
    print("Sync complete!")
    print(f"Total pages processed: {total_pages}")
    print(f"✅ Successfully created: {created_pages}")
    print(f"❌ Failed: {total_pages - created_pages}")

if __name__ == "__main__":
    sync_knowledge_base()
