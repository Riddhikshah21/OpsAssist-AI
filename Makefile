.PHONY: install dev stop backend frontend ingest eval test lint clean

install:
	uv sync

dev:
	docker compose up -d

stop:
	docker compose down

backend:
	uv run uvicorn app.main:app --reload

frontend:
	uv run streamlit run frontend/streamlit_app.py

ingest:
	uv run python -m scripts.ingest_docs

eval:
	uv run python -m scripts.run_eval

test:
	uv run pytest -v

lint:
	uv run ruff check .

clean:
	find . -type d -name "__pycache__" -exec rm -rf {} +
	find . -type d -name ".pytest_cache" -exec rm -rf {} +
	find . -type d -name ".ruff_cache" -exec rm -rf {} +