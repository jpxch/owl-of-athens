# Owl of Athens Roadmap

Last updated: 2026-04-06

## Purpose (Grounding Contract)

This file is the source-of-truth context for ongoing work on this project.

- `owl-of-athens` is a local-first AI learning engine built around the loop `goal -> lesson -> response -> evaluation`.
- It is not a chatbot, a one-off lesson generator, or a coding-only tutor.
- Scope includes:
  - structured lesson generation from learner goals
  - learner response evaluation with next-step guidance
  - a minimal learner-facing web flow for the teaching loop
- The project owns contracts, backend APIs, frontend flow, provider orchestration, and future persistence.
- Keep phase status aligned with real code, docs, and the current working tree.

## Deployment Target (Current)

- Primary runtime target is a local/dev split between the FastAPI API and the Next.js web app.
- Runtime configuration remains environment-driven (`DATABASE_URL`, `MODEL_PROVIDER`, `OPENAI_API_KEY`, `ATLAS_BASE_URL`, `OLLAMA_BASE_URL`).
- Keep deployment docs environment-specific, but keep code paths portable where possible.

## Verified Status Snapshot

Validated from the repo and current working tree on 2026-04-06 unless otherwise noted:

- `git status --short` is dirty:
  - `ROADMAP.md` modified as part of this refresh
  - `.codex` untracked
- Active branch is `feature/teaching-loop-spine`.
- `git log -1 --oneline` reports `5e0e05e` (`feat: enhance lesson generation UI and add evaluation feedback components`).
- `.env.example` exists and the repo expects:
  - `DATABASE_URL`
  - `MODEL_PROVIDER`
  - `OPENAI_API_KEY`
  - `ATLAS_BASE_URL`
  - `OLLAMA_BASE_URL`
- Core backend entrypoints exist and are currently wired through:
  - `api/main.py`
  - `api/app/api/routes/lesson.py`
  - `api/app/api/routes/evaluation.py`
- Shared provider and config layers exist for:
  - environment-driven settings in `api/app/core/config.py`
  - schema-backed OpenAI generation/evaluation in `api/app/services/provider.py`
- The repo currently includes tests for:
  - `api/tests/test_health.py`
- Current docs status:
  - `README.md` describes the project, core loop, architecture, and local dev entrypoints
  - `web/README.md` is still the default Next.js starter README
  - `api/README.md` is empty
- Current runtime verification:
  - `api/main.py` exposes `GET /health`
  - the API mounts `POST /generate-lesson` and `POST /evaluate-response`
  - `web/src/app/page.tsx` implements a basic goal -> lesson -> response -> feedback flow
- Current local verification:
  - `uv run pytest` in `api/` could not complete in this sandbox because `uv` could not create its cache/lock temp files on the read-only cache path
  - `pnpm lint` in `web/` could not complete in this environment because `eslint` failed to load `libatomic.so.1`
- Remaining visible gaps:
  - provider model selection is hardcoded instead of fully env-driven
  - empty-input/provider validation paths are not normalized into clear 4xx API errors
  - route/provider contract tests do not exist yet
  - frontend API base URL is hardcoded in the page
  - no recorded live end-to-end lesson/evaluation verification exists yet
  - no persistence models or migrations are implemented yet

Implemented APIs / Interfaces:

- `GET /health`
- `POST /generate-lesson`
- `POST /evaluate-response`

Implemented core services / modules:

- API surface:
  - `api/main.py`
  - `api/app/api/routes/lesson.py`
  - `api/app/api/routes/evaluation.py`
- Contracts and request models:
  - `core/contracts/lesson.schema.json`
  - `core/contracts/evaluation.schema.json`
  - `core/contracts/atlas.contract.md`
  - `api/app/api/models/requests.py`
  - `api/app/api/models/lesson.py`
- Provider/config:
  - `api/app/services/provider.py`
  - `api/app/core/config.py`
- Frontend:
  - `web/src/app/page.tsx`
  - `web/src/app/layout.tsx`

Current system direction:
The minimal teaching loop skeleton is now real in both the API and the web app. The immediate gap is not basic scaffolding anymore, but proving the spine: tighten the contracts and error paths, remove the remaining hardcoded config, add route/provider tests, and complete one real end-to-end lesson/evaluation run before moving into persistence or broader product work.

## Git Status And Direction

Current git status:

- Active branch: `feature/teaching-loop-spine`
- Working tree: dirty because this roadmap refresh is in progress and `.codex` is untracked
- Latest commit before this roadmap refresh: `5e0e05e` (`feat: enhance lesson generation UI and add evaluation feedback components`)

