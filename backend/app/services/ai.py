import json
from abc import ABC, abstractmethod
from typing import Any

import httpx

from app.core.config import get_settings
from app.schemas.factcheck import FactCheckResult, NormalizedComment

FACT_CHECK_SYSTEM_PROMPT = """Extract factual claims from the transcript and comments.
Classify each as VERIFIED, FALSE, or UNCERTAIN.
Never invent sources. Return only valid JSON with keys:
verified_facts, false_claims, uncertain_claims, sources_or_reasoning."""


class ProviderUnavailable(RuntimeError):
    pass


class AIProvider(ABC):
    name: str

    @abstractmethod
    async def analyze(self, transcript: str, comments: list[NormalizedComment]) -> FactCheckResult:
        raise NotImplementedError


class OpenAICompatibleProvider(AIProvider):
    def __init__(self, name: str, base_url: str, api_key: str | None, model: str):
        self.name = name
        self.base_url = base_url.rstrip("/")
        self.api_key = api_key
        self.model = model

    async def analyze(self, transcript: str, comments: list[NormalizedComment]) -> FactCheckResult:
        if not self.api_key:
            raise ProviderUnavailable(f"{self.name} API key is not configured")
        payload = {
            "model": self.model,
            "messages": [
                {"role": "system", "content": FACT_CHECK_SYSTEM_PROMPT},
                {
                    "role": "user",
                    "content": json.dumps(
                        {
                            "transcript": transcript,
                            "comments": [c.model_dump() for c in comments],
                        }
                    ),
                },
            ],
            "response_format": {"type": "json_object"},
            "temperature": 0.1,
        }
        async with httpx.AsyncClient(timeout=45) as client:
            response = await client.post(
                f"{self.base_url}/chat/completions",
                headers={"Authorization": f"Bearer {self.api_key}"},
                json=payload,
            )
        if response.status_code in {401, 402, 403, 408, 429}:
            raise ProviderUnavailable(f"{self.name} failed with {response.status_code}")
        response.raise_for_status()
        content = response.json()["choices"][0]["message"]["content"]
        return FactCheckResult.model_validate_json(content)


class GrokProvider(OpenAICompatibleProvider):
    def __init__(self) -> None:
        settings = get_settings()
        super().__init__("grok", settings.grok_base_url, settings.grok_api_key, settings.grok_model)


class GeminiProvider(OpenAICompatibleProvider):
    def __init__(self) -> None:
        settings = get_settings()
        super().__init__("gemini", settings.gemini_base_url, settings.gemini_api_key, settings.gemini_model)


class DemoProvider(AIProvider):
    name = "free-demo"

    async def analyze(self, transcript: str, comments: list[NormalizedComment]) -> FactCheckResult:
        text = f"{transcript} {' '.join(c.comment for c in comments)}".strip()
        if not text:
            return FactCheckResult(uncertain_claims=["No content was available to verify."])
        return FactCheckResult(
            verified_facts=[],
            false_claims=[],
            uncertain_claims=["Demo mode: external AI is disabled, so claims require human review."],
            sources_or_reasoning=[
                "Set AI_FREE_DEMO_MODE=false and configure Grok/Gemini keys for live analysis."
            ],
        )


class FactCheckEngine:
    def __init__(self, providers: list[AIProvider] | None = None):
        settings = get_settings()
        self.providers = providers or (
            [DemoProvider()] if settings.ai_free_demo_mode else [GrokProvider(), GeminiProvider()]
        )

    async def analyze(self, transcript: str, comments: list[NormalizedComment]) -> tuple[str, FactCheckResult]:
        errors: list[str] = []
        for provider in self.providers:
            try:
                return provider.name, await provider.analyze(transcript, comments)
            except (ProviderUnavailable, httpx.TimeoutException, httpx.HTTPError, KeyError, ValueError) as exc:
                errors.append(f"{provider.name}: {exc}")
                continue
        raise ProviderUnavailable("; ".join(errors))


def result_summary(result: dict[str, Any]) -> str:
    if result.get("false_claims"):
        return "FALSE"
    if result.get("uncertain_claims"):
        return "UNCERTAIN"
    return "VERIFIED"
