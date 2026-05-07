"""Adapter that streams from either OpenAI- or Anthropic-format LLM endpoints."""
from __future__ import annotations

import json
import logging
from typing import AsyncIterator

import httpx

from .config import settings

log = logging.getLogger(__name__)


class LLMProxy:
    def __init__(self) -> None:
        self.fmt = settings.LLM_FORMAT
        self.endpoint = settings.LLM_ENDPOINT.rstrip("/")
        self.api_key = settings.LLM_API_KEY
        self.model = settings.LLM_MODEL
        self.timeout = settings.LLM_TIMEOUT_SECONDS

    async def stream(self, system: str, messages: list[dict]) -> AsyncIterator[str]:
        if self.fmt == "openai":
            async for token in self._stream_openai(system, messages):
                yield token
        elif self.fmt == "anthropic":
            async for token in self._stream_anthropic(system, messages):
                yield token
        else:
            yield f"[Unsupported LLM_FORMAT: {self.fmt}]"

    async def _stream_openai(self, system: str, messages: list[dict]) -> AsyncIterator[str]:
        url = f"{self.endpoint}/chat/completions"
        body = {
            "model": self.model,
            "messages": [{"role": "system", "content": system}, *messages],
            "stream": True,
        }
        headers = {
            "Authorization": f"Bearer {self.api_key}",
            "Content-Type": "application/json",
        }

        async with httpx.AsyncClient(timeout=self.timeout) as client:
            try:
                async with client.stream("POST", url, json=body, headers=headers) as resp:
                    if resp.status_code >= 400:
                        text = await resp.aread()
                        yield f"[LLM error {resp.status_code}: {text.decode('utf-8', errors='replace')[:500]}]"
                        return
                    async for line in resp.aiter_lines():
                        if not line or not line.startswith("data:"):
                            continue
                        payload = line[5:].strip()
                        if payload == "[DONE]":
                            return
                        try:
                            obj = json.loads(payload)
                        except json.JSONDecodeError:
                            continue
                        choices = obj.get("choices") or []
                        if not choices:
                            continue
                        delta = choices[0].get("delta") or {}
                        content = delta.get("content")
                        if content:
                            yield content
            except httpx.RequestError as exc:
                log.exception("OpenAI proxy error")
                yield f"[Connection error: {exc}]"

    async def _stream_anthropic(self, system: str, messages: list[dict]) -> AsyncIterator[str]:
        url = f"{self.endpoint}/messages"
        body = {
            "model": self.model,
            "system": system,
            "messages": messages,
            "max_tokens": 4096,
            "stream": True,
        }
        headers = {
            "x-api-key": self.api_key,
            "anthropic-version": "2023-06-01",
            "Content-Type": "application/json",
        }

        async with httpx.AsyncClient(timeout=self.timeout) as client:
            try:
                async with client.stream("POST", url, json=body, headers=headers) as resp:
                    if resp.status_code >= 400:
                        text = await resp.aread()
                        yield f"[LLM error {resp.status_code}: {text.decode('utf-8', errors='replace')[:500]}]"
                        return
                    async for line in resp.aiter_lines():
                        if not line or not line.startswith("data:"):
                            continue
                        payload = line[5:].strip()
                        if not payload:
                            continue
                        try:
                            obj = json.loads(payload)
                        except json.JSONDecodeError:
                            continue
                        if obj.get("type") == "content_block_delta":
                            delta = obj.get("delta") or {}
                            text = delta.get("text")
                            if text:
                                yield text
                        elif obj.get("type") == "message_stop":
                            return
            except httpx.RequestError as exc:
                log.exception("Anthropic proxy error")
                yield f"[Connection error: {exc}]"


proxy = LLMProxy()
