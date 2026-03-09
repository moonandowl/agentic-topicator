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
        model=model or "gpt-5.4-pro",
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

    client = genai.Client(api_key=api_keys.get("google", ""))
    async with client.aio as aclient:
        response = await aclient.models.generate_content(
            model=model or "gemini-3.1-pro-preview",
            contents=f"{system_prompt}\n\n---\n\n{user_message}",
            config={"temperature": 0.7, "max_output_tokens": 2048},
        )
    return response.text or ""


async def _perplexity(
    system_prompt: str,
    user_message: str,
    api_keys: dict[str, str],
    timeout: float,
    model: str | None = None,
) -> str:
    from openai import AsyncOpenAI

    client = AsyncOpenAI(
        api_key=api_keys.get("perplexity", ""),
        base_url="https://api.perplexity.ai",
    )
    response = await client.chat.completions.create(
        model=model or "sonar-pro",
        messages=[
            {"role": "system", "content": system_prompt},
            {"role": "user", "content": user_message},
        ],
        timeout=timeout,
    )
    return response.choices[0].message.content or ""
