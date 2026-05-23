import os
import json

import dotenv

dotenv.load_dotenv()

SLACK_BOT_TOKEN = os.environ.get("SLACK_BOT_TOKEN")
SLACK_APP_TOKEN = os.environ.get("SLACK_APP_TOKEN")
OPENAI_API_KEY = os.environ.get("OPENAI_API_KEY")
NOTION_API_TOKEN = os.environ.get("NOTION_API_TOKEN")
NOTION_DATABASE_ID = os.environ.get("NOTION_DATABASE_ID")

CHROMA_TENANT = os.environ.get("CHROMA_TENANT", "default_tenant")
CHROMA_API_KEY = os.environ.get("CHROMA_API_KEY", "default_chroma_api_key")
CHROMA_DB_PATH = "./notion_db" # Path to store ChromaDB data
CHROMA_COLLECTION_NAME = "notion-knowledge-base"

PERSONAS = json.loads(open("personas.json").read())

GPT_MODEL = os.environ.get("GPT_MODEL", "gpt-4.1-nano") # Default to gpt-4.1-nano if not set

NOTION_DOCUMENTATION_DB_ID = os.environ.get("NOTION_DOCUMENTATION_DB_ID")


def utility_for_validating_env_vars():
    print("Validating environment variables...")
    print(len(SLACK_BOT_TOKEN), len(SLACK_APP_TOKEN), len(OPENAI_API_KEY), len(NOTION_API_TOKEN), len(NOTION_DATABASE_ID))
    # 57 97 51 50 32
    print(len(CHROMA_API_KEY), len(CHROMA_TENANT))
    # 47, 36
    
    if not all([SLACK_BOT_TOKEN, SLACK_APP_TOKEN, OPENAI_API_KEY, NOTION_API_TOKEN, NOTION_DATABASE_ID, CHROMA_API_KEY, CHROMA_TENANT]):
        raise EnvironmentError("One or more required environment variables are missing.")
    
    assert len(SLACK_BOT_TOKEN) == 57, "SLACK_BOT_TOKEN length mismatch"
    # SLACK_BOT_TOKEN=xoxb-
    assert SLACK_BOT_TOKEN.startswith("xoxb-"), "SLACK_BOT_TOKEN format incorrect"

    assert len(SLACK_APP_TOKEN) == 97, "SLACK_APP_TOKEN length mismatch"
    # SLACK_APP_TOKEN=xapp-
    assert SLACK_APP_TOKEN.startswith("xapp-"), "SLACK_APP_TOKEN format incorrect"

    assert len(OPENAI_API_KEY) == 51, "OPENAI_API_KEY length mismatch"
    # OPENAI_API_KEY=sk-
    assert OPENAI_API_KEY.startswith("sk-"), "OPENAI_API_KEY format incorrect"

    assert len(NOTION_API_TOKEN) == 50, "NOTION_API_TOKEN length mismatch"
    # NOTION_API_TOKEN=ntn_
    assert NOTION_API_TOKEN.startswith("ntn_"), "NOTION_API_TOKEN format incorrect"

    assert len(NOTION_DATABASE_ID) == 32, "NOTION_DATABASE_ID length mismatch"

    assert len(CHROMA_API_KEY) == 47, "CHROMA_API_KEY length mismatch"
    # CHROMA_API_KEY=ck-
    assert CHROMA_API_KEY.startswith("ck-"), "CHROMA_API_KEY format incorrect"

    assert len(CHROMA_TENANT) == 36, "CHROMA_TENANT length mismatch"
    
    print("All required environment variables are set correctly.")

utility_for_validating_env_vars()


mcp_config = json.loads(open("mcp_config.json").read())
