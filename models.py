"""Pydantic models for API requests and responses."""

from typing import List, Literal, Optional

from pydantic import BaseModel

Provider = Literal["anthropic", "openai", "google", "perplexity", "grok"]


class GenerateTopicsRequest(BaseModel):
    topic: str
    audience: str
    model_provider: Provider = "anthropic"


class Suggestion(BaseModel):
    sub_agent_name: str
    topic: str
    justification: str


class AgentResult(BaseModel):
    agent_name: str
    suggestions: List[Suggestion]
    error: Optional[str] = None


class GenerateBriefsRequest(BaseModel):
    selections: List[Suggestion]
    original_topic: str
    original_audience: str
    model_provider: Provider = "anthropic"


class Brief(BaseModel):
    selection: Suggestion
    content: str
    error: Optional[str] = None
