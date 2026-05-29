from app.core.config import get_settings
from app.schemas.factcheck import NormalizedComment


class FacebookScraper:
    async def scrape(self, url: str) -> tuple[dict, list[NormalizedComment]]:
        settings = get_settings()
        if settings.scraper_free_demo_mode or not settings.apify_api_token:
            return (
                {"source": "free-demo", "url": url, "likes": 0, "shares": 0},
                [
                    NormalizedComment(
                        author="demo-user",
                        comment="This needs verification before publishing.",
                        likes=0,
                        reply_count=0,
                        timestamp="",
                    )
                ],
            )
        return await self._scrape_with_apify(url)

    async def _scrape_with_apify(self, url: str) -> tuple[dict, list[NormalizedComment]]:
        # Hook point for Apify actor runs. Keep this isolated because actor inputs differ by plan/version.
        # Recommended production flow: call actor, poll dataset, normalize all rows here.
        raise NotImplementedError("Apify live scraping is configured here for your chosen actor input schema")


def dedupe_and_clean_comments(comments: list[NormalizedComment]) -> list[NormalizedComment]:
    seen: set[tuple[str, str]] = set()
    cleaned: list[NormalizedComment] = []
    for comment in comments:
        text = comment.comment.strip()
        if not text:
            continue
        key = (comment.author.strip().lower(), text.lower())
        if key in seen:
            continue
        if any(token in text.lower() for token in ["buy followers", "free crypto", "whatsapp me"]):
            continue
        seen.add(key)
        cleaned.append(comment.model_copy(update={"comment": text}))
    return cleaned
