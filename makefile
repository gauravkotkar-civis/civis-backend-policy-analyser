#!/usr/bin/env bash
SHELL := $(shell which bash)
VIRTUAL_ENV = .venv

##@ Utility
.PHONY: help
help:  ## Display this help
	@awk 'BEGIN {FS = ":.*##"; printf "\nUsage:\n  make <target>\033[36m\033[0m\n"} /^[a-zA-Z_-]+:.*?##/ { printf "  \033[36m%-15s\033[0m %s\n", $$1, $$2 } /^##@/ { printf "\n\033[1m%s\033[0m\n", substr($$0, 5) } ' $(MAKEFILE_LIST)

.PHONY: venv
venv: uv
	uv venv --python 3.13.3 ${VIRTUAL_ENV}; \
	source ${VIRTUAL_ENV}/bin/activate; \
	uv lock; \
	make install && make dev; \
	uv pip compile pyproject.toml -o requirements.txt

.PHONY: uv
uv:  ## Install uv if it's not present.
	@command -v uv > /dev/null 2>&1 || curl -LsSf https://astral.sh/uv/install.sh | sh
	uv --version

.PHONY: dev
dev: uv ## Install dev dependencies
	source ${VIRTUAL_ENV}/bin/activate;
	uv sync --dev

.PHONY: lock
lock: uv ## lock dependencies
	uv lock

.PHONY: install
install: uv ## Install dependencies
	source ${VIRTUAL_ENV}/bin/activate;
	uv sync --active

.PHONY: test
test:  ## Run tests
	uv run pytest

.PHONY: lint
lint:  ## Run linters
	uv run ruff check ./src ./tests

.PHONY: fix
fix:  ## Fix lint errors
	uv run ruff check ./src ./tests --fix
	uv run ruff format ./src ./tests

.PHONY: cov
cov: ## Run tests with coverage
	uv run pytest --cov=src --cov-report=term-missing

.PHONY: run
run:  ## Run the FastAPI app
	uv run uvicorn civis_backend_policy_analyser.api.app:app --reload

.PHONY: db-up db-down db-logs db-psql

db-up:
	docker compose up -d

db-down:
	docker compose down

db-logs:
	docker compose logs -f civis_postgres_container

db-psql:
	docker exec -it civis_postgres_container psql -U ffg -d civis

seed:
	poetry run python seed_data.py