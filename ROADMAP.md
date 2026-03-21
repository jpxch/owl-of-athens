# Owl of Athens Roadmap

Last updated: 2026-03-21

## Purpose (Grounding Contract)

This file is the source-of-truth context for ongoing ChatGPT/Codex sessions.

- `owl-of-athens` is a local-first AI learning engine.
- It is not just a chatbot, a one-off lesson generator, or a coding-only tutor.
- The system owns:
  - goal-to-curriculum planning
  - lesson delivery and progression
  - assessment, misconception tracking, and adaptation
  - learner state, progress history, and multi-user coordination
- Runtime shape is intentionally split:
  - `continuum-mini` is the primary backend/server host
  - `atlas` is the intended heavy AI runtime / graphics host
  - `/mnt/continuum/Projects/owl-of-athens` is the canonical shared source repo
- Keep phase status aligned with the real code in the repo and current working tree.

## Deployment Target (Current)

- Canonical source repo lives at `/mnt/continuum/Projects/owl-of-athens`.
- Shared bare Git remote lives at `/mnt/continuum/git/owl-of-athens.git`.
- Primary backend/runtime target is `continuum-mini` (`192.168.0.74`, Tailscale `100.95.103.102`).
- Intended AI/graphics runtime target is `atlas` (reachable from `continuum-mini` over Tailscale at `100.80.245.114`).
- Keep runtime config environment-driven:
  - `DATABASE_URL`
  - `API_HOST`
  - `API_PORT`
  - `MODEL_PROVIDER`
  - `ATLAS_BASE_URL`
  - `OPENAI_API_KEY`
  - `OLLAMA_BASE_URL`

## Verified Status Snapshot

Validated in this workspace on 2026-03-21 unless otherwise noted:

- `git rev-parse --is-inside-work-tree` returns `true`.
- Active branch is `main`.
- `git log -1 --oneline` currently fails because `main` has no commits yet.
- `git remote -v` reports:
  - `origin /mnt/continuum/git/owl-of-athens.git (fetch)`
  - `origin /mnt/continuum/git/owl-of-athens.git (push)`
- `git status --short` currently shows only untracked scaffold files; the initial bootstrap commit has not happened yet.
- Root scaffold exists:
  - `.mise.toml`
  - `.gitignore`
  - `.env.example`
  - `README.md`
  - `Makefile`
  - `ROADMAP.md`
- `.mise.toml` is populated and pins:
  - `python = "3.14"`
  - `node = "25"`
  - `pnpm = "10"`
  - `uv = "latest"`
- Root docs/config files are still mostly placeholders:
  - `.gitignore` is currently empty
  - `.env.example` is currently empty
  - `README.md` is currently empty
  - `Makefile` is currently empty
- Backend scaffold exists under `api/`:
  - `api/pyproject.toml`
  - `api/main.py`
  - `api/app/api`
  - `api/app/core`
  - `api/app/db`
  - `api/app/models`
  - `api/app/schemas`
  - `api/app/services`
  - `api/tests`
- `api/pyproject.toml` includes the planned backend baseline dependencies:
  - `fastapi`
  - `sqlalchemy`
  - `alembic`
  - `pydantic-settings`
  - `psycopg`
  - `httpx`
  - `openai`
  - `uvicorn`
  - `pytest`
- `api/main.py` is still the default placeholder and does not yet expose a FastAPI app.
- Frontend scaffold exists under `web/`:
  - `web/package.json`
  - `web/src/app`
  - `web/next.config.ts`
  - `web/eslint.config.mjs`
  - `web/postcss.config.mjs`
  - `web/tsconfig.json`
- `web/package.json` confirms the current frontend baseline:
  - `next` `16.2.1`
  - `react` `19.2.4`
  - `react-dom` `19.2.4`
  - `eslint`
  - `eslint-config-next`
  - `tailwindcss`
  - `babel-plugin-react-compiler`
- `web/README.md` is still the default `create-next-app` README.
- Shared structure exists, but is still empty:
  - `atlas-runtime/`
  - `core/contracts/`
  - `core/prompts/`
  - `core/seeds/`
  - `infra/env/`
  - `infra/podman/`
  - `infra/systemd/`
  - `docs/`
  - `scripts/`
- No verified database models, Alembic environment, HTTP routes, application config module, deployment scripts, or product tests exist yet.

Current repo tree snapshot:

```text
.
├── .env.example
├── .gitignore
├── .mise.toml
├── Makefile
├── README.md
├── ROADMAP.md
├── api
│   ├── app
│   │   ├── api
│   │   ├── core
│   │   ├── db
│   │   ├── models
│   │   ├── schemas
│   │   └── services
│   ├── main.py
│   ├── pyproject.toml
│   ├── README.md
│   ├── tests
│   └── uv.lock
├── atlas-runtime
├── core
│   ├── contracts
│   ├── prompts
│   └── seeds
├── docs
├── infra
│   ├── env
│   ├── podman
│   └── systemd
├── scripts
└── web
    ├── eslint.config.mjs
    ├── next.config.ts
    ├── next-env.d.ts
    ├── package.json
    ├── pnpm-workspace.yaml
    ├── postcss.config.mjs
    ├── public
    ├── README.md
    ├── src
    │   └── app
    └── tsconfig.json
```

