include .env

# Knowledge Base Management
create-kb:
	$(VENV_PATH)/Scripts/python.exe lib/create_knowledge_base.py

create-kb-linux:
	$(VENV_PATH)/bin/python3 lib/create_knowledge_base.py

create-wiki:
	$(VENV_PATH)/Scripts/python.exe lib/create_wiki_structure.py

create-wiki-linux:
	$(VENV_PATH)/bin/python3 lib/create_wiki_structure.py

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
	@echo "  create-wiki   - Create hierarchical Wiki structure in Notion"
	@echo "  sync-notion   - Sync existing Notion content to ChromaDB"
	@echo "  run          - Start the Slack bot"
	@echo "  migrate      - Test ChromaDB migration"
	@echo "  help         - Show this help message"



DOCKER_REGISTRY=$(AWS_ACCOUNT_ID).dkr.ecr.$(AWS_REGION).amazonaws.com


# Docker
auth:
	aws ecr get-login-password --region $(AWS_REGION) | docker login --username AWS --password-stdin $(DOCKER_REGISTRY)

create-repo:
	aws ecr create-repository --repository-name $(C_SUITE_IMAGE) --region $(AWS_REGION) || true

docker:
	docker build --build-arg PORT=$(PORT) -t $(DOCKER_REGISTRY)/$(C_SUITE_IMAGE):$(C_SUITE_VERSION) -f Dockerfile .
	docker push $(DOCKER_REGISTRY)/$(C_SUITE_IMAGE):$(C_SUITE_VERSION)
	kubectl rollout restart deployment $(DEPLOYMENT) --namespace=$(NAMESPACE)


OPENAI_SECRET=--from-literal=C_SUITE_OPENAI_API_KEY=$(OPENAI_API_KEY)
NOTION_SECRETS=--from-literal=C_SUITE_NOTION_API_TOKEN=$(NOTION_API_TOKEN)
CHROMA_SECRETS=--from-literal=C_SUITE_CHROMA_TENANT=$(CHROMA_TENANT) --from-literal=C_SUITE_CHROMA_API_KEY=$(CHROMA_API_KEY)
SLACK_SECRETS=--from-literal=C_SUITE_SLACK_BOT_TOKEN=$(SLACK_BOT_TOKEN) --from-literal=C_SUITE_SLACK_APP_TOKEN=$(SLACK_APP_TOKEN)
SECRETS=$(SLACK_SECRETS) $(NOTION_SECRETS) $(CHROMA_SECRETS) $(OPENAI_SECRET)

secrets:
	kubectl create secret generic app-secrets --namespace $(NAMESPACE) $(SECRETS)

update-secrets:
	kubectl create secret generic app-secrets --namespace $(NAMESPACE) $(SECRETS) --dry-run=client -o yaml | kubectl apply -f -
