# Knowledge as Code Workflow

This project implements a "Knowledge as Code" approach where your company knowledge base is defined in structured YAML files and automatically synced to Notion.

## 🏗️ Architecture

```
knowledge_base.yaml  →  create_knowledge_base.py  →  Notion Database
                                    ↓
                            sync_notion.py  →  ChromaDB  →  Slack Bot
```

## 📁 File Structure

- `knowledge_base.yaml` - Your knowledge base schema and content
- `lib/create_knowledge_base.py` - Creates Notion database and pages
- `lib/sync_notion.py` - Syncs Notion content to ChromaDB
- `lib/notion_rag.py` - RAG functionality for the bot

## 🚀 Quick Start

### 1. Set up your environment
```bash
# Create .env file with your API keys
cp .env.example .env
# Edit .env with your actual API keys
```

### 2. Create your knowledge base
```bash
# Create the Notion database and pages from YAML
make create-kb
```

### 3. Sync to ChromaDB
```bash
# Sync Notion content to vector database
make sync-notion
```

### 4. Start the bot
```bash
# Run the Slack bot
make run
```

## 📝 Editing Your Knowledge Base

### Structure
The `knowledge_base.yaml` file has two main sections:

1. **Database Schema** - Defines the Notion database structure
2. **Content** - Your actual knowledge base content

### Adding New Content

1. **Edit `knowledge_base.yaml`**:
   ```yaml
   content:
     company:
       vision_mission:
         - title: "New Policy Document"
           content: |
             # Your content here in Markdown
             
             ## Section 1
             - Bullet point 1
             - Bullet point 2
           category: "Company"
           subcategory: "Vision & Mission"
           department: ["Executive"]
           document_type: "Policy"
           priority: "High"
           status: "Approved"
           tags: ["policy", "strategy"]
   ```

2. **Sync to Notion**:
   ```bash
   make create-kb
   ```

3. **Update ChromaDB**:
   ```bash
   make sync-notion
   ```

### Supported Content Types

- **Headers**: `#`, `##`, `###`
- **Lists**: `- item` (bulleted), `1. item` (numbered)
- **Checkboxes**: `- [ ]` (unchecked), `- [x]` (checked)
- **Code blocks**: ```language
- **Regular text**: Paragraphs

## 🔧 Available Commands

```bash
make help              # Show all available commands
make create-kb         # Create knowledge base from YAML
make sync-notion       # Sync Notion content to ChromaDB
make run              # Start the Slack bot
make migrate          # Test ChromaDB migration
```

## 📊 Knowledge Base Categories

### Company
- Vision & Mission
- Strategy & Planning
- About & History
- Team & People

### Product
- Product Strategy
- Core Features
- Product Management

### Engineering
- Software Development
- Technical Infrastructure
- DevOps & Deployment

### Design
- User Experience
- Visual Design
- Research & Insights

### Marketing
- Brand & Messaging
- Growth & Acquisition
- Content & Communications

### Operations
- Standard Operating Procedures
- Compliance & Legal
- Business Operations

## 🎯 Benefits

1. **Version Control**: Track changes to your knowledge base
2. **Automation**: Deploy knowledge updates with a single command
3. **Consistency**: Structured format ensures consistent documentation
4. **Collaboration**: Multiple people can edit YAML files
5. **Backup**: Your knowledge is stored in code, not just in Notion

## 🔄 Workflow

1. **Edit** `knowledge_base.yaml` with new content
2. **Commit** changes to git
3. **Deploy** with `make create-kb`
4. **Sync** to ChromaDB with `make sync-notion`
5. **Test** with your Slack bot

## 🚨 Important Notes

- Always run `make create-kb` before `make sync-notion`
- The YAML file is the source of truth
- Notion database ID must be set in `.env`
- Make sure your Notion integration has proper permissions
