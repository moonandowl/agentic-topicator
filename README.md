# Agentic Topicator

[![CI](https://github.com/moonandowl/agentic-topicator/actions/workflows/ci.yml/badge.svg)](https://github.com/moonandowl/agentic-topicator/actions/workflows/ci.yml)

A parallel, agent-based system for generating article topic ideas and article briefs. Input a topic and audience; 26 specialized sub-agents run in parallel, each returning article-worthy angles through a distinct psychological lens. Select ideas and generate full article briefs for writers.

**Repository:** [github.com/moonandowl/agentic-topicator](https://github.com/moonandowl/agentic-topicator)

## Quick Start

```bash
pip install -r requirements.txt
cp .env.example .env
# Edit .env with API keys and optional AUTH_USERNAME / AUTH_PASSWORD
uvicorn main:app --reload
# Open http://localhost:8000
```

## Process

1. **Input** — Topic + Audience
2. **26 Sub-Agents (parallel)** — Each returns 3 topic suggestions with justifications
3. **Review & Select** — Browse all suggestions, filter by agent, select one or more
4. **Brief Builder** — One call per selection; produces full article brief (outline, guideline bullets, CTA)
5. **Export** — Download all briefs as .zip or individual files

## Supported Models

- Claude Opus 4.6 MAX (Anthropic)
- GPT-4.1 (OpenAI)
- Gemini 2.5 Pro (Google)
- Sonar Pro (Perplexity)

Select per run from the UI.

## Deploy (Render)

1. Fork or clone this repo, then connect it to [Render](https://render.com).
2. Create a new Web Service from the repository.
3. Render will auto-detect `render.yaml`; no extra config needed.
4. Add environment variables in the Render dashboard (see below).

## Environment Variables

| Variable | Required | Description |
|----------|----------|-------------|
| `ANTHROPIC_API_KEY` | One of four | For Claude Opus 4.6 MAX |
| `OPENAI_API_KEY` | One of four | For GPT-4.1 |
| `GOOGLE_API_KEY` | One of four | For Gemini 2.5 Pro |
| `PERPLEXITY_API_KEY` | One of four | For Sonar Pro |
| `AUTH_USERNAME` | Optional | When set with `AUTH_PASSWORD`, enables HTTP Basic Auth |
| `AUTH_PASSWORD` | Optional | When set with `AUTH_USERNAME`, enables HTTP Basic Auth |

## Docs

- **[CURSOR_PROJECT_SPEC.md](./CURSOR_PROJECT_SPEC.md)** — Full spec for building the project in Cursor
- **[process-flow.md](./process-flow.md)** — Architecture, data flow, API, UI
- **[sub-agents-reference.md](./sub-agents-reference.md)** — Agent definitions and system prompt guidance
