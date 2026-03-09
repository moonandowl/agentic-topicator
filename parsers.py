"""Parse structured output from LLM responses."""

import re

from models import Suggestion


def parse_suggestions(text: str, agent_name: str) -> list[Suggestion]:
    """Parse sub-agent output format into Suggestion objects."""
    suggestions: list[Suggestion] = []
    pattern = re.compile(
        r"Sub-Agent Name:\s*(.+?)\s*\nTopic:\s*(.+?)\s*\nJustification:\s*(.+?)(?=\n\nSub-Agent Name:|\Z)",
        re.DOTALL,
    )
    for match in pattern.finditer(text):
        name = match.group(1).strip()
        topic = match.group(2).strip()
        justification = match.group(3).strip()
        if name and topic and justification:
            suggestions.append(
                Suggestion(
                    sub_agent_name=name,
                    topic=topic,
                    justification=justification,
                )
            )
    # Fallback: simpler line-by-line parse
    if not suggestions and "Topic:" in text:
        lines = text.strip().split("\n")
        i = 0
        while i < len(lines) - 2:
            if "Sub-Agent Name:" in lines[i]:
                name = lines[i].split(":", 1)[1].strip()
                i += 1
                if i < len(lines) and "Topic:" in lines[i]:
                    topic = lines[i].split(":", 1)[1].strip()
                    i += 1
                    if i < len(lines) and "Justification:" in lines[i]:
                        justification = lines[i].split(":", 1)[1].strip()
                        suggestions.append(
                            Suggestion(
                                sub_agent_name=name,
                                topic=topic,
                                justification=justification,
                            )
                        )
                        i += 1
            i += 1
    return suggestions[:3]
