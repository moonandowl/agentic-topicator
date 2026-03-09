"""LLM provider abstraction for Anthropic, OpenAI, Google, and Perplexity."""

from typing import Literal

Provider = Literal["anthropic", "openai", "google", "perplexity"]


async def completions(
    provider: Provider,
    system_prompt: str,
    user_message: str,
    api_keys: dict[str, str],
    timeout: float = 90.0,
    model_overrides: dict | None = None,
) -> str:
    """Call the appropriate LLM and return the text response."""
    overrides = model_overrides or {}
    if provider == "anthropic":
        return await _anthropic(
            system_prompt,
            user_message,
            api_keys,
            timeout,
            overrides.get("anthropic"),
        )
    if provider == "openai":
        return await _openai(
            system_prompt, user_message, api_keys, timeout, overrides.get("openai")
        )
    if provider == "google":
        return await _google(
            system_prompt, user_message, api_keys, timeout, overrides.get("google")
        )
    if provider == "perplexity":
        return await _perplexity(
            system_prompt,
            user_message,
            api_keys,
            timeout,
            overrides.get("perplexity"),
        )
    raise ValueError(f"Unknown provider: {provider}")


async def _anthropic(
    system_prompt: str,
    user_message: str,
    api_keys: dict[str, str],
    timeout: float,
    model: str | None = None,
) -> str:
    import anthropic

    client = anthropic.AsyncAnthropic(api_key=api_keys.get("anthropic", ""))
    response = await client.messages.create(
        model=model or "claude-opus-4-6",
        max_tokens=2048,
        system=system_prompt,
        messages=[{"role": "user", "content": user_message}],
    )
    return response.content[0].text


async def _openai(
    system_prompt: str,
    user_message: str,
    api_keys: dict[str, str],
    timeout: float,
    model: str | None = None,
) -> str:
    from openai import AsyncOpenAI

    client = AsyncOpenAI(api_key=api_keys.get("openai", ""))
    response = await client.chat.completions.create(
        model=model or "gpt-4o",
        messages=[
            {"role": "system", "content": system_prompt},
            {"role": "user", "content": user_message},
        ],
        timeout=timeout,
    )
    return response.choices[0].message.content or ""


async def _google(
    system_prompt: str,
    user_message: str,
    api_keys: dict[str, str],
    timeout: float,
    model: str | None = None,
) -> str:
    from google import genai
    from google.genai import types

    client = genai.Client(api_key=api_keys.get("google", ""))
    async with client.aio as aclient:
        response = await aclient.models.generate_content(
            model=model or "gemini-2.0-flash",
            contents=user_message,
            config=types.GenerateContentConfig(
                system_instruction=system_prompt,
                temperature=0.7,
                max_output_tokens=2048,
            ),
        )
    return response.text or ""


def _inject_perplexity_citations(content: str, citations: list[str]) -> str:
    """Replace [1], [2], etc. with actual URLs from Perplexity citations array."""
    if not citations:
        return content
    import re
    pattern = re.compile(r"\[(\d+)\]")

    def replace_match(m):
        n = int(m.group(1))
        idx = n - 1
        if 0 <= idx < len(citations):
            return f" ({citations[idx]})"
        return m.group(0)

    return pattern.sub(replace_match, content)


async def _perplexity(
    system_prompt: str,
    user_message: str,
    api_keys: dict[str, str],
    timeout: float,
    model: str | None = None,
) -> str:
    import httpx

    api_key = api_keys.get("perplexity", "")
    payload = {
        "model": model or "sonar-pro",
        "messages": [
            {"role": "system", "content": system_prompt},
            {"role": "user", "content": user_message},
        ],
        "max_tokens": 2048,
    }
    async with httpx.AsyncClient(timeout=timeout) as client:
        r = await client.post(
            "https://api.perplexity.ai/chat/completions",
            headers={
                "Authorization": f"Bearer {api_key}",
                "Content-Type": "application/json",
            },
            json=payload,
        )
        r.raise_for_status()
        data = r.json()
    content = (
        data.get("choices", [{}])[0]
        .get("message", {})
        .get("content")
        or ""
    )
    citations = data.get("citations") or []
    if isinstance(citations, (list, tuple)) and citations:
        return _inject_perplexity_citations(content, list(citations))
    return content
