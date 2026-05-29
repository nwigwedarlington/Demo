from __future__ import annotations

import json
import uuid
from dataclasses import asdict, dataclass
from datetime import UTC, datetime


@dataclass
class Comment:
    author: str
    comment: str
    likes: int = 0
    reply_count: int = 0
    timestamp: str = ""


@dataclass
class Transcript:
    transcript: str
    language: str
    confidence: float


def clean_comments(comments: list[Comment]) -> list[Comment]:
    seen: set[tuple[str, str]] = set()
    cleaned: list[Comment] = []
    for item in comments:
        text = item.comment.strip()
        key = (item.author.lower().strip(), text.lower())
        if not text or key in seen:
            continue
        if any(token in text.lower() for token in ["buy followers", "free crypto", "whatsapp me"]):
            continue
        seen.add(key)
        cleaned.append(Comment(item.author, text, item.likes, item.reply_count, item.timestamp))
    return cleaned


def demo_fact_check(transcript: Transcript, comments: list[Comment]) -> dict:
    if not transcript.transcript and not comments:
        return {
            "verified_facts": [],
            "false_claims": [],
            "uncertain_claims": ["No content was available to verify."],
            "sources_or_reasoning": [],
        }
    return {
        "verified_facts": [],
        "false_claims": [],
        "uncertain_claims": [
            "Demo mode: external AI is disabled, so factual claims require human review."
        ],
        "sources_or_reasoning": [
            "The workflow reached the AI step successfully.",
            "Set AI_FREE_DEMO_MODE=false with Grok/Gemini keys for live analysis.",
        ],
    }


def build_publish_payload(result: dict) -> dict:
    false_count = len(result["false_claims"])
    uncertain_count = len(result["uncertain_claims"])
    risk_score = min(100, false_count * 45 + uncertain_count * 20)
    return {
        "title": "Facebook fact-check ready for review",
        "summary": f"{uncertain_count} uncertain claim(s) require review.",
        "fact_check_result": json.dumps(result),
        "hashtags": ["#FactCheck", "#MediaLiteracy"],
        "risk_score": risk_score,
        "publish_ready": risk_score < 70,
    }


def main() -> None:
    job = {
        "id": str(uuid.uuid4()),
        "url": "https://www.facebook.com/example/videos/123456789",
        "source_type": "video",
        "status": "queued",
        "attempts": 0,
        "created_at": datetime.now(UTC).isoformat(),
    }

    print("1. Job created")
    print(json.dumps(job, indent=2))

    job["status"] = "processing"
    job["attempts"] += 1

    metadata = {"source": "free-demo", "likes": 0, "shares": 0, "url": job["url"]}
    comments = clean_comments(
        [
            Comment("demo-user", "This needs verification before publishing."),
            Comment("demo-user", "This needs verification before publishing."),
            Comment("spam", "buy followers now"),
            Comment("viewer", "Can someone check if this claim is true?", likes=2),
        ]
    )

    print("\n2. Scraper normalized comments")
    print(json.dumps({"metadata": metadata, "comments": [asdict(c) for c in comments]}, indent=2))

    transcript = Transcript(
        transcript=(
            "Demo transcript: the video makes a public claim that should be checked "
            "against trusted sources before publishing."
        ),
        language="en",
        confidence=0.5,
    )

    print("\n3. Transcript extracted")
    print(json.dumps(asdict(transcript), indent=2))

    result = demo_fact_check(transcript, comments)
    print("\n4. AI fact-check result")
    print(json.dumps(result, indent=2))

    payload = build_publish_payload(result)
    print("\n5. Publish-ready payload")
    print(json.dumps(payload, indent=2))

    job["status"] = "completed"
    print("\n6. Final job status")
    print(json.dumps(job, indent=2))

    print("\nFailure alert example")
    print(
        "ALERT: WORKFLOW FAILURE\n"
        "Service: queue-worker\n"
        f"URL: {job['url']}\n"
        "Error: Example transient timeout\n"
        f"Timestamp: {datetime.now(UTC).isoformat()}"
    )


if __name__ == "__main__":
    main()
