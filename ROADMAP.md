# Owl of Athens Roadmap

Last updated: 2026-03-22

## Purpose (Grounding Contract)

This file is the source-of-truth context for ongoing AI-assisted sessions.

- `owl-of-athens` is a local-first AI learning engine.
- It is not a chatbot, a one-off lesson generator, or a coding-only tutor.
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
- Treat unverified claims as pending, even if they are likely true.

## Deployment Target (Current)

- Canonical source repo: `/mnt/continuum/Projects/owl-of-athens`
- Shared bare Git remote: `/mnt/continuum/git/owl-of-athens.git`
- Primary backend/runtime target: `continuum-mini` (`192.168.0.74`, Tailscale `100.95.103.102`)
- Intended AI/graphics runtime target: `atlas` (`192.168.0.138`, Tailscale `100.80.245.114`)
- All runtime config must be environment-driven. Required env vars:
  - `DATABASE_URL`
  - `API_HOST`
  - `API_PORT`
  - `MODEL_PROVIDER`
  - `ATLAS_BASE_URL`
  - `OPENAI_API_KEY`
  - `OLLAMA_BASE_URL`

## Core Contracts

These files are the ground truth for how the system behaves. They are defined before
the endpoints that implement them. If a contract and an implementation disagree, the
contract wins until the contract is explicitly updated.

### Lesson Contract (`core/contracts/lesson.schema.json`)

Status: **Committed, needs correction**

Target shape:

```json
{
  "lesson_id": "uuid",
  "goal": "string",
  "title": "string",
  "scope": {
    "prerequisite_concepts": ["string"],
    "out_of_scope": ["string"]
  },
  "concept": {
    "explanation": "string",
    "key_points": ["string"]
  },
  "example": {
    "input": "string",
    "output": "string",
    "explanation": "string"
  },
  "task": {
    "prompt": "string",
    "instructions": "string",
    "response_type": "code | explanation | choice | short_answer",
    "expected_format": "string"
  }
}
```

Design decisions locked:
- One task per lesson. Multi-step lessons require session state and partial evaluation
  logic that is out of scope until the single-task loop is proven.
- Response type is declared by the lesson, not inferred at evaluation time.
- `scope` is required. A lesson that does not declare its boundaries will over-generate.

Current known defects in the committed file:
- `example` is malformed and currently contains task-shaped properties instead of
  `input`, `output`, and `explanation`.
- `task` is required but not actually defined in `properties`.
- `short_answer` is misspelled.

### Evaluation Contract (`core/contracts/evaluation.schema.json`)

Status: **Committed, needs correction**

Target shape:

```json
{
  "lesson_id": "uuid",
  "response_type": "code | explanation | choice | short_answer",
  "learner_response": "string",
  "score": "float (0.0-1.0)",
  "correct": "boolean",
  "feedback": "string",
  "misconception": "string | null",
  "next_action": "retry | continue | review"
}
```

Design decisions locked:
- `misconception` is nullable. If the evaluator detects a specific wrong mental model,
  name it. If not, `null`.
- `next_action` is always present. The system always tells the learner what to do next.
- `score` is a float, not a boolean.

Current known defects in the committed file:
- The schema does not yet include `lesson_id`.
- The schema does not yet include `response_type`.
- The schema does not yet include `learner_response`.

### Atlas Runtime Contract (`core/contracts/atlas.contract.md`)

Status: **Missing**

The contract between `continuum-mini` API services and `atlas` inference services must
exist as a file before Phase 1 begins, even as a placeholder. At minimum it must
declare:
- Request shape
- Response shape
- Auth/transport mechanism
- Which model operations are intended to run on `atlas` vs inline on `continuum-mini`

## Falsifiable Test (Spine Exit Criterion)

The spine is not proven until a real person can do all of the following in sequence:

1. Enter a learning goal.
2. Receive a lesson that conforms to the lesson contract.
3. Read the lesson and know what the task is asking without additional context.
4. Submit a response.
5. Receive feedback that is specific to their response, not generic.
6. Understand from the feedback what to do next.

If any step fails, the spine is broken regardless of whether the API returns 200.

## Verified Status Snapshot

Validated in this workspace on 2026-03-22:

- `git rev-parse --is-inside-work-tree` returns `true`.
- Active branch is `main`.
- `git status --short --branch` is clean except for roadmap changes in progress.
- `git log --oneline --decorate -5` shows three commits on `main`:
  - `a5601ba feat: define canonical lesson and evalutation contracts`
  - `ffca0db chore: establish project baseline (env, gitignore, readme, makefile, port config)`
  - `d1ee5ef chore: bootstrap foundation scaffold`
- Root files:
  - `.gitignore` is populated
  - `.env.example` is populated
  - `README.md` is still empty
  - `Makefile` exists and includes API/web/dev/lint targets
- Backend state:
  - `api/main.py` exposes a real FastAPI app with `/health`
  - `api/app/core/config.py` exists
  - config is not yet correct enough to count as phase-complete:
    - `MODEL_PROVIDER` default is misspelled
    - `OPEN_AI_KEY` does not match required env var `OPENAI_API_KEY`