Implemented project surfaces:

- Repo/tooling baseline:
  - `.mise.toml`
  - Git repo on `main`
  - shared bare remote at `/mnt/continuum/git/owl-of-athens.git`
- Backend scaffold:
  - `api/pyproject.toml`
  - `api/main.py`
  - `api/app/*` package layout
  - `api/tests/`
- Frontend scaffold:
  - `web/package.json`
  - `web/src/app`
  - `web/eslint.config.mjs`
  - `web/next.config.ts`
  - `web/postcss.config.mjs`
  - `web/tsconfig.json`
- Shared runtime scaffolding:
  - `atlas-runtime/`
  - `core/`
  - `infra/`
  - `docs/`
  - `scripts/`

Current runtime path is still only scaffold-level. There is no verified API server, DB lifecycle, model-provider integration, or deployment automation yet.

## Git Status And Direction

Current git status:

- Active branch: `main`
- Remote: `origin -> /mnt/continuum/git/owl-of-athens.git`
- Working tree: scaffold files exist but are still untracked and uncommitted
- Latest commit on branch: none yet

Required direction:

1. Make the first bootstrap commit so roadmap claims attach to a real repo baseline.
2. Populate `.gitignore`, `.env.example`, `README.md`, and `Makefile` with real project conventions.
3. Replace `api/main.py` placeholder output with a real FastAPI app entrypoint and config module.
4. Initialize Alembic and define the first persistence model slice: learner, goal, lesson, attempt.
5. Replace the default Next.js starter UI with an Owl of Athens app shell.
6. Define the contract between `continuum-mini` API services and future `atlas-runtime` inference services.
7. Keep the first milestone limited to one end-to-end learner flow before expanding into collaboration, adaptation, or local inference complexity.
8. Add deployment sync scripts so each machine can copy only the runtime slice it needs from the canonical repo.

## Reality-Checked Phase Status

| Phase | Name | Status | Notes |
|---|---|---|---|
| 0 | Foundation | In Progress | Git repo, shared bare remote, mise toolchain file, backend dependency baseline, and Next.js app scaffold exist. Root docs, app runtime, migrations, and service scripts are still missing. |
| 1 | Teaching Loop MVP | Not Started | No verified goal -> lesson -> response -> evaluation flow exists yet. |
| 2 | Course Generation | Not Started | No curriculum planner or dependency-aware course structure exists yet. |
| 3 | Assessment Engine | Not Started | No grading, rubric evaluation, or feedback persistence exists yet. |
| 4 | Adaptive Learning Engine | Not Started | No mastery model, review policy, or dynamic lesson-branching rules exist yet. |
| 5 | Learner State And Multi-User | Not Started | No learner profiles, sync model, or shared-session semantics exist yet. |
| 6 | Learning Modes Expansion | Not Started | `explain`, `drill`, `challenge`, and `project` should wait until the default course loop is stable. |
| 7 | Misconception Tracking | Not Started | No error taxonomy or repeated-mistake tracking exists yet. |
| 8 | Model Provider Layer | Not Started | OpenAI is present as a dependency, and `atlas-runtime/` exists, but no provider abstraction or runtime integration exists yet. |
| 9 | Learner Experience UI | In Progress | Next.js App Router scaffold exists, but it is still the default starter and not yet an Owl of Athens product UI. |
| 10 | Knowledge And Mastery Tracking | Not Started | No durable mastery map, topic state, or progression projection exists yet. |
| 11 | Domain Expansion | Not Started | Multi-domain content should begin after one excellent domain proves the core loop. |

## Next Milestone Checklist

### Phase 0 Closure (Foundation)

- [x] Initialize Git repository
- [x] Create shared bare remote under `/mnt/continuum/git/owl-of-athens.git`
- [x] Add `.mise.toml` for shared toolchain management
- [x] Scaffold `api/`, `web/`, `core/`, `atlas-runtime/`, `infra/`, `docs/`, `scripts/`
- [ ] Commit the initial scaffold to `main`
- [ ] Populate `.gitignore`
- [ ] Populate `.env.example`
- [ ] Populate root `README.md`
- [ ] Populate root `Makefile`
- [ ] Add backend app config module
- [ ] Add FastAPI app bootstrap
- [ ] Initialize Alembic environment

### Phase 1 Kickoff (Teaching Loop MVP)

