# Project: Owl of Athens
API_DIR=api
WEB_DIR=web

# API (FastAPI)
api-install:
	cd $(API_DIR) && uv sync

api-dev:
	cd $(API_DIR) && uv run uvicorn main:app --reload --host 0.0.0.0 --port 8010

api-test:
	cd $(API_DIR) && uv run pytest

# Web (Next.js)
web-install:
	cd $(WEB_DIR) && pnpm install

web-dev:
	cd $(WEB_DIR) && pnpm dev

web-build:
	cd $(WEB_DIR) && pnpm build

# Full Stack
dev:
	make -j2 api-dev web-dev

# Quality
lint:
	cd $(API_DIR) && uv run ruff check .
	cd $(WEB_DIR) && pnpm lint

# Clean
clean:
	rm -rf $(API_DIR)/.venv
	rm -rf $(WEB_DIR)/node_modules
	rm -rf $(WEB_DIR)/.next