- Frontend state:
  - `web/` is still effectively scaffold-level
  - `web/README.md` is still the default Next.js starter README
- Contracts state:
  - `core/contracts/lesson.schema.json` exists but is malformed
  - `core/contracts/evaluation.schema.json` exists but is incomplete
  - `core/contracts/atlas.contract.md` does not exist
- No verified provider module, lesson/evaluation endpoints, persistence wiring, or
  end-to-end spine flow exist yet.

## Reality-Checked Phase Status

Phases 2-11 are real and will be built. They are parked until the Phase 1 spine passes
the falsifiable test. The only active phases are 0.5 and 1.

| Phase | Name | Status | Notes |
|---|---|---|---|
| 0.5 | Foundation (Minimal, Correct) | **In Progress** | Bootstrap commits exist, but README is still empty, contracts are not yet correct, atlas contract is missing, and config/env naming is not yet aligned. |
| 1 | Teaching Loop Spine | **Not Started** | No goal -> lesson -> response -> evaluation flow exists yet. |
| — | *Horizon (deferred)* | — | Phases 2-11 stay parked until the Phase 1 spine passes the falsifiable test. |

## Phase 0.5 — Foundation (Minimal, Correct)

**Goal:** The smallest foundation that is still correct. Not a throwaway. Not a full
platform. Enough to build the spine on without incurring rewrites.

**What is in scope:**
- Accurate root docs and runtime guidance
- Clean FastAPI app entrypoint with env-driven config
- Correct core contracts committed to `core/contracts/`
- Minimal Makefile with usable `dev`, `lint`, and `test` targets

**What is explicitly out of scope until after Phase 1:**
- Alembic and database migrations
- Full DB model definitions
- Infra/deployment scripts
- Multi-user or auth logic

### Phase 0.5 Checklist

- [x] Initialize Git repository
- [x] Create shared bare remote at `/mnt/continuum/git/owl-of-athens.git`
- [x] Add `.mise.toml` with pinned toolchain
- [x] Scaffold `api/`, `web/`, `core/`, `atlas-runtime/`, `infra/`, `docs/`, `scripts/`
- [x] Create bootstrap/foundation commits on `main`
- [x] Populate `.gitignore`
- [x] Populate `.env.example`
- [ ] Populate root `README.md` with project purpose, runtime split, and local dev setup
- [ ] Confirm root `Makefile` matches the minimal agreed target and current toolchain
- [ ] Fix `api/app/core/config.py` env names and provider default
- [x] Replace `api/main.py` placeholder with a real FastAPI app entrypoint
- [ ] Correct `core/contracts/lesson.schema.json`
- [ ] Correct `core/contracts/evaluation.schema.json`
- [ ] Add `core/contracts/atlas.contract.md` stub
- [ ] Update roadmap claims whenever real implementation state changes

### Phase 0.5 Closure Gate

Phase 0.5 is closed when all of the following are true:

- [ ] ROADMAP claims match the actual file state.
- [ ] `README.md` is no longer a placeholder.
- [ ] `api/main.py` exposes a real FastAPI app that boots without error.
- [ ] `api/app/core/config.py` correctly reads required env vars via pydantic-settings.
- [ ] `lesson.schema.json`, `evaluation.schema.json`, and `atlas.contract.md` all exist
      and match the locked contract shapes.

## Phase 1 — Teaching Loop Spine

**Goal:** One real learner can enter a goal, receive a lesson, submit a response, and
get meaningful feedback. Nothing is hardcoded. Nothing is faked. The falsifiable test
passes.

**Build order within Phase 1:**

1. Repair and lock the lesson/evaluation contracts plus the atlas stub.
2. Add an OpenAI provider baseline: the minimum provider interface needed to make one
   structured call and validate the response against the lesson contract.
3. Add `POST /generate-lesson` to take a goal and return a contract-conforming lesson.
4. Add `POST /evaluate-response` to take a lesson ID plus learner response and return a
   contract-conforming evaluation.
5. Replace the default Next.js starter with an Owl of Athens app shell.
6. Add goal entry view.
7. Add lesson display view.
8. Add response submission view.
9. Add feedback and next-action view.
10. Run the falsifiable test manually end to end.

**Persistence is added after the spine passes the falsifiable test, not before:**

11. Initialize Alembic.
12. Add `learner`, `goal`, `lesson`, and `attempt` models.
13. Wire persistence into the generate and evaluate endpoints.
14. Confirm the falsifiable test still passes with persistence enabled.

### Phase 1 Checklist

**Contracts and provider:**
- [ ] `core/contracts/lesson.schema.json` corrected and validated
- [ ] `core/contracts/evaluation.schema.json` corrected and validated
- [ ] `core/contracts/atlas.contract.md` stub committed
- [ ] OpenAI provider module in `api/app/services/provider.py`
- [ ] Structured output validation against lesson contract on every model response
- [ ] Failure-path handling for malformed model output

**API:**
- [ ] `POST /generate-lesson` implemented
- [ ] `POST /evaluate-response` implemented
- [ ] Both endpoints boot and return contract-conforming responses locally

