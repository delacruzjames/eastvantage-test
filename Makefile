PYTHON ?= python3
VENV := .venv
BIN := $(VENV)/bin
PIP := $(BIN)/pip
UVICORN := $(BIN)/uvicorn
PYTEST := $(BIN)/pytest
ALEMBIC := $(BIN)/alembic

HOST ?= 0.0.0.0
PORT ?= 8000

.DEFAULT_GOAL := help

.PHONY: help install run test migrate migrate-down docker-up docker-down docker-logs clean

help:
	@echo "make install      Create .venv and install dependencies"
	@echo "make run          Run the API locally with reload"
	@echo "make test         Run tests"
	@echo "make migrate      Apply Alembic migrations"
	@echo "make migrate-down Roll back the latest Alembic migration"
	@echo "make docker-up    Build and start with Docker Compose"
	@echo "make docker-down  Stop the Docker Compose stack"
	@echo "make docker-logs  Follow Docker logs"
	@echo "make clean        Remove Python caches"

install:
	$(PYTHON) -m venv $(VENV)
	$(PIP) install -r requirements.txt

run:
	$(UVICORN) app.main:app --reload --host $(HOST) --port $(PORT)

test:
	$(PYTEST)

migrate:
	$(ALEMBIC) upgrade head

migrate-down:
	$(ALEMBIC) downgrade -1

docker-up:
	docker compose up --build

docker-down:
	docker compose down

docker-logs:
	docker compose logs -f

clean:
	find . -type d -name __pycache__ -not -path './.venv/*' -exec rm -rf {} +
	rm -rf .pytest_cache
