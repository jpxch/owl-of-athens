API_DIR := api
WEB_DIR := web

API_HOST ?= 0.0.0.0
API_PORT ?= 8010

.PHONY: install api-install web-install api-dev web-dev web-build api-test web-lint dev lint test clean

install: api-install web-install

api-install:
	cd $(API_DIR) && uv sync

web-install:
	cd $(WEB_DIR) && pnpm install

api-dev:
	cd $(API_DIR) && uv run uvicorn main:app --reload --host $(API_HOST) --port $(API_PORT)

web-dev:
	cd $(WEB_DIR) && pnpm dev

web-build:
	cd $(WEB_DIR) && pnpm build

dev:
	$(MAKE) -j2 api-dev web-dev

api-test:
	cd $(API_DIR) && uv run pytest

test: api-test

web-lint:
	cd $(WEB_DIR) && pnpm lint

lint: web-lint
	@echo "Skipping API lint: no Python linter is configured in api/pyproject.toml yet."

clean:
	rm -rf $(API_DIR)/.venv
	rm -rf $(WEB_DIR)/node_modules
	rm -rf $(WEB_DIR)/.next