- [ ] Add learner and goal creation flow
- [ ] Add lesson-generation request endpoint
- [ ] Generate one structured lesson payload from a goal
- [ ] Render lesson content in the UI
- [ ] Accept learner submission for one lesson step
- [ ] Return evaluation plus next-step recommendation
- [ ] Persist learner attempt and lesson outcome

### Phase 2 Kickoff (Course Generation)

- [ ] Define canonical curriculum schema: course, unit, lesson, prerequisites
- [ ] Generate multi-lesson plans from user goals
- [ ] Persist generated curricula
- [ ] Add lesson unlocking / progression rules
- [ ] Support at least one concrete domain end to end

### Phase 3 Kickoff (Assessment Engine)

- [ ] Support objective checks for quiz-style prompts
- [ ] Support rubric-based evaluation for open-ended responses
- [ ] Persist assessment rationale and learner-visible feedback
- [ ] Separate learner-facing feedback from system/internal grading metadata
- [ ] Add failure-path handling for malformed model output

### Phase 8 Kickoff (Model Provider Layer)

- [ ] Define provider interface for hosted and local model backends
- [ ] Add OpenAI provider baseline
- [ ] Add `atlas-runtime` service contract
- [ ] Keep `atlas-runtime` and API contract environment-driven
- [ ] Add structured-output validation around all model responses

### Phase 9 Kickoff (Learner Experience UI)

- [ ] Replace default starter page with product shell
- [ ] Add goal entry view
- [ ] Add lesson display view
- [ ] Add response submission view
- [ ] Add first progress summary view

## Branch Closure Requirements (`main` bootstrap baseline)

Close the current bootstrap baseline when all items below are true:

- [ ] Initial scaffold is committed to `main`.
- [ ] `README.md`, `.env.example`, `.gitignore`, and `Makefile` are no longer placeholders.
- [ ] `api/main.py` exposes a real FastAPI app entrypoint.
- [ ] Alembic is initialized and ready for the first migration.
- [ ] `web/README.md` and the default starter page have been replaced with project-specific content.
- [ ] The repo includes basic sync/deploy scripts for copying runtime slices to `continuum-mini` and `atlas`.
- [ ] ROADMAP claims match the actual code and file state.

Current status against bootstrap closure gate (2026-03-21):

- Git remote: configured and ready.
- Scaffold directories: present.
- Tooling baseline: `mise`, `uv`, and Next.js scaffolding are in place.
- Commit history: blocked because the first commit has not been created yet.
- Root docs/config: still mostly empty placeholders.
- Backend runtime: blocked because `api/main.py` is still a placeholder script.
- Persistence layer: blocked because Alembic and first models do not exist yet.
- Frontend product UI: blocked because `web/` is still the default `create-next-app` starter.

## Git Workflow Guardrails (Solo Professional Baseline)

Use this workflow for every roadmap item unless explicitly overridden:

- [ ] Create work only on topic branches (`feature/*`, `fix/*`, `chore/*`, `docs/*`) once the bootstrap baseline is committed
- [ ] Keep branch scope aligned to one roadmap unit
- [ ] Record verification commands and outcomes whenever roadmap status changes
- [ ] Update ROADMAP when real implementation state changes
- [ ] Prefer squash merges to keep `main` readable
- [ ] Keep runtime-copy scripts separate from source-code changes when possible
- [ ] Treat unverified claims as pending, even if they are likely true

Recommended branch naming examples:

- `chore/bootstrap-foundation`
- `feature/goal-and-lesson-flow`
- `feature/alembic-baseline`
- `docs/runtime-split`
- `fix/api-entrypoint`

PR template checklist (copy into PR description):

```md
## Summary
- Phase / roadmap item:
- Scope (what this PR changes):
- Out of scope / deferred:

## Verification
- [ ] Backend boots locally
- [ ] Frontend boots locally
- [ ] Tests run and pass (list commands)
- [ ] Manual smoke checks completed (list flows)

## Docs and Contract
- [ ] ROADMAP updated (if status changed)
- [ ] README / env docs updated (if behavior changed)
- [ ] Runtime split notes updated (if deployment behavior changed)

## Git Hygiene
- [ ] Branch name follows convention (`feature/*`, `fix/*`, `chore/*`, `docs/*`)
- [ ] PR scoped to one roadmap slice
- [ ] Follow-up issues linked for deferred work
```

## Immediate Build Order

1. Commit the current scaffold baseline to `main`.
2. Fill in `.gitignore`, `.env.example`, `README.md`, and `Makefile`.
3. Replace `api/main.py` with a FastAPI application entrypoint.
4. Add `api/app/core/config.py` and the first app settings contract.
5. Initialize Alembic and create the first migration baseline.
6. Replace the default Next.js starter page with a real Owl of Athens shell.
7. Add the first end-to-end learner slice: goal -> lesson -> response -> evaluation -> persisted progress.
8. Add runtime sync scripts for copying `api/` to `continuum-mini` and `atlas-runtime/` to `atlas`.
