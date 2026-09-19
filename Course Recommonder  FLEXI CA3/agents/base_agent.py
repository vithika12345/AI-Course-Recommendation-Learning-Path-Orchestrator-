"""
Base Agent Implementation
Provides unified LLM access (Groq, OpenAI, Google Gemini)
and an intelligent offline heuristic engine for offline viva demos.
"""

import os
import json
import time
from typing import Dict, Any, Optional, List
import requests


class BaseAgent:
    """
    Base Agent class offering LLM invocation with multi-provider support
    and robust fallback mechanisms.
    """

    def __init__(
        self,
        name: str,
        role: str,
        provider: str = "offline",
        api_key: Optional[str] = None,
        model: Optional[str] = None
    ):
        self.name = name
        self.role = role
        self.provider = provider.lower() if provider else "offline"
        self.api_key = api_key or os.getenv("LLM_API_KEY", "")
        self.model = model or self._default_model(self.provider)

    def _default_model(self, provider: str) -> str:
        provider = provider.lower()
        if provider == "groq":
            return "llama-3.3-70b-versatile"
        elif provider == "openai":
            return "gpt-4o-mini"
        elif provider == "gemini":
            return "gemini-1.5-flash"
        return "heuristic-offline"

    def call_llm(
        self,
        system_prompt: str,
        user_prompt: str,
        temperature: float = 0.3,
        max_tokens: int = 1500
    ) -> Dict[str, Any]:
        """
        Invokes configured LLM provider.
        Returns a dict with:
        - content: str
        - duration_s: float
        - provider: str
        - model: str
        """
        start_time = time.time()

        # If offline or no API key, invoke heuristic engine
        if self.provider == "offline" or not self.api_key:
            content = self._heuristic_fallback(system_prompt, user_prompt)
            duration = round(time.time() - start_time, 3)
            return {
                "content": content,
                "duration_s": max(0.1, duration),
                "provider": "Local Heuristic Engine",
                "model": "offline-rule-agent"
            }

        try:
            if self.provider == "groq":
                content = self._call_openai_compatible(
                    endpoint="https://api.groq.com/openai/v1/chat/completions",
                    system_prompt=system_prompt,
                    user_prompt=user_prompt,
                    temperature=temperature,
                    max_tokens=max_tokens
                )
            elif self.provider == "openai":
                content = self._call_openai_compatible(
                    endpoint="https://api.openai.com/v1/chat/completions",
                    system_prompt=system_prompt,
                    user_prompt=user_prompt,
                    temperature=temperature,
                    max_tokens=max_tokens
                )
            elif self.provider == "gemini":
                content = self._call_gemini(
                    system_prompt=system_prompt,
                    user_prompt=user_prompt,
                    temperature=temperature
                )
            else:
                content = self._heuristic_fallback(system_prompt, user_prompt)
        except Exception as e:
            # Fallback smoothly so app never crashes
            content = self._heuristic_fallback(
                system_prompt,
                user_prompt,
                fallback_reason=f"API connection error ({str(e)}). Switched to offline heuristic agent."
            )

        duration = round(time.time() - start_time, 3)
        return {
            "content": content,
            "duration_s": duration,
            "provider": self.provider.title(),
            "model": self.model
        }

    def _call_openai_compatible(
        self,
        endpoint: str,
        system_prompt: str,
        user_prompt: str,
        temperature: float,
        max_tokens: int
    ) -> str:
        headers = {
            "Authorization": f"Bearer {self.api_key}",
            "Content-Type": "application/json"
        }
        payload = {
            "model": self.model,
            "messages": [
                {"role": "system", "content": system_prompt},
                {"role": "user", "content": user_prompt}
            ],
            "temperature": temperature,
            "max_tokens": max_tokens
        }
        resp = requests.post(endpoint, json=payload, headers=headers, timeout=25)
        resp.raise_for_status()
        data = resp.json()
        return data["choices"][0]["message"]["content"]

    def _call_gemini(self, system_prompt: str, user_prompt: str, temperature: float) -> str:
        url = f"https://generativelanguage.googleapis.com/v1beta/models/{self.model}:generateContent?key={self.api_key}"
        payload = {
            "contents": [
                {
                    "parts": [
                        {"text": f"System Context:\n{system_prompt}\n\nTask:\n{user_prompt}"}
                    ]
                }
            ],
            "generationConfig": {
                "temperature": temperature,
                "maxOutputTokens": 1500
            }
        }
        resp = requests.post(url, json=payload, headers={"Content-Type": "application/json"}, timeout=25)
        resp.raise_for_status()
        data = resp.json()
        return data["candidates"][0]["content"]["parts"][0]["text"]

    def _heuristic_fallback(
        self,
        system_prompt: str,
        user_prompt: str,
        fallback_reason: Optional[str] = None
    ) -> str:
        """Subclasses should implement or customize heuristic fallback output."""
        return "Heuristic fallback response generated by base agent."
