# Owl of Athens

Owl of Athens is a local-first AI learning engine designed to guide a learner through a structured loop:

goal → lesson → response → evaluation

---

## What This Is

Owl of Athens is not a chatbot.

It is a teaching system built around a core loop:

1. A learner provides a goal
2. The system generates a structured lesson
3. The learner completes a task
4. The system evaluates the response
5. Feedback determines the next step

The focus is not conversation — it is progression.

---

## System Architecture

- API (`api/`)
  - FastAPI backend
  - Orchestration layer
  - Validation (schema enforcement)
  - Future persistence

- Atlas (`atlas`)
  - Model inference layer
  - LLM execution (OpenAI / local models)

- Web (`web/`)
  - Next.js frontend
  - Learner interface

- Contracts (`core/contracts/`)
  - Lesson schema
  - Evaluation schema
  - Atlas interface contract

---

## Runtime Model

- API runs on: continuum-mini
- Model execution runs on: atlas
- Communication: HTTP (JSON)
- Configuration: environment-driven

---

## Local Development

Start the API:

    make api-dev

Default URL:

    http://localhost:8010

Health check:

    GET /health

Start the web app:

    make web-dev

---

## Project Structure

    api/              FastAPI backend
    web/              Next.js frontend
    core/contracts/   system contracts (lesson, evaluation, atlas)
    atlas-runtime/    future inference service
    infra/            deployment + environment

---

## Current Status

Phase: 0.5 — Spine Preparation

What exists:

- Contracts defined (lesson + evaluation)
- Atlas runtime contract stub
- Backend bootstrapped (FastAPI + config)
- Local development workflow

What is not built yet:

- Lesson generation endpoint
- Evaluation endpoint
- Database / persistence
- Curriculum logic

---

## Goal of Phase 0.5

Prove the core loop works:

Can a learner input a goal and receive:

- a clear lesson
- a meaningful task
- actionable feedback

If this loop fails, the system fails.

---

## Next Steps

- Implement POST /generate-lesson
- Implement POST /evaluate-response
- Validate outputs against contracts
- Test the loop manually end-to-end

---

## Design Principle

Build the smallest possible working teaching loop first.

Do not optimize for:

- multi-user systems
- adaptive learning
- curriculum graphs

until the core experience feels correct.