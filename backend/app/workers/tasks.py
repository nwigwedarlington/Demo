import asyncio
import traceback
from uuid import UUID

import dramatiq
from dramatiq.brokers.redis import RedisBroker

from app.core.config import get_settings
from app.db.session import AsyncSessionLocal
from app.models.entities import (
    Comment,
    FactCheck,
    Failure,
    Job,
    JobStatus,
    PublishQueue,
    ScrapedPost,
    Transcript,
)
from app.services.ai import FactCheckEngine
from app.services.notifications import NotificationService
from app.services.publishing import PublishingService
from app.services.scraper import FacebookScraper, dedupe_and_clean_comments
from app.services.transcript import TranscriptService

settings = get_settings()
broker = RedisBroker(url=settings.redis_url)
dramatiq.set_broker(broker)


@dramatiq.actor(max_retries=3, time_limit=600000)
def process_job(job_id: str) -> None:
    asyncio.run(_process_job(UUID(job_id)))


async def _process_job(job_id: UUID) -> None:
    async with AsyncSessionLocal() as db:
        job = await db.get(Job, job_id)
        if not job:
            return
        try:
            job.status = JobStatus.processing.value
            job.attempts += 1
            await db.commit()

            metadata, raw_comments = await FacebookScraper().scrape(job.url)
            comments = dedupe_and_clean_comments(raw_comments)
            post = ScrapedPost(job_id=job.id, url=job.url, post_metadata=metadata)
            db.add(post)
            await db.flush()
            for comment in comments:
                db.add(Comment(post_id=post.id, **comment.model_dump()))

            transcript_result = await TranscriptService().extract(job.url)
            db.add(Transcript(job_id=job.id, **transcript_result.model_dump()))

            provider, result = await FactCheckEngine().analyze(transcript_result.transcript, comments)
            db.add(FactCheck(job_id=job.id, provider=provider, result=result.model_dump()))

            publish_payload = PublishingService().build_payload(job.url, result)
            db.add(PublishQueue(job_id=job.id, channel="webhook", payload=publish_payload.model_dump()))

            job.status = JobStatus.completed.value
            job.last_error = None
            await db.commit()
        except Exception as exc:
            summary = traceback.format_exc(limit=8)
            job.status = JobStatus.failed.value
            job.last_error = str(exc)
            db.add(
                Failure(
                    job_id=job.id,
                    service_name="queue-worker",
                    error_message=str(exc),
                    stack_trace_summary=summary,
                )
            )
            await db.commit()
            await NotificationService().telegram_failure("queue-worker", job.url, str(exc), summary)
            raise
