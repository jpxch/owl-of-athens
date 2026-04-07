# Owl of Athens Web

Next.js frontend for the Owl of Athens teaching loop.

The current learner flow supports:

- entering a learning goal
- generating a structured lesson from the API
- submitting a learner response
- receiving evaluation feedback and next-step guidance

## Local Development

Start the web app from the repo root:

```bash
make web-dev
```

Default URL:

```text
http://localhost:3000
```

## Environment

Set the API base URL in `.env.local`:

```bash
NEXT_PUBLIC_API_BASE_URL=http://localhost:8010
```

If unset, the frontend falls back to `http://localhost:8010`.

## Key Files

- `src/app/page.tsx` - learner flow UI and API calls
- `src/app/layout.tsx` - app metadata and root layout
- `src/app/globals.scss` - shared global styles
