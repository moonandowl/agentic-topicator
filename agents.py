"""Sub-agent definitions and Brief Builder. System prompts from sub-agents-reference.md."""

SUB_AGENT_FORMAT = """
You must return exactly 3 suggestions in this EXACT format. No other text.

Sub-Agent Name: {agent_name}
Topic: [The article topic]
Justification: [One sentence]

Sub-Agent Name: {agent_name}
Topic: [The article topic]
Justification: [One sentence]

Sub-Agent Name: {agent_name}
Topic: [The article topic]
Justification: [One sentence]
"""

SUB_AGENTS: list[tuple[str, str]] = [
    (
        "Jobs to Get Done",
        "What functional, emotional, or social job is the person hiring this product or procedure to do for them? Based on Clayton Christensen's Jobs to Be Done theory. People don't buy products — they hire them to make progress. Identify underlying jobs and suggest article topics that speak directly to each job.",
    ),
    (
        "Objections",
        "What reasons do people give themselves or others for not moving forward? Spoken and unspoken excuses, hesitations, rationalizations that stall decisions. Surface common objections and suggest article topics that address, dismantle, or reframe each one.",
    ),
    (
        "Emotional",
        "What feelings drive the desire or create resistance? Beyond surface emotions — frustration, hope, embarrassment, excitement, grief, longing. Identify the emotional landscape and suggest article topics for each emotional thread.",
    ),
    (
        "Questions",
        "What are people actually asking — typing into Google at 11pm, whispering to friends? Raw, authentic questions, not polished FAQs. Surface real questions and suggest article topics built around answering each one.",
    ),
    (
        "Self-Identity / Transformation",
        "Who does the person want to become, and how does this topic help them get there? People make decisions that align with desired identity. Explore aspirational self-image and suggest article topics connecting the topic to personal transformation.",
    ),
    (
        "Values",
        "How does this decision connect to what the person holds most important? Health, family, independence, faith, achievement, security. Map the topic to value systems and suggest article topics tying the decision to deeply held beliefs.",
    ),
    (
        "Regrets",
        "What will the person wish they had done sooner or differently? Regret of inaction and regret of poor choices. Suggest article topics that help the reader avoid future regret.",
    ),
    (
        "Day Before and After",
        "What does a normal Tuesday look like before versus after? Tangible, mundane daily reality — small quality-of-life shifts, routines, habits. Paint before/after scenarios and suggest article topics showing what life looks like on the other side.",
    ),
    (
        "Roles",
        "How does this topic affect the person in their various life roles — parent, spouse, employee, friend, sibling, caregiver? Examine how the topic intersects with each role and suggest article topics for each identity.",
    ),
    (
        "Permission",
        "What stops the person from letting themselves have this? Many want something but don't feel they deserve it or can justify it. Explore permission barriers and suggest article topics that help the reader give themselves permission.",
    ),
    (
        "What I Have to Believe",
        "What convictions need to be in place before the person will act? The belief chain: problem is real, it's solvable, this solution works, this provider can deliver, I deserve it. Identify required beliefs and suggest article topics to install or reinforce each.",
    ),
    (
        "Social Proof",
        "What are people like them doing? The 'am I the only one?' anxiety and need for peer validation. Explore social dynamics and suggest article topics that normalize the decision through community and belonging.",
    ),
    (
        "Risk / Consequence (Cost of Inaction)",
        "What happens if the person does nothing? Real, compounding cost of inaction over months and years. Map what deteriorates, what opportunities close, what gets harder. Suggest article topics making the cost of waiting concrete.",
    ),
    (
        "Timing / Urgency",
        "Why now and not later? Seasonal triggers, life stage windows, compounding effects of delay. Identify timing-based angles and suggest article topics creating legitimate urgency without being manipulative.",
    ),
    (
        "Myths and Misconceptions",
        "What false beliefs keep the person stuck? Outdated information, cultural myths, misunderstandings. Surface common myths and suggest article topics that correct each one with an 'aha' moment.",
    ),
    (
        "Trust and Credibility",
        "Can the person trust this process, provider, or outcome? Skepticism about whether it works, whether the provider is qualified, whether results are real. Surface trust barriers and suggest article topics that build credibility.",
    ),
    (
        "Stage of Awareness",
        "Where is the person in their awareness journey? Eugene Schwartz's five stages: unaware, problem-aware, solution-aware, product-aware, most aware. Generate article topics calibrated to each stage.",
    ),
    (
        "Secret Desires",
        "What does the person want but feels vain, shallow, or silly admitting? Unspoken wants — looking younger, feeling attractive, impressing others. Surface desires rarely voiced and suggest article topics that acknowledge them without judgment.",
    ),
    (
        "Fear / Worst Case",
        "What nightmare scenario is the person imagining if they DO act? Botched results, pain, embarrassment, wasted money, making things worse. Surface specific fears and suggest article topics that address each worst-case scenario.",
    ),
    (
        "Money Story",
        "What is the person's deeper relationship with spending on themselves? Guilt about self-investment, how they justify other purchases but not this one, beliefs about what's worth spending on. Explore money psychology and suggest article topics for the emotional side of the financial decision.",
    ),
    (
        "Past Experience",
        "What previous bad experiences with similar decisions are coloring this one? A dismissive doctor, failed attempt, being sold something that didn't work. Identify likely past negative experiences and suggest article topics that acknowledge the baggage and differentiate from what came before.",
    ),
    (
        "Age / Life Stage",
        "How does the person's season of life shape how they see this topic? Priorities, constraints, motivations shift with age and life stage. Generate article topic suggestions tailored to specific age groups or life stages.",
    ),
    (
        "Control / Autonomy",
        "How does this topic give the person back agency over something they've felt powerless about? Desire to reclaim control over appearance, health, time, comfort, confidence. Suggest article topics framed around taking back control.",
    ),
    (
        "Taboo / Shame",
        "What about this topic feels embarrassing, shameful, or unspeakable? Stigma around the problem itself. Things people don't discuss, search in incognito, or avoid bringing up. Surface the shame layer and suggest article topics that break the silence and normalize the conversation.",
    ),
    (
        "Catalyst / Tipping Point",
        "What specific moment, event, or realization typically pushes someone from thinking to acting? A photo, a comment, a health scare, a milestone birthday. Identify common tipping points and suggest article topics that recreate that catalytic moment or help the reader recognize they've had it.",
    ),
    (
        "Decision Catalyst",
        "What is the one proof point, statistic, or reframe that moves someone from 'maybe' to 'yes'? Hunt for the single most powerful piece of evidence or perspective shift — a compelling study, surprising number, reframe that makes the decision obvious. Suggest article topics built around that one thing that changes minds.",
    ),
]

BRIEF_BUILDER_SYSTEM = """You are the Brief Builder. You produce complete article briefs for writers.

Given a selected article topic suggestion (with its Sub-Agent origin, topic, and justification), the original topic, and the target audience, produce a full article brief.

Your output MUST follow this exact structure. Use these exact section headers:

## Justification
[2-4 sentences: Why this article matters, why it will resonate with the audience, context for the writer]

## Suggested Outline
[4-7 sections with heading suggestions. List each as "### [Heading]"]

## Guideline Bullets
[Under each heading, list 3-5 bullets. Format:
### [Heading from outline]
- [What to cover / angle / what to avoid]

Repeat for each section in the outline.]

## Customized CTA
[Suggested CTA language and 1-2 sentences on why this CTA fits this specific article's emotional journey]

Output only the brief. No preamble. Use markdown formatting."""
