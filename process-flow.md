# Content Topic Agent System — Process Flow & Architecture

## Purpose

This application helps content strategists generate deeply researched article ideas from a single topic input. Instead of brainstorming manually, the system runs 26 specialized sub-agents in parallel, each analyzing the topic through a distinct psychological or behavioral lens. The user reviews all outputs, selects a single idea, and the system builds a complete article brief around it.

---

## User Roles

There is one user role: the content strategist. They input topics, review agent outputs, select ideas, and receive finished article briefs that are handed off to writers.

---

## Process Flow

### Step 1: Topic Input

The user provides two inputs:
- **Topic** — The subject to analyze (e.g., "dental implants," "knee replacement," "Invisalign for adults")
- **Audience** — Who the content is for (e.g., "women 35-55 considering cosmetic dentistry," "active adults 50+ with chronic knee pain")

This is the only user input required to trigger the entire sub-agent layer.

### Step 2: Sub-Agent Execution (Parallel)

All 26 sub-agents receive the same topic + audience input and run simultaneously. Each agent analyzes the topic through its unique lens and returns a list of article-worthy topic suggestions.

Key behavior:
- All 26 agents fire at the same time. They do not depend on each other.
- Each agent returns its own independent list of suggestions. There is no cross-agent communication.
- Each suggestion should be a clear, specific article idea — not abstract analysis or research findings.
- The output format for every agent should be consistent so the UI can display them uniformly.

**Expected output per agent:**
Each agent returns a list of 3 article topic suggestions. Each suggestion includes three fields in this exact format:

```
Sub-Agent Name: [Name of the agent that generated this suggestion]
Topic: [The article topic]
Justification: [One sentence explaining why this topic is being recommended]
```

The sub-agent name is repeated on every suggestion so the UI can display all suggestions across all agents in a single unified feed while still showing which agent produced each one. This allows the user to scan everything at once without needing to click into individual agent tabs.

### Step 3: User Review and Multi-Selection

The user sees all suggestions from all 26 agents in a unified feed. Each suggestion displays:

```
Sub-Agent Name: [Agent]
Topic: [Topic]
Justification: [One sentence]
```

The user can:
- Scan the full feed across all agents
- Filter by agent name to focus on a specific lens
- Read individual justifications to understand why each topic is being recommended

The user selects **one or more suggestions** by checking a box on each one they want. Selected suggestions go into a visible selection queue (like a shopping cart) so the user can review everything they have picked before generating briefs. This supports batch workflows where the same topic run produces briefs for multiple clients.

### Step 4: Brief Builder Execution (Batch)

Once the user is satisfied with their selections, they hit "Generate Briefs" once. The Brief Builder fires a parallel call for each selected suggestion. Each call receives three inputs:
- **The selected suggestion** (including the Sub-Agent Name, Topic, and Justification)
- **The original topic**
- **The original audience**

All calls run concurrently. Each brief comes back independently as it completes, with progressive loading in the UI so the user does not wait for all briefs to finish before seeing results.

The Brief Builder produces a complete article brief containing:

1. **Justification** — Why this article matters. What makes it timely, relevant, and valuable to the target audience. This gives the writer context on the purpose behind the piece.

2. **Suggested Outline** — A section-by-section structure for the article. Typically 4-7 sections with clear heading suggestions. The outline should reflect a logical reading flow that moves the reader from where they are to where the article wants to take them.

3. **Guideline Bullets Under Each Heading** — Under every section in the outline, specific points the writer should cover. These are not sentences to copy — they are direction. Each bullet tells the writer what to address, what angle to take, what to include or avoid, and what the reader should feel or understand after reading that section.

4. **Customized CTA** — A call to action tailored to the emotional and psychological state the reader will be in after consuming this specific article. Not a generic "book a consultation" but a CTA that flows naturally from the content. Should include suggested CTA language and a brief note on why this CTA fits this particular article.

### Step 5: Output Delivery

The completed briefs are displayed on a results screen. Each brief is labeled with its topic, the agent it came from, and the full brief content.

**Export options:**
- **Zipped individual files** — Each brief is generated as its own document. All briefs are bundled into a single .zip file for one-click download.
- **Individual export** — Download any single brief on its own from the results screen.

The user can also:
- Go back to the selection queue and add or remove suggestions
- Regenerate any individual brief without affecting the others

---

## Data Flow Diagram

```
┌─────────────────────┐
│   USER INPUT        │
│   - Topic           │
│   - Audience        │
└────────┬────────────┘
         │
         ▼
┌─────────────────────────────────────────────┐
│           26 SUB-AGENTS (PARALLEL)          │
│                                             │
│  ┌──────────┐ ┌──────────┐ ┌──────────┐    │
│  │ Jobs to  │ │Objections│ │ Emotional│    │
│  │ Get Done │ │          │ │          │    │
│  └──────────┘ └──────────┘ └──────────┘    │
│  ┌──────────┐ ┌──────────┐ ┌──────────┐    │
│  │Questions │ │Self-ID / │ │  Values  │    │
│  │          │ │Transform │ │          │    │
│  └──────────┘ └──────────┘ └──────────┘    │
│                                             │
│  ... (all 26 agents)                        │
│                                             │
│  Each returns 3 article topic               │
│  suggestions with angle summaries           │
└────────────────────┬────────────────────────┘
                     │
                     ▼
┌─────────────────────────────────────────────┐
│        USER REVIEW & MULTI-SELECTION        │
│                                             │
│  User browses all agent outputs             │
│  User selects ONE or MORE suggestions       │
│  Selections go into a visible queue         │
│                                             │
└────────────────────┬────────────────────────┘
                     │
                     ▼
┌─────────────────────────────────────────────┐
│       BRIEF BUILDER AGENT (BATCH)           │
│                                             │
│  Fires one parallel call per selection      │
│                                             │
│  Each call receives:                        │
│  - Selected suggestion + justification      │
│  - Original topic                           │
│  - Original audience                        │
│                                             │
│  Each call outputs:                         │
│  - Justification                            │
│  - Suggested outline                        │
│  - Guideline bullets per heading            │
│  - Customized CTA                           │
│                                             │
└────────────────────┬────────────────────────┘
                     │
                     ▼
┌─────────────────────────────────────────────┐
│          COMPLETED ARTICLE BRIEFS           │
│                                             │
│  Results screen with all briefs             │
│  Export: Zipped individual files or         │
│          single brief download              │
│                                             │
└─────────────────────────────────────────────┘
```

