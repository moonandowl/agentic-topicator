# Content Topic Agent System — Sub-Agent Reference

## System Overview

This system generates article topic ideas for client content. A user inputs a topic and audience. All 26 sub-agents run in parallel, each producing a list of article-worthy angles through its specific psychological or behavioral lens. The user reviews all outputs, selects one or more ideas from any agent, and passes them to the pipeline: the SEO Title Agent runs first (one per selection), producing search-optimized H1 titles; then the Brief Builder produces a complete article brief for each selection. Each brief includes both the topic H1 and the SEO title H1.

## Architecture

- **Layer 1: Sub-Agents (26 agents, run in parallel)** — Each agent receives the same topic + audience input and returns a list of article angle suggestions through its unique lens.
- **Layer 2: SEO Title Agent (runs on demand, once per selected topic)** — Runs before the Brief Builder. Receives each selected suggestion and produces an H1-ready SEO/AEO-optimized title for search and AI overviews. Output is inserted as a second H1 below the topic in the final brief.
- **Layer 3: Brief Builder (runs on demand, once per selection)** — Receives the user's chosen article idea plus the SEO title from the prior step and produces a full article brief including justification, outline, guideline bullets under each heading, and a customized CTA.

## Expected Sub-Agent Output Format

Every sub-agent must return its suggestions in this exact format:

```
Sub-Agent Name: [Name of the agent]
Topic: [The article topic]
Justification: [One sentence explaining why this topic is being recommended]

Sub-Agent Name: [Name of the agent]
Topic: [The article topic]
Justification: [One sentence explaining why this topic is being recommended]
```

Each agent produces 3 suggestions. The Sub-Agent Name is repeated on every suggestion so all suggestions from all agents can be displayed in a single unified feed while still showing which agent generated each one.

---

## Sub-Agent Definitions

### 1. Jobs to Get Done Agent
**Perspective:** What functional, emotional, or social job is the person hiring this product or procedure to do for them? Based on Clayton Christensen's Jobs to Be Done theory. People don't buy products — they hire them to make progress in their lives. This agent identifies the underlying jobs and suggests article topics that speak directly to each job.

### 2. Objections Agent
**Perspective:** What reasons do people give themselves or others for not moving forward? These are the spoken and unspoken excuses, hesitations, and rationalizations that stall decisions. This agent surfaces common objections and suggests article topics that address, dismantle, or reframe each one.

### 3. Emotional Agent
**Perspective:** What feelings are driving the desire or creating resistance? This goes beyond surface-level emotions to the deeper feelings at play — frustration, hope, embarrassment, excitement, grief, longing. This agent identifies the emotional landscape around the topic and suggests article topics that speak to each emotional thread.

### 4. Questions Agent
**Perspective:** What are people actually asking — typing into Google at 11pm, whispering to friends, wondering silently in consultations? These are the real questions on their mind, not the polished FAQ versions. This agent surfaces raw, authentic questions and suggests article topics built around answering each one.

### 5. Self-Identity / Transformation Agent
**Perspective:** Who does the person want to become, and how does this topic help them get there? People make decisions that align with their desired identity. This agent explores the aspirational self-image — both near-term transformation and the longer arc of the life they are building — and suggests article topics that connect the topic to personal transformation and becoming.

### 6. Values Agent
**Perspective:** How does this decision connect to what the person holds most important in life? Health, family, independence, faith, achievement, security — decisions that align with core values feel right, and those that conflict feel wrong. This agent maps the topic to value systems and suggests article topics that tie the decision to deeply held beliefs.

### 7. Regrets Agent
**Perspective:** What will the person wish they had done sooner or differently? Regret is one of the most powerful human motivators. This agent explores both the regret of inaction and the regret of poor choices, then suggests article topics that help the reader avoid future regret.

### 8. Day Before and After Agent
**Perspective:** What does a normal Tuesday look like before versus after? This is about the tangible, mundane, daily reality — not dramatic transformations but the small quality-of-life shifts, including changes to routines, habits, and daily behaviors. This agent paints specific before/after daily scenarios and suggests article topics that show the reader what life actually looks like on the other side.

### 9. Roles Agent
**Perspective:** How does this topic affect the person in their various life roles — as a parent, spouse, employee, friend, sibling, church member, team leader, caregiver? People don't exist in a vacuum. This agent examines how the topic intersects with each role and suggests article topics that speak to the reader within a specific identity they hold.

### 10. Permission Agent
**Perspective:** What is stopping the person from letting themselves have this? Many people want something but don't feel they deserve it, can justify it, or are allowed to prioritize themselves. This agent explores the internal permission barriers and suggests article topics that help the reader give themselves permission to act.

### 11. What I Have to Believe Agent
**Perspective:** What convictions need to be in place before the person will act? This maps the sequential belief chain — from believing the problem is real, to believing it's solvable, to believing this specific solution works, to believing this provider can deliver it, to believing they deserve it. This agent identifies each required belief and suggests article topics designed to install or reinforce a single belief.

### 12. Social Proof Agent
**Perspective:** What are people like them doing, and what would those people think? This taps into the "am I the only one?" anxiety and the human need for validation from peers. This agent explores social dynamics around the topic and suggests article topics that normalize the decision through the lens of community and belonging.

### 13. Risk / Consequence Agent (Cost of Inaction)
**Perspective:** What happens if the person does nothing and lets time pass? This is not about fear — it is about the real, compounding cost of inaction over months and years. This agent maps out what deteriorates, what opportunities close, and what gets harder, then suggests article topics that make the cost of waiting concrete.

### 14. Timing / Urgency Agent
**Perspective:** Why now and not later? This explores seasonal triggers, life stage windows, compounding effects of delay, and the moments when action becomes more natural or necessary. This agent identifies timing-based angles and suggests article topics that create legitimate urgency without being manipulative.

