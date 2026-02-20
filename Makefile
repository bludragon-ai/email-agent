.PHONY: install dev test lint run docker-up docker-down

install:
	pip install -e .

dev:
	pip install -e ".[dev]"

test:
	pytest -v --tb=short

lint:
	ruff check src/ tests/

run:
	streamlit run src/ui/app.py --server.port=8503

docker-up:
	docker compose up --build -d

docker-down:
	docker compose down