---

## Agent Design Principles

### Every sub-agent must:
- Accept the same two inputs: topic and audience
- Return a consistent output format: Sub-Agent Name, Topic, and a one-sentence Justification for each suggestion
- Operate independently with no awareness of other agents
- Generate topics that are specific enough for a writer to understand the angle from the topic title and justification alone
- Stay in its lane — the Emotional agent does not generate objections, the Roles agent does not generate emotions

### The Brief Builder must:
- Accept three inputs per call: selected suggestion, original topic, original audience
- Run one call per selected suggestion, all in parallel
- Produce a brief that a writer could pick up cold and produce a quality article without needing to ask clarifying questions
- Tailor the CTA to the specific emotional journey of the article, not use a generic CTA
- Provide enough direction in the guideline bullets that the writer knows what to say, but not so much that it becomes a draft

---

## Technical Considerations

### Parallel Execution
All 26 sub-agents should run concurrently. They are independent of each other and share no state. The UI should show progress as agents complete (streaming or progressive loading) rather than waiting for all 26 to finish before displaying anything.

### API Architecture
Each sub-agent is a separate LLM call with its own system prompt defining its unique perspective. The topic and audience are injected into the user message. All calls use the same model.

Suggested structure:
```
POST /api/generate-topics
  Body: { topic, audience }
  Response: Fires all 26 agent calls in parallel
  Returns: Array of 26 agent results, each containing agent name and list of suggestions

POST /api/generate-briefs
  Body: { selections: [{ subAgentName, topic, justification }], originalTopic, originalAudience }
  Response: Fires one Brief Builder call per selection in parallel
  Returns: Array of completed brief objects

GET /api/export-briefs
  Body: { briefIds: [...] }
  Response: Generates a .zip file containing each brief as an individual document
  Returns: Downloadable .zip file
```

### State Management
- The application needs to hold the results of all 26 agents in state after Step 2
- A selection queue holds all user-selected suggestions until the user triggers brief generation
- When briefs are generated, the app passes each selected suggestion plus the original topic and audience to separate Brief Builder calls
- Completed briefs are held in state for display and export
- There is no need for persistent storage unless you want to save past runs for reference

### Export Implementation
- Each completed brief is rendered as its own individual document file
- "Download All" generates a .zip archive containing all brief files using a server-side zip library (e.g., JSZip or archiver)
- Individual briefs can be downloaded one at a time from the results screen
- File naming convention should include the topic and agent name for easy identification (e.g., "LASIK-Emotional-Agent-Brief.md")

### Error Handling
- If an individual sub-agent fails, display the other 25 results and show an error state for the failed agent with a retry option
- If an individual Brief Builder call fails, display all other completed briefs and show an error state on the failed brief with a retry option — do not block the entire batch
- Set reasonable timeouts per call — if one call hangs, it should not block the others

### Rate Limiting
- 26 parallel LLM calls for sub-agents is a significant burst. Consider whether the API provider requires batching or staggering
- Brief generation adds another burst — if the user selects 20 topics, that is 20 more parallel calls. Apply the same batching strategy
- If rate limits are hit, implement a queue that processes calls in batches (e.g., 10 at a time) with the UI updating as each batch completes

---

## UI Recommendations

### Topic Input Screen
- Clean, simple form with two fields: Topic and Audience
- A "Generate" button that triggers all 26 agents
- Loading state that shows agents completing progressively

### Agent Results Screen
- All suggestions from all 26 agents displayed in a unified feed, each labeled with its Sub-Agent Name, Topic, and Justification
- Option to filter by agent name so the user can drill into a specific agent's output
- Each suggestion has a checkbox for multi-selection
- A visible selection queue (sidebar or bottom bar) showing all currently selected suggestions with a count
- "Generate Briefs" button that triggers the Brief Builder for all selected suggestions at once

### Brief Output Screen
- All completed briefs displayed in a list or card layout, each labeled with its topic and originating agent
- Click into any brief to view the full content: Justification, Outline, Guideline Bullets, CTA
- "Download All" button that generates a .zip file containing each brief as its own individual document
- Individual download button on each brief for single-file export
- "Back" button to return to agent results and modify selections
- Option to regenerate any individual brief without affecting the others

---

## Sub-Agent List (Complete)

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

Plus the **Brief Builder** as the output agent.

---

## File Reference

- **sub-agents-reference.md** — Contains the detailed perspective description for each of the 26 sub-agents and the Brief Builder. Use this file to build the individual system prompts for each agent.
- **This file (process-flow.md)** — Contains the system architecture, data flow, process steps, and technical considerations. Use this file to build the application structure, API routes, UI, and orchestration logic.
