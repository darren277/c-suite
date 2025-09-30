include .env

# Knowledge Base Management
create-kb:
	.venv/Scripts/python.exe lib/create_knowledge_base.py

create-kb-linux:
	.venv/bin/python3 lib/create_knowledge_base.py

sync-notion:
	.venv/Scripts/python.exe lib/sync_notion.py

sync-notion-linux:
	.venv/bin/python3 lib/sync_notion.py

# Application
run:
	.venv/Scripts/python.exe main.py

run-linux:
	.venv/bin/python3 main.py

# Migration
migrate:
	.venv/Scripts/python.exe migrate.py

migrate-linux:
	.venv/bin/python3 migrate.py

# Help
help:
	@echo "Available commands:"
	@echo "  create-kb     - Create knowledge base from knowledge_base.yaml"
	@echo "  sync-notion   - Sync existing Notion content to ChromaDB"
	@echo "  run          - Start the Slack bot"
	@echo "  migrate      - Test ChromaDB migration"
	@echo "  help         - Show this help message"