Required direction:

1. Finish Phase 1 spine hardening before adding persistence or broader product scope.
2. Make provider behavior fully env-driven and contract-aligned.
3. Add the first real backend tests for lesson/evaluation route and provider paths.
4. Remove remaining hardcoded frontend configuration and default starter docs/metadata.

## Reality-Checked Phase Status

| Phase | Name | Status | Notes |
|---|---|---|---|
| 0 | Foundation | Complete | FastAPI, Next.js, contracts, config, Makefile, and root docs exist in usable baseline form. |
| 1 | Core Platform | In Progress | The teaching loop spine exists, but backend hardening, route/provider tests, and live verification are still missing. |
| 2 | Main Product Surface | In Progress | A minimal learner page exists, but it still uses a hardcoded API base URL and default app metadata/docs remain. |
| 3 | Stabilization | Not Started | No serious route/provider coverage or end-to-end verification baseline yet. |
| 4 | Consumer Contracts | In Progress | Lesson/evaluation schemas and request models exist with UUID-shaped `lesson_id` enforcement, but broader route/provider contract coverage is still missing. |
| 5 | Persistence Layer | Not Started | Dependencies are present, but no models, migrations, or DB wiring exist. |
| 6 | Atlas / Provider Expansion | Not Started | `atlas.contract.md` is a stub and the provider path is OpenAI-only today. |
| 7 | Automation / Lifecycle | Not Started | No deployment/sync scripts or branch/release automation checked in. |
| 8 | Testing & Data Quality | Not Started | Only a health smoke test exists. |
| 9 | Hardening & Operations | Not Started | No observability, deployment verification, or operational playbooks yet. |
| 10 | Future / Advanced Work | Not Started | Adaptive learning, multi-user state, and curriculum depth remain intentionally deferred. |

## Next Milestone Checklist

### Suggested Immediate Next Step

- [x] Refresh the roadmap against the actual repo state
- [x] Enforce UUID-shaped `lesson_id` across contracts and models
- [ ] Move provider model selection into settings/env
- [ ] Normalize invalid input and provider validation failures into predictable API errors
- [ ] Add focused route/provider tests
- [ ] Record a real local lesson/evaluation verification run

### Phase 1 Kickoff (Teaching Loop Spine Hardening)

- [x] Tighten `lesson.schema.json` and `evaluation.schema.json` identifier validation
- [x] Align Pydantic lesson/request models with the tighter contract
- [ ] Replace hardcoded provider model selection with config-driven selection
- [ ] Add route/provider tests beyond `api/tests/test_health.py`

### Phase 2 Closure (Minimal Learner Surface)

- [x] Replace the default Next.js starter page with a learner flow
- [x] Support goal entry, lesson display, response submission, and feedback display
- [ ] Move the frontend API base URL out of `web/src/app/page.tsx`
- [ ] Replace default app metadata and starter README content with project-specific docs

### Phase 3 Stabilization (Spine Proof)

- [ ] Run one real end-to-end goal -> lesson -> response -> evaluation flow
- [ ] Verify malformed model output fails safely and visibly
- [ ] Verify empty/invalid request paths return clear client-facing errors
- [ ] Re-run backend/frontend verification in a working local environment

### Phase 4 Kickoff (Persistence)

- [ ] Initialize Alembic
- [ ] Add `learner`, `goal`, `lesson`, and `attempt` models
- [ ] Persist generate/evaluate workflow state
- [ ] Re-run the proven teaching loop with persistence enabled

### Phase N Gate (Pre-Expansion)

- [ ] Testing baseline covers health, lesson generation, and evaluation paths
- [ ] Contracts, models, and provider behavior stay aligned
- [ ] Docs reflect the real local dev workflow for both `api/` and `web/`
- [ ] Runtime verification is recorded before starting adaptive/multi-user work

## Git Workflow Guardrails

Use this workflow for every roadmap item unless explicitly overridden:

- [ ] Create work only on topic branches (`feature/*`, `fix/*`, `chore/*`, `docs/*`).
- [ ] Keep branch scope aligned to one roadmap unit.
- [ ] Rebase or merge `main` before finalizing work.
- [ ] Open a PR for every branch with purpose, verification, and deferred follow-ups.
- [ ] Require passing checks before merge.
- [ ] Prefer squash merge unless there is a reason not to.
- [ ] Delete merged branches after merge.
- [ ] Tag significant milestones on `main`.
- [ ] If scope changes mid-branch, cut a new branch for unrelated work.
