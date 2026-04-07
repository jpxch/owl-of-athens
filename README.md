# Owl of Athens

Owl of Athens is a local-first AI learning engine built around one tight loop:

goal -> lesson -> response -> evaluation

It is not a chatbot. The system is designed to teach one concrete step at a time, evaluate the learner's response, and suggest what should happen next.

## Current State

The teaching-loop spine is implemented today:

- `GET /health`
- `POST /generate-lesson`
- `POST /evaluate-response`
- schema-backed provider validation for lessons and evaluations
- a learner-facing Next.js flow for goal entry, lesson review, response submission, and evaluation display

The current milestone is to harden and verify that loop end to end before starting persistence, adaptive curriculum work, or broader product scope.

## Project Structure

```text
api/              FastAPI backend and provider orchestration
web/              Next.js learner interface
core/contracts/   canonical lesson and evaluation schemas
atlas-runtime/    future inference runtime work
infra/            environment and deployment support
```

## Local Development

From the repo root:

```bash
make api-dev
make web-dev
```

Default local URLs:

- API: `http://localhost:8010`
- Web: `http://localhost:3000`

## Environment

The repo expects configuration in `.env` for the API and optionally `.env.local` for the web app.

Common variables:

- `DATABASE_URL`
- `MODEL_PROVIDER`
- `OPENAI_API_KEY`
- `OPENAI_MODEL`
- `ATLAS_BASE_URL`
- `OLLAMA_BASE_URL`
- `NEXT_PUBLIC_API_BASE_URL`

If `NEXT_PUBLIC_API_BASE_URL` is unset, the web app falls back to `http://localhost:8010`.

## Verification

Typical local checks:

```bash
cd api && uv run pytest
cd web && pnpm lint
cd web && pnpm exec tsc --noEmit
```

## Design Principle

Build the smallest believable teaching loop first.

Keep the product focused on:

- clear lesson generation
- constrained learner tasks
- actionable evaluation feedback

Defer persistence, multi-user state, and adaptive curriculum systems until the core loop feels reliable.
