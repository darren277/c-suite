"""
Wiki Structure Creator for Notion
Automatically creates hierarchical Wiki structure with master page and category landing pages
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

def load_knowledge_schema():
    """Load the knowledge base schema from YAML file"""
    with open('knowledge_base.yaml', 'r', encoding='utf-8') as file:
        return yaml.safe_load(file)

def create_master_wiki_page(notion, schema, parent_page_id):
    """Create the master Wiki page with navigation and database views"""
    
    # Master Wiki page content
    wiki_content = """# 🏥 HealthTech Company Wiki

> Your central knowledge repository for everything company-related

## 🚀 Quick Start
- **New to the company?** Start with [Company Overview](#company-overview)
- **Looking for technical docs?** Check [Engineering Resources](#engineering-resources)
- **Need compliance info?** See [Operations & Compliance](#operations--compliance)

## 📊 Browse by Category

### 🏢 Company
*Vision, mission, strategy, and team information*

### 🚀 Product  
*Product strategy, features, and management*

### ⚙️ Engineering
*Technical documentation, APIs, and infrastructure*

### 🎨 Design
*UX/UI standards, research, and visual design*

### 📈 Marketing
*Brand guidelines, campaigns, and content*

### 📋 Operations
*SOPs, policies, and legal requirements*

---

## 🔍 Search & Filter
*Use the database views below to find exactly what you need*

## 📋 All Documents
*Complete knowledge base with all approved documents*

## 🔥 High Priority Documents
*Critical information that needs immediate attention*

## 🕒 Recently Updated
*Latest changes and additions to our knowledge base*

## 👥 By Department
*Documents organized by team ownership*

---

## 📚 Category Landing Pages
- [🏢 Company Overview](./Company-Overview)
- [🚀 Product Documentation](./Product-Documentation)
- [⚙️ Engineering Resources](./Engineering-Resources)
- [🎨 Design Guidelines](./Design-Guidelines)
- [📈 Marketing Materials](./Marketing-Materials)
- [📋 Operations & Compliance](./Operations-Compliance)

---

*Last updated: {date}*
""".format(date=datetime.now().strftime("%B %d, %Y"))

    # Convert content to Notion blocks
    blocks = convert_markdown_to_blocks(wiki_content)
    
    # Create the master Wiki page
    try:
        page = notion.pages.create(
            parent={"type": "page_id", "page_id": parent_page_id},
            properties={
                "title": [{"text": {"content": "Company Wiki"}}]
            }
        )
        
        # Add content
        notion.blocks.children.append(
            block_id=page['id'],
            children=blocks
        )
        
        # Add database views
        add_database_views(notion, page['id'], schema)
        
        print(f"✅ Created master Wiki page: {page['id']}")
        return page['id']
        
    except Exception as e:
        print(f"❌ Error creating master Wiki page: {e}")
        return None

def add_database_views(notion, page_id, schema):
    """Add database views to the master Wiki page"""
    
    # Note: Database views need to be created manually in Notion
    # We'll add text blocks that explain how to add the views
    try:
        notion.blocks.children.append(
            block_id=page_id,
            children=[{
                "type": "paragraph",
                "paragraph": {
                    "rich_text": [{"type": "text", "text": {"content": "📋 To add database views, use the /database command and select your knowledge base database. Then configure the views as needed."}}]
                }
            }]
        )
        print("✅ Added database view instructions")
    except Exception as e:
        print(f"❌ Error adding database view instructions: {e}")

def create_category_landing_pages(notion, schema, parent_page_id):
    """Create landing pages for each category"""
    
    categories = {
        "Company": {
            "emoji": "🏢",
            "description": "Vision, mission, strategy, and team information",
            "subcategories": ["Vision & Mission", "Strategy & Planning", "About & History", "Team & People"]
        },
        "Product": {
            "emoji": "🚀", 
            "description": "Product strategy, features, and management",
            "subcategories": ["Product Strategy", "Core Features", "Product Management"]
        },
        "Engineering": {
            "emoji": "⚙️",
            "description": "Technical documentation, APIs, and infrastructure", 
            "subcategories": ["Software Development", "Technical Infrastructure", "DevOps & Deployment"]
        },
        "Design": {
            "emoji": "🎨",
            "description": "UX/UI standards, research, and visual design",
            "subcategories": ["User Experience", "Visual Design", "Research & Insights"]
        },
        "Marketing": {
            "emoji": "📈",
            "description": "Brand guidelines, campaigns, and content",
            "subcategories": ["Brand & Messaging", "Growth & Acquisition", "Content & Communications"]
        },
        "Operations": {
            "emoji": "📋",
            "description": "SOPs, policies, and legal requirements",
            "subcategories": ["Standard Operating Procedures", "Compliance & Legal", "Business Operations"]
        }
    }
    
    created_pages = {}
    
    for category, info in categories.items():
        page_name = f"{info['emoji']} {category} Overview"
        
        # Create category page content
        content = f"""# {page_name}

> {info['description']}

## 📋 Quick Navigation
- [All {category} Documents](#all-{category.lower()}-documents)
- [High Priority](#high-priority-{category.lower()})
- [Recently Updated](#recently-updated-{category.lower()})

## 📚 Subcategories

"""
        
        # Add subcategory sections
        for subcategory in info['subcategories']:
            content += f"### {subcategory}\n"
            content += f"*Documents related to {subcategory.lower()}*\n\n"
        
        content += f"""## 🔗 Related Resources
- [🏢 Company Overview](./Company-Overview) (if not Company)
- [🚀 Product Documentation](./Product-Documentation) (if not Product)
- [⚙️ Engineering Resources](./Engineering-Resources) (if not Engineering)
- [🎨 Design Guidelines](./Design-Guidelines) (if not Design)
- [📈 Marketing Materials](./Marketing-Materials) (if not Marketing)
- [📋 Operations & Compliance](./Operations-Compliance) (if not Operations)

---

## 📊 Document Views

### All {category} Documents
*Complete list of all {category.lower()} related documents*

### High Priority {category}
*Critical {category.lower()} information*

### Recently Updated {category}
*Latest changes in {category.lower()}*

---

*Last updated: {datetime.now().strftime("%B %d, %Y")}*
"""
        
        # Convert to blocks
        blocks = convert_markdown_to_blocks(content)
        
        try:
            # Create the category page
            page = notion.pages.create(
                parent={"type": "page_id", "page_id": parent_page_id},
                properties={
                    "title": [{"text": {"content": page_name}}]
                }
            )
            
            # Add content
            notion.blocks.children.append(
                block_id=page['id'],
                children=blocks
            )
            
            # Add category-specific database views
            add_category_database_views(notion, page['id'], category)
            
            created_pages[category] = page['id']
            print(f"✅ Created {category} landing page: {page['id']}")
            
        except Exception as e:
            print(f"❌ Error creating {category} landing page: {e}")
    
    return created_pages

def add_category_database_views(notion, page_id, category):
    """Add category-specific database views"""
    
    # Add instructions for adding database views
    try:
        notion.blocks.children.append(
            block_id=page_id,
            children=[{
                "type": "paragraph",
                "paragraph": {
                    "rich_text": [{"type": "text", "text": {"content": f"📊 To add {category} database views, use the /database command and filter by Category = '{category}'"}}]
                }
            }]
        )
    except Exception as e:
        print(f"❌ Error adding database view instructions for {category}: {e}")

def get_parent_page_id(notion):
    """Get the parent page ID for creating new pages"""
    # This should be your workspace root or a specific parent page
    # For now, we'll use the database parent
    try:
        database = notion.databases.retrieve(database_id=NOTION_DOCUMENTATION_DB_ID)
        return database['parent']['page_id']
    except:
        # Fallback - you might need to set this manually
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
        # Bullet points
        elif line.startswith('- '):
            blocks.append({
                "object": "block",
                "type": "bulleted_list_item",
                "bulleted_list_item": {
                    "rich_text": [{"type": "text", "text": {"content": line[2:]}}]
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

def create_wiki_parent_page(notion):
    """Create a parent page to group all Wiki pages together"""
    
    parent_content = """# 📚 Company Knowledge Base

> Central repository for all company knowledge, processes, and documentation

This is your one-stop destination for everything related to our company. Use the navigation below to find what you need.

## 🚀 Quick Access
- [🏥 Company Wiki](./Company-Wiki) - Main Wiki hub
- [📊 Knowledge Database](./Knowledge-Database) - Direct database access

## 📁 Category Overview
- [🏢 Company](./Company-Overview) - Vision, mission, strategy
- [🚀 Product](./Product-Documentation) - Product strategy and features  
- [⚙️ Engineering](./Engineering-Resources) - Technical documentation
- [🎨 Design](./Design-Guidelines) - UX/UI standards and research
- [📈 Marketing](./Marketing-Materials) - Brand and content guidelines
- [📋 Operations](./Operations-Compliance) - SOPs and compliance

---

*This page serves as the central hub for all company knowledge. All Wiki pages are organized under this parent page for easy navigation.*
"""
    
    # Convert to blocks
    blocks = convert_markdown_to_blocks(parent_content)
    
    try:
        # Create the parent page
        parent_page = notion.pages.create(
            parent={"type": "page_id", "page_id": get_parent_page_id(notion)},
            properties={
                "title": [{"text": {"content": "Company Knowledge Base"}}]
            }
        )
        
        # Add content
        notion.blocks.children.append(
            block_id=parent_page['id'],
            children=blocks
        )
        
        print(f"✅ Created Wiki parent page: {parent_page['id']}")
        return parent_page['id']
        
    except Exception as e:
        print(f"❌ Error creating Wiki parent page: {e}")
        return None

def create_wiki_structure():
    """Main function to create the complete Wiki structure"""
    print("🚀 Starting Wiki Structure Creation...")
    
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
    
    # Create Wiki parent page
    print("\nCreating Wiki parent page...")
    parent_page_id = create_wiki_parent_page(notion)
    if not parent_page_id:
        print("❌ Failed to create Wiki parent page")
        return
    
    # Create master Wiki page
    print("\nCreating master Wiki page...")
    master_page_id = create_master_wiki_page(notion, schema, parent_page_id)
    if not master_page_id:
        print("❌ Failed to create master Wiki page")
        return
    
    # Create category landing pages
    print("\nCreating category landing pages...")
    category_pages = create_category_landing_pages(notion, schema, parent_page_id)
    
    print("\nWiki structure creation complete!")
    print(f"Parent page: {parent_page_id}")
    print(f"Master Wiki page: {master_page_id}")
    print(f"Category pages created: {len(category_pages)}")
    
    for category, page_id in category_pages.items():
        print(f"  - {category}: {page_id}")

if __name__ == "__main__":
    create_wiki_structure()
