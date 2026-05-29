import pytest

from app.schemas.factcheck import FactCheckResult
from app.services.ai import AIProvider, FactCheckEngine, ProviderUnavailable


class FailingProvider(AIProvider):
    name = "failing"

    async def analyze(self, transcript, comments):
        raise ProviderUnavailable("credits exhausted")


class GoodProvider(AIProvider):
    name = "good"

    async def analyze(self, transcript, comments):
        return FactCheckResult(verified_facts=["The fallback provider ran."])


@pytest.mark.asyncio
async def test_ai_failover_uses_next_provider():
    provider, result = await FactCheckEngine([FailingProvider(), GoodProvider()]).analyze("text", [])
    assert provider == "good"
    assert result.verified_facts == ["The fallback provider ran."]
