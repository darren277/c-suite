include .env

# Knowledge Base Management
create-kb:
	$(VENV_PATH)/Scripts/python.exe lib/create_knowledge_base.py

create-kb-linux:
	$(VENV_PATH)/bin/python3 lib/create_knowledge_base.py

sync-notion:
	$(VENV_PATH)/Scripts/python.exe lib/sync_notion.py

sync-notion-linux:
	$(VENV_PATH)/bin/python3 lib/sync_notion.py

# Application
run:
	$(VENV_PATH)/Scripts/python.exe main.py

run-linux:
	$(VENV_PATH)/bin/python3 main.py

# Migration
migrate:
	$(VENV_PATH)/Scripts/python.exe migrate.py

migrate-linux:
	$(VENV_PATH)/bin/python3 migrate.py

# Help
help:
	@echo "Available commands:"
	@echo "  create-kb     - Create knowledge base from knowledge_base.yaml"
	@echo "  sync-notion   - Sync existing Notion content to ChromaDB"
	@echo "  run          - Start the Slack bot"
	@echo "  migrate      - Test ChromaDB migration"
	@echo "  help         - Show this help message"
