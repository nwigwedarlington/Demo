from pydantic import BaseModel, Field


class NormalizedComment(BaseModel):
    author: str = ""
    comment: str = ""
    likes: int = 0
    reply_count: int = 0
    timestamp: str = ""


class TranscriptResult(BaseModel):
    transcript: str
    language: str = "unknown"
    confidence: float = 0.0


class FactCheckResult(BaseModel):
    verified_facts: list[str] = Field(default_factory=list)
    false_claims: list[str] = Field(default_factory=list)
    uncertain_claims: list[str] = Field(default_factory=list)
    sources_or_reasoning: list[str] = Field(default_factory=list)


class PublishPayload(BaseModel):
    title: str
    summary: str
    fact_check_result: str
    hashtags: list[str]
    risk_score: int
    publish_ready: bool = True
