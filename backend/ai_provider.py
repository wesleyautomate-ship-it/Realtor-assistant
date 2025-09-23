"""
AI Provider (OpenAI-only)
-------------------------

This module exposes a stable interface for AI text generation using OpenAI.
Per product decision, OpenAI is the sole provider for PropertyPro AI.

Usage:
    from ai_provider import get_ai_provider
    provider = get_ai_provider()
    result = provider.generate_content(prompt)
    text = getattr(result, "text", None) or getattr(result, "content", None)

Configuration (env variables):
    OPENAI_API_KEY (required)
    OPENAI_MODEL (default: gpt-4o-mini)
"""
from __future__ import annotations

import os
from types import SimpleNamespace
from typing import Any


class AIProviderBase:
    """Base interface for AI providers."""

    def generate_content(self, prompt: str) -> Any:
        raise NotImplementedError


class OpenAIProvider(AIProviderBase):
    def __init__(self, api_key: str, model_name: str):
        # Support both the legacy and new OpenAI clients gracefully
        self._api_key = api_key
        self._model = model_name
        try:
            # Newer SDK style
            from openai import OpenAI  # type: ignore
            self._client = OpenAI(api_key=api_key)
            self._mode = "new"
        except Exception:
            # Legacy SDK fallback
            import openai  # type: ignore
            openai.api_key = api_key
            self._openai = openai
            self._mode = "legacy"

    def generate_content(self, prompt: str) -> Any:
        # Normalize output to object with `.text`
        try:
            if getattr(self, "_mode", "legacy") == "new":
                # New SDK responses API
                try:
                    # Prefer Responses API when available
                    resp = self._client.responses.create(
                        model=self._model,
                        input=prompt,
                    )
                    content = resp.output_text  # Unified text accessor
                except Exception:
                    # Fallback to chat.completions
                    resp = self._client.chat.completions.create(
                        model=self._model,
                        messages=[{"role": "user", "content": prompt}],
                    )
                    content = resp.choices[0].message.content
            else:
                # Legacy SDK chat completion
                resp = self._openai.ChatCompletion.create(
                    model=self._model,
                    messages=[{"role": "user", "content": prompt}],
                    temperature=0.7,
                )
                content = resp["choices"][0]["message"]["content"]

            return SimpleNamespace(text=content)
        except Exception as e:
            # Surface an informative error while keeping interface consistent
            return SimpleNamespace(text=f"[AI Error] {e}")


def get_ai_provider() -> AIProviderBase:
    api_key = os.getenv("OPENAI_API_KEY", "").strip()
    model_name = os.getenv("OPENAI_MODEL", "gpt-4o-mini").strip()
    if not api_key:
        raise RuntimeError("OPENAI_API_KEY is required for PropertyPro AI")
    return OpenAIProvider(api_key=api_key, model_name=model_name)
