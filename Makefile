include .env

sync-notion:
	.venv/Scripts/python.exe lib/sync_notion.py

run:
	.venv/Scripts/python.exe main.py

migrate:
	.venv/Scripts/python.exe migrate.py
