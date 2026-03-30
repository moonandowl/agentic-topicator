# Agentic Topicator — Cursor Project Specification

Use this document to build the Agentic Topicator from scratch in a new Cursor project. Read it fully before implementing.

---

## Project Overview

**Name:** Agentic Topicator

**Purpose:** A content topic ideation system. The user inputs a topic and audience. 26 specialized sub-agents run in parallel, each returning 3 article topic suggestions through a distinct psychological or behavioral lens. The user reviews all outputs, selects one or more suggestions, and the Brief Builder generates complete article briefs for writers.

**Key differentiator from Article Topic Council:** No debate, no cross-talk. Each agent runs independently in parallel. Faster and simpler.

---

## Reference Documents

- **[process-flow.md](./process-flow.md)** — Process steps, data flow, API design, UI recommendations, technical considerations
- **[sub-agents-reference.md](./sub-agents-reference.md)** — Detailed perspective and output format for each of the 26 sub-agents and the Brief Builder. Use for system prompts.

---

## Tech Stack Requirements

- **Framework:** FastAPI (Python)
- **UI:** Server-rendered HTML (Jinja2) or similar; keep it simple
- **Auth:** HTTP Basic Auth with configurable username and password (via env vars). Same pattern as Article Topic Council.
- **Persistence:** Optional. Process-flow says "no need for persistent storage unless you want to save past runs." Start without DB; add SQLite later if needed for session history.
- **Models:** Support the same four providers and let user choose per run:

| Provider  | Model ID        | Env Var            |
|----------|------------------|--------------------|
| Anthropic| claude-opus-4-6  | ANTHROPIC_API_KEY  |
| OpenAI   | gpt-4.1          | OPENAI_API_KEY     |
| Google   | gemini-2.5-pro   | GOOGLE_API_KEY     |
| Perplexity | sonar-pro     | PERPLEXITY_API_KEY |

- **Auth env var:** `AUTH_PASSWORD` — when set, require HTTP Basic Auth on all routes except `/health` for deployment healthchecks (only password is verified; username ignored).

---

## Process Summary (from process-flow.md)

1. **Topic Input** — User provides Topic and Audience. Only two fields.
2. **Sub-Agent Execution** — All 26 agents run in parallel. Each returns 3 suggestions in format: `Sub-Agent Name`, `Topic`, `Justification`.
3. **User Review & Multi-Selection** — Unified feed of all suggestions. User can filter by agent. Checkboxes for selection. Visible selection queue.
4. **Brief Builder** — One parallel call per selected suggestion. Inputs: selection + original topic + audience. Outputs: Justification, Outline, Guideline Bullets, Customized CTA.
5. **Output Delivery** — Display briefs. Export: zipped individual files or single-brief download.

---

## Sub-Agent Output Format (Required)

Every sub-agent must return suggestions in this exact format:

```
Sub-Agent Name: [Agent display name]
Topic: [Article topic]
Justification: [One sentence]

Sub-Agent Name: [Agent display name]
Topic: [Article topic]
Justification: [One sentence]
```

3 suggestions per agent. Sub-Agent Name is repeated on every suggestion so the UI can show a unified feed with agent attribution.

---

## Brief Builder Output (Required)

Per selected suggestion, the Brief Builder produces:

1. **Justification** — Why this article matters; context for the writer
2. **Suggested Outline** — 4–7 sections with heading suggestions
3. **Guideline Bullets Under Each Heading** — What to cover, angle, what to avoid
4. **Customized CTA** — Tailored to the article’s emotional journey, with suggested language and rationale

---

## API Structure (from process-flow.md)

```
POST /api/generate-topics
  Body: { topic, audience, model_provider? }
  Response: Array of 26 agent results; each has agent name + list of suggestions
  Runs all 26 agents in parallel (or batched if rate limits require)

POST /api/generate-briefs
  Body: { selections: [{ subAgentName, topic, justification }], originalTopic, originalAudience, model_provider? }
  Response: Array of completed brief objects
  Runs one Brief Builder call per selection in parallel

GET /api/export-briefs?ids=... (or POST with body)
  Response: .zip file containing each brief as an individual document
```

---

## UI Flow

1. **Input screen** — Topic (text), Audience (text), Model (dropdown: Anthropic, OpenAI, Google, Perplexity). Generate button.
2. **Results screen** — Unified feed of all suggestions. Filter by agent. Checkbox per suggestion. Selection queue (sidebar or bar) with count. "Generate Briefs" button.
3. **Briefs screen** — List/cards of completed briefs. Expand to view full content. Download All (.zip), Download single. Back to modify selections. Regenerate individual brief.

---

## Error Handling

- Sub-agent failure: show other 25 results, error + retry for failed agent
- Brief Builder failure: show other briefs, error + retry for failed one
- Use timeouts so one hung call does not block others
- Rate limits: batch calls (e.g., 10 at a time) if needed; update UI as batches complete

---

## File Naming for Export

Use pattern: `{TopicSlug}-{AgentName}-Brief.md` (e.g., `LASIK-Emotional-Agent-Brief.md`)

---

## Implementation Order

1. Project scaffold: FastAPI app, config, env, auth, model providers (mirror Article Topic Council structure)
2. Sub-agent layer: 26 system prompts from sub-agents-reference.md; single `generate_topics` orchestration that runs all in parallel (with optional batching)
3. Input UI + topic generation + results feed with selection
4. Brief Builder: single prompt; `generate_briefs` that runs one call per selection in parallel
5. Briefs display + export (zip + single file)

---

## Environment Variables

Configure via the host dashboard or shell exports; the app reads `os.environ` only (no `.env` file loading).

```env
# Required for chosen provider
ANTHROPIC_API_KEY=
OPENAI_API_KEY=
GOOGLE_API_KEY=
PERPLEXITY_API_KEY=
XAI_API_KEY=

# Optional auth (when set, enables HTTP Basic Auth)
AUTH_PASSWORD=
```

---

## Dependencies (Suggested)

```
fastapi>=0.115.0
uvicorn>=0.34.0
anthropic>=0.42.0
openai>=1.59.0
google-genai>=1.0.0
httpx>=0.28.0
python-multipart>=0.0.18
jinja2>=3.1.4
pydantic>=2.10.0
```

For zip export: use Python stdlib `zipfile` or a simple archiver.

---

## Sub-Agent List (26)

1. Jobs to Get Done  
2. Objections  
3. Emotional  
4. Questions  
5. Self-Identity / Transformation  
6. Values  
7. Regrets  
8. Day Before and After  
9. Roles  
10. Permission  
11. What I Have to Believe  
12. Social Proof  
13. Risk / Consequence (Cost of Inaction)  
14. Timing / Urgency  
15. Myths and Misconceptions  
16. Trust and Credibility  
17. Stage of Awareness  
18. Secret Desires  
19. Fear / Worst Case  
20. Money Story  
21. Past Experience  
22. Age / Life Stage  
23. Control / Autonomy  
24. Taboo / Shame  
25. Catalyst / Tipping Point  
26. Decision Catalyst  

Plus **Brief Builder** as the output agent.

Full perspectives and prompt guidance: see [sub-agents-reference.md](./sub-agents-reference.md).
