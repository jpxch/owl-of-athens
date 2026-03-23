# Atlas Runtime Contract (Stub)

## Purpose

Defines the interface between:

- continuum-mini (API / orchestration layer)
- atlas (model execution layer)

This is a minimal stub for Phase 0.5.

---

## Transport

- Protocol: HTTP (JSON)
- Base URL: defined via ATLAS_BASE_URL

---

## Endpoint: Generate Lesson

POST /v1/lesson/generate

### Request

{
  "goal": "string"
}

### Response

{
  "lesson": { ...Lesson Schema... }
}

---

## Endpoint: Evaluate Response

POST /v1/lesson/evaluate

### Request

{
  "lesson_id": "string",
  "response_type": "code | explanation | choice | short_answer",
  "learner_response": "string"
}

### Response

{
  "evaluation": { ...Evaluation Schema... }
}

---

## Notes

- Atlas is responsible ONLY for model inference
- Validation of schema happens in API layer
- API owns persistence and orchestration
- Atlas is stateless

---

## Future Extensions

- streaming responses
- local model fallback (Ollama)
- batching
- caching layer