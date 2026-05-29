from uuid import UUID

from fastapi import APIRouter, Depends, HTTPException
from prometheus_client import CONTENT_TYPE_LATEST, generate_latest
from sqlalchemy import desc, select
from sqlalchemy.ext.asyncio import AsyncSession
from starlette.responses import Response

from app.db.session import get_db
from app.models.entities import Job, JobStatus
from app.schemas.jobs import JobCreate, JobRead
from app.workers.tasks import process_job

router = APIRouter()


@router.post("/jobs", response_model=JobRead)
async def create_job(payload: JobCreate, db: AsyncSession = Depends(get_db)) -> Job:
    job = Job(url=str(payload.url), source_type=payload.source_type)
    db.add(job)
    await db.commit()
    await db.refresh(job)
    process_job.send(str(job.id))
    return job


@router.get("/jobs", response_model=list[JobRead])
async def list_jobs(db: AsyncSession = Depends(get_db)) -> list[Job]:
    result = await db.execute(select(Job).order_by(desc(Job.created_at)).limit(100))
    return list(result.scalars().all())


@router.get("/jobs/{job_id}", response_model=JobRead)
async def get_job(job_id: UUID, db: AsyncSession = Depends(get_db)) -> Job:
    job = await db.get(Job, job_id)
    if not job:
        raise HTTPException(status_code=404, detail="Job not found")
    return job


@router.post("/retry/{job_id}", response_model=JobRead)
async def retry_job(job_id: UUID, db: AsyncSession = Depends(get_db)) -> Job:
    job = await db.get(Job, job_id)
    if not job:
        raise HTTPException(status_code=404, detail="Job not found")
    job.status = JobStatus.queued.value
    job.last_error = None
    await db.commit()
    await db.refresh(job)
    process_job.send(str(job.id))
    return job


@router.get("/health")
async def health() -> dict:
    return {"status": "ok"}


@router.get("/metrics")
async def metrics() -> Response:
    return Response(generate_latest(), media_type=CONTENT_TYPE_LATEST)
