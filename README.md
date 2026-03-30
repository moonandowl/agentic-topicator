# Agentic Topicator

[![CI](https://github.com/moonandowl/agentic-topicator/actions/workflows/ci.yml/badge.svg)](https://github.com/moonandowl/agentic-topicator/actions/workflows/ci.yml)

A parallel, agent-based system for generating article topic ideas and article briefs. Input a topic and audience; 26 specialized sub-agents run in parallel, each returning article-worthy angles through a distinct psychological lens. Select ideas and generate full article briefs for writers.

**Repository:** [github.com/moonandowl/agentic-topicator](https://github.com/moonandowl/agentic-topicator)

## Quick Start

```bash
pip install -r requirements.txt
cp .env.example .env
# Edit .env: API keys plus AUTH_USERNAME and AUTH_PASSWORD (both required to lock the app)
uvicorn main:app --reload
# Open http://localhost:8000 — browser will prompt for Basic Auth username/password
```

**Password protection:** Set `AUTH_USERNAME` and `AUTH_PASSWORD` together. All routes except `/health` require HTTP Basic Auth. Add the same variables in Railway or Render (see Deploy) so production is protected.

## Process

1. **Input** — Topic + Audience
2. **26 Sub-Agents (parallel)** — Each returns 3 topic suggestions with justifications
3. **Review & Select** — Browse all suggestions, filter by agent, select one or more
4. **Brief Builder** — One call per selection; produces full article brief (outline, guideline bullets, CTA)
5. **Export** — Download all briefs as .zip or individual files

## Supported Models

- **Anthropic:** claude-opus-4-6
- **OpenAI:** gpt-4o (override with `OPENAI_MODEL` for gpt-5.4-pro, etc.)
- **Google:** gemini-2.0-flash (override with `GOOGLE_MODEL` for gemini-3.1-pro-preview, etc.)
- **Perplexity:** sonar-pro
- **Grok (xAI):** grok-4-fast-reasoning (override with `GROK_MODEL`)

Select per run from the UI. Override via env vars if needed.

## Deploy

### Railway

1. Go to [Railway](https://railway.app) and sign in with GitHub.
2. Click **New Project** → **Deploy from GitHub repo**.
3. Select `moonandowl/agentic-topicator` (or your fork).
4. Railway auto-detects `railway.json`; no extra config needed.
5. In the service **Variables** tab, add your API keys and optional auth (see below).
6. In **Settings** → **Networking**, click **Generate Domain** for a public URL.

### Render

1. Connect the repo at [Render](https://render.com).
2. Create a new Web Service; Render auto-detects `render.yaml`.
3. Add environment variables in the dashboard (see below).

## Environment Variables

| Variable | Required | Description |
|----------|----------|-------------|
| `ANTHROPIC_API_KEY` | One of five | For claude-opus-4-6 |
| `OPENAI_API_KEY` | One of five | For gpt-4o |
| `GOOGLE_API_KEY` | One of five | For gemini-2.0-flash |
| `PERPLEXITY_API_KEY` | One of five | For sonar-pro |
| `XAI_API_KEY` | One of five | For Grok (grok-4-fast-reasoning) |
| `OPENAI_MODEL` | Optional | Default: `gpt-4o` |
| `GOOGLE_MODEL` | Optional | Default: `gemini-2.0-flash` |
| `ANTHROPIC_MODEL` | Optional | Default: `claude-opus-4-6` |
| `PERPLEXITY_MODEL` | Optional | Default: `sonar-pro` |
| `GROK_MODEL` | Optional | Default: `grok-4-fast-reasoning` |
| `AUTH_USERNAME` | Optional | When set with `AUTH_PASSWORD`, enables HTTP Basic Auth |
| `AUTH_PASSWORD` | Optional | When set with `AUTH_USERNAME`, enables HTTP Basic Auth |

## Docs

- **[CURSOR_PROJECT_SPEC.md](./CURSOR_PROJECT_SPEC.md)** — Full spec for building the project in Cursor
- **[process-flow.md](./process-flow.md)** — Architecture, data flow, API, UI
- **[sub-agents-reference.md](./sub-agents-reference.md)** — Agent definitions and system prompt guidance
