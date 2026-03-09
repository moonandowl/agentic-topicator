"""Orchestration: generate_topics and generate_briefs."""

import asyncio
from typing import Literal

from agents import BRIEF_BUILDER_SYSTEM, SUB_AGENT_FORMAT, SUB_AGENTS
from llm import completions
from models import AgentResult, Brief, Suggestion
from parsers import parse_suggestions

Provider = Literal["anthropic", "openai", "google", "perplexity"]


def _api_keys(settings, provider: Provider) -> dict[str, str]:
    return {
        "anthropic": settings.anthropic_api_key,
        "openai": settings.openai_api_key,
        "google": settings.google_api_key,
        "perplexity": settings.perplexity_api_key,
    }


def _model_overrides(settings) -> dict:
    if not settings:
        return {}
    return {
        "anthropic": getattr(settings, "anthropic_model", None),
        "openai": getattr(settings, "openai_model", None),
        "google": getattr(settings, "google_model", None),
        "perplexity": getattr(settings, "perplexity_model", None),
    }


async def _run_sub_agent(
    agent_name: str,
    perspective: str,
    topic: str,
    audience: str,
    provider: Provider,
    api_keys: dict[str, str],
    settings,
) -> AgentResult:
    system = f"""You are the {agent_name} agent.

Your perspective: {perspective}

You must return exactly 3 article topic suggestions for the given topic and audience.
Each suggestion must be a specific, article-worthy idea — not abstract analysis.

""" + SUB_AGENT_FORMAT.format(agent_name=agent_name)

    user = f"Topic: {topic}\nAudience: {audience}"

    try:
        text = await completions(
            provider,
            system,
            user,
            api_keys,
            timeout=60.0,
            model_overrides=_model_overrides(settings),
        )
        suggestions = parse_suggestions(text, agent_name)
        if not suggestions:
            # Use raw lines as fallback if parse fails
            suggestions = [
                Suggestion(sub_agent_name=agent_name, topic=topic, justification=text[:200])
            ]
        return AgentResult(agent_name=agent_name, suggestions=suggestions, error=None)
    except Exception as e:
        return AgentResult(
            agent_name=agent_name,
            suggestions=[],
            error=str(e),
        )


async def generate_topics(
    topic: str,
    audience: str,
    provider: Provider,
    settings,
) -> list[AgentResult]:
    """Run all 26 sub-agents in parallel."""
    api_keys = _api_keys(settings, provider)
    tasks = [
        _run_sub_agent(
            name, perspective, topic, audience, provider, api_keys, settings
        )
        for name, perspective in SUB_AGENTS
    ]
    results = await asyncio.gather(*tasks, return_exceptions=True)
    out: list[AgentResult] = []
    for i, r in enumerate(results):
        if isinstance(r, Exception):
            out.append(
                AgentResult(
                    agent_name=SUB_AGENTS[i][0],
                    suggestions=[],
                    error=str(r),
                )
            )
        else:
            out.append(r)
    return out


async def _run_brief_builder(
    selection: Suggestion,
    original_topic: str,
    original_audience: str,
    provider: Provider,
    api_keys: dict[str, str],
    settings,
) -> Brief:
    user = f"""Selected suggestion:
Sub-Agent: {selection.sub_agent_name}
Topic: {selection.topic}
Justification: {selection.justification}

Original topic: {original_topic}
Original audience: {original_audience}
"""
    try:
        content = await completions(
            provider,
            BRIEF_BUILDER_SYSTEM,
            user,
            api_keys,
            timeout=90.0,
            model_overrides=_model_overrides(settings),
        )
        return Brief(selection=selection, content=content, error=None)
    except Exception as e:
        return Brief(selection=selection, content="", error=str(e))


async def generate_briefs(
    selections: list[Suggestion],
    original_topic: str,
    original_audience: str,
    provider: Provider,
    settings,
) -> list[Brief]:
    """Run Brief Builder once per selection in parallel."""
    api_keys = _api_keys(settings, provider)
    tasks = [
        _run_brief_builder(
            s, original_topic, original_audience, provider, api_keys, settings
        )
        for s in selections
    ]
    return await asyncio.gather(*tasks, return_exceptions=False)