**UI:**
- [ ] Default Next.js starter replaced with Owl of Athens app shell
- [ ] Goal entry view
- [ ] Lesson display view
- [ ] Response submission view
- [ ] Feedback and next-action view

**Spine validation:**
- [ ] Falsifiable test passes manually end to end (no persistence yet)

**Persistence (after spine passes):**
- [ ] Alembic initialized
- [ ] `learner`, `goal`, `lesson`, `attempt` models defined
- [ ] Generate and evaluate endpoints persist to DB
- [ ] Falsifiable test passes with persistence enabled

### Phase 1 Closure Gate

Phase 1 is closed when all of the following are true:

- [ ] The falsifiable test passes with persistence enabled.
- [ ] No hardcoded values exist in the generate or evaluate paths.
- [ ] Model provider is fully env-driven (`MODEL_PROVIDER`, `OPENAI_API_KEY`).
- [ ] All model responses are validated against their contract before use.
- [ ] `web/README.md` describes how to run the full local dev stack.
- [ ] ROADMAP updated to reflect actual state.

## Horizon Phases (Parked)

These phases are real. They are not being designed for until the Phase 1 spine passes
its falsifiable test. Do not let their existence drive Phase 0.5 or Phase 1 decisions.

| Phase | Name | Waiting On |
|---|---|---|
| 2 | Course Generation | Phase 1 spine proven. Curriculum schema can only be designed well after one lesson loop is understood. |
| 3 | Assessment Engine | Phase 1 evaluation path stable. Rubric and objective evaluation forks from the evaluation contract. |
| 4 | Adaptive Learning Engine | Phase 3. Mastery model requires stable assessment signal first. |
| 5 | Learner State and Multi-User | Phase 1 persistence. Profile and sync model requires a working single-user baseline. |
| 6 | Learning Modes Expansion | Phase 1. `explain`, `drill`, `challenge`, `project` modes require a stable default loop first. |
| 7 | Misconception Tracking | Phase 3. Error taxonomy requires assessment data to build from. |
| 8 | Model Provider Layer (full) | Phase 1 OpenAI baseline. Full provider abstraction and atlas-runtime integration follow after the baseline call is proven. |
| 9 | Learner Experience UI (full) | Phase 1 UI shell. Full product UI follows after the spine UI is validated. |
| 10 | Knowledge and Mastery Tracking | Phase 4. Durable mastery map requires the adaptive engine. |
| 11 | Domain Expansion | Phase 1 end to end on one domain. Multi-domain begins after one excellent domain proves the core loop. |

## Git Status and Direction

Current git status:

- Active branch: `main`
- Remote: `origin -> /mnt/continuum/git/owl-of-athens.git`
- Working tree: clean except for current roadmap edits
- Bootstrap/foundation work already exists on `main`

Required direction:

1. Do not redo the bootstrap commit sequence. That work already landed on `main`.
2. Finish Phase 0.5 correctness work on a topic branch from current `main`.
3. Repair the core contracts before writing endpoint code that depends on them.
4. Build Phase 1 spine on a dedicated branch after the Phase 0.5 closure gate is met.
5. Do not start Phase 2+ implementation branches until Phase 1 closes.

## Git Workflow Guardrails (Solo Professional Baseline)

- Work on topic branches only (`feature/*`, `fix/*`, `chore/*`, `docs/*`).
- Keep branch scope aligned to one roadmap unit.
- Record verification commands and their actual output whenever roadmap status changes.
- Update ROADMAP when real implementation state changes, not before.
- Prefer squash merges to keep `main` readable.
- Keep runtime-copy scripts separate from source-code changes.
- Treat unverified claims as pending, even if they are likely true.

Recommended branch naming:

- `fix/foundation-alignment`
- `docs/atlas-contract`
- `feature/teaching-loop-spine`
- `feature/alembic-baseline`
- `chore/deploy-scripts`

## Immediate Build Order

This is the current executable sequence. Do not deviate without updating this section.

1. **Finish foundation alignment** — `fix/foundation-alignment`
   - Populate root `README.md`
   - Fix `api/app/core/config.py`
   - Correct `lesson.schema.json`
   - Correct `evaluation.schema.json`
   - Add `core/contracts/atlas.contract.md`
   - Verify the FastAPI app still boots

2. **Build the spine** — `feature/teaching-loop-spine`
   - OpenAI provider module
   - `POST /generate-lesson`
   - `POST /evaluate-response`
   - Next.js app shell + goal -> lesson -> response -> feedback UI
   - Run falsifiable test manually

3. **Add persistence** — `feature/alembic-baseline`
   - Alembic init + first migration
   - `learner`, `goal`, `lesson`, `attempt` models
   - Wire endpoints
   - Re-run falsifiable test
   - **Phase 1 is now closed**

4. **Add runtime sync scripts** — `chore/deploy-scripts`
   - Script to copy `api/` slice to `continuum-mini`
   - Script to copy `atlas-runtime/` slice to `atlas`
   - Keep these separate from source-code changes
