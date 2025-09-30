import os
import json

import dotenv

dotenv.load_dotenv()

SLACK_BOT_TOKEN = os.environ.get("SLACK_BOT_TOKEN")
SLACK_APP_TOKEN = os.environ.get("SLACK_APP_TOKEN")
OPENAI_API_KEY = os.environ.get("OPENAI_API_KEY")
NOTION_API_TOKEN = os.environ.get("NOTION_API_TOKEN")
NOTION_DATABASE_ID = os.environ.get("NOTION_DATABASE_ID")
CHROMA_DB_PATH = "./notion_db" # Path to store ChromaDB data
CHROMA_COLLECTION_NAME = "notion-knowledge-base"

PERSONAS = json.loads(open("personas.json").read())

GPT_MODEL = os.environ.get("GPT_MODEL", "gpt-4.1-nano") # Default to gpt-4.1-nano if not set

NOTION_DOCUMENTATION_DB_ID = os.environ.get("NOTION_DOCUMENTATION_DB_ID")
