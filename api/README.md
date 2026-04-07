# Owl of Athens API

FastAPI backend for the Owl of Athens teaching loop.

Current routes:

- `GET /health`
- `POST /generate-lesson`
- `POST /evaluate-response`

Error behavior:

- invalid request payloads return `400` with field-level validation details
- provider configuration failures return `500`
- malformed provider output and schema-validation failures return `502` with structured error metadata

## Responsibilities

- validate incoming lesson and evaluation requests
- orchestrate provider calls
- validate model output against the canonical JSON contracts
- return learner-facing errors that distinguish invalid input from upstream/provider failures

## Local Development

Start the API from the repo root:

```bash
make api-dev
```

Default URL:

```text
http://localhost:8010
```

## Environment

The API reads configuration from `.env`.

Required or commonly used variables:

- `DATABASE_URL`
- `CORS_ALLOWED_ORIGINS`
- `MODEL_PROVIDER`
- `OPENAI_API_KEY`
- `OPENAI_MODEL`
- `ATLAS_BASE_URL`
- `OLLAMA_BASE_URL`

## Testing

Run backend tests from `api/`:

```bash
uv run pytest
```

Current automated coverage includes:

- health route registration
- lesson generation route behavior
- evaluation route behavior
- invalid request payload handling
- malformed provider response handling
- provider schema failure handling