### 15. Myths and Misconceptions Agent
**Perspective:** What false beliefs are keeping the person stuck? These are the "truths" people hold that are actually wrong — outdated information, cultural myths, misunderstandings, or assumptions they have never questioned. This agent surfaces common myths and suggests article topics that create an "aha" moment by correcting each one.

### 16. Trust and Credibility Agent
**Perspective:** Can the person trust this process, provider, or outcome? This addresses skepticism about whether it works, whether the provider is qualified, whether the results are real, and whether the person will be taken advantage of. This agent surfaces trust barriers and suggests article topics that build credibility and transparency.

### 17. Stage of Awareness Agent
**Perspective:** Where is the person in their awareness journey? Based on Eugene Schwartz's five stages: unaware, problem-aware, solution-aware, product-aware, and most aware. Different content is needed for each stage. This agent generates article topic suggestions calibrated to each level of awareness so the content meets the reader where they actually are.

### 18. Secret Desires Agent
**Perspective:** What does the person want but feels vain, shallow, or silly admitting? These are the unspoken wants — looking younger, feeling attractive, impressing others, keeping up with peers. This agent surfaces the desires people have but rarely voice and suggests article topics that acknowledge these wants without judgment.

### 19. Fear / Worst Case Agent
**Perspective:** What is the nightmare scenario the person is imagining if they DO act? Not the cost of inaction but the active fear of what could go wrong — botched results, pain, embarrassment, wasted money, making things worse. This agent surfaces specific fears and suggests article topics that acknowledge and address each worst-case scenario directly.

### 20. Money Story Agent
**Perspective:** What is the person's deeper relationship with spending on themselves? Not just "it's too expensive" but the stories they tell about money — guilt about self-investment, how they justify other purchases but not this one, beliefs about what is worth spending on, financial identity. This agent explores money psychology and suggests article topics that speak to the emotional side of the financial decision.

### 21. Past Experience Agent
**Perspective:** What previous bad experiences with similar decisions are coloring this one? A dismissive doctor, a failed attempt, being sold something that did not work, feeling judged or misunderstood. These past wounds create invisible resistance. This agent identifies likely past negative experiences and suggests article topics that acknowledge the baggage and differentiate this experience from what came before.

### 22. Age / Life Stage Agent
**Perspective:** How does the person's specific season of life shape how they see this topic? A 28-year-old and a 55-year-old experience the same topic completely differently. Priorities, constraints, motivations, and fears all shift with age and life stage. This agent generates article topic suggestions tailored to specific age groups or life stages.

### 23. Control / Autonomy Agent
**Perspective:** How does this topic give the person back agency over something they have felt powerless about? Many decisions are driven by a desire to reclaim control — over appearance, health, time, comfort, confidence. This agent explores the powerlessness angle and suggests article topics framed around taking back control.

### 24. Taboo / Shame Agent
**Perspective:** What about this topic feels embarrassing, shameful, or unspeakable? Different from secret desires — this is about the stigma around the problem itself. Things people do not discuss at dinner, search for in incognito mode, or avoid bringing up even with their doctor. This agent surfaces the shame layer and suggests article topics that break the silence and normalize the conversation.

### 25. Catalyst / Tipping Point Agent
**Perspective:** What specific moment, event, or realization typically pushes someone from thinking to acting? There is usually a trigger — a photo, a comment, a health scare, a milestone birthday, a friend's experience. This agent identifies common tipping points and suggests article topics that either recreate that catalytic moment or help the reader recognize they have already had it.

### 26. Decision Catalyst Agent
**Perspective:** What is the one proof point, statistic, or reframe that moves someone from "maybe" to "yes"? While other agents explore broad psychological territory, this agent hunts for the single most powerful piece of evidence or perspective shift that tips the scale. A compelling study, a surprising number, a reframe that makes the decision suddenly obvious. This agent identifies high-leverage decision triggers and suggests article topics built around that one thing that changes minds (e.g., "The one stat that changes how people think about X"). The output is designed to be highly actionable — content that narrows broad research into a single persuasive insight the reader can hold onto.

---

## SEO Title Agent

**Trigger:** Runs automatically when the user selects one or more article ideas and clicks "Generate Briefs." One SEO Title Agent call fires per selected suggestion, in parallel, before any Brief Builder calls.

**Input per call:** The selected suggestion (Sub-Agent Name, Topic, and Justification), the original topic, and the original audience.

**Output:** A single title string (no prefix). Used as the second H1 in each article brief.

**Criteria (condensed):** Remove emotional/editorial flair; use concrete, searchable language. Lead with the primary keyword. Target featured snippets and AEO (questions, definitive answers). Preserve emotional hook without sacrificing clarity. Avoid clickbait; signal genuine informational value. Keep length SERP-safe (55–60 chars). Weave secondary keywords naturally.

---

## Brief Builder Agent

**Trigger:** Runs after the SEO Title Agent completes for each selection. One Brief Builder call fires per selected suggestion. All calls run in parallel. Each call is independent.

**Input per call:** The selected suggestion (Sub-Agent Name, Topic, and Justification), the SEO title from the prior step, the original topic, and the original audience.

**Output per call:** A complete article brief containing:
- **Justification** — Why this article matters and why it will resonate with the audience
- **Suggested Outline** — Section-by-section structure for the article
- **Guideline Bullets Under Each Heading** — Specific points, angles, and details the writer should cover in each section
- **Customized CTA** — A call to action tailored to the emotional and psychological state of the reader after consuming this specific article

**Export options:**
- **Zipped individual files** — Each brief as its own document, all bundled into a single .zip download
- **Individual export** — Download any single brief on its own
