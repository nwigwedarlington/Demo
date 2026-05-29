from app.schemas.factcheck import FactCheckResult, PublishPayload


class PublishingService:
    def build_payload(self, url: str, result: FactCheckResult) -> PublishPayload:
        false_count = len(result.false_claims)
        uncertain_count = len(result.uncertain_claims)
        risk_score = min(100, false_count * 45 + uncertain_count * 20)
        title = "Facebook fact-check ready for review"
        if false_count:
            summary = f"{false_count} false claim(s) found."
        elif uncertain_count:
            summary = f"{uncertain_count} uncertain claim(s) require review."
        else:
            summary = "No false claims identified by the configured AI provider."
        return PublishPayload(
            title=title,
            summary=summary,
            fact_check_result=result.model_dump_json(),
            hashtags=["#FactCheck", "#MediaLiteracy"],
            risk_score=risk_score,
            publish_ready=risk_score < 70,
        )
