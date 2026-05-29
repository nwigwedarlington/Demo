import uuid
from datetime import datetime
from enum import Enum

from sqlalchemy import DateTime, Float, ForeignKey, Integer, JSON, String, Text, func
from sqlalchemy.orm import Mapped, mapped_column, relationship

from app.db.base import Base


class JobStatus(str, Enum):
    queued = "queued"
    processing = "processing"
    completed = "completed"
    failed = "failed"


class TimestampMixin:
    created_at: Mapped[datetime] = mapped_column(DateTime(timezone=True), server_default=func.now())
    updated_at: Mapped[datetime] = mapped_column(
        DateTime(timezone=True), server_default=func.now(), onupdate=func.now()
    )


class Job(Base, TimestampMixin):
    __tablename__ = "jobs"

    id: Mapped[uuid.UUID] = mapped_column(primary_key=True, default=uuid.uuid4)
    url: Mapped[str] = mapped_column(Text)
    source_type: Mapped[str] = mapped_column(String(40))
    status: Mapped[str] = mapped_column(String(30), default=JobStatus.queued.value)
    attempts: Mapped[int] = mapped_column(Integer, default=0)
    last_error: Mapped[str | None] = mapped_column(Text)

    scraped_posts: Mapped[list["ScrapedPost"]] = relationship(back_populates="job")
    transcript: Mapped["Transcript | None"] = relationship(back_populates="job")
    fact_check: Mapped["FactCheck | None"] = relationship(back_populates="job")


class ScrapedPost(Base, TimestampMixin):
    __tablename__ = "scraped_posts"

    id: Mapped[uuid.UUID] = mapped_column(primary_key=True, default=uuid.uuid4)
    job_id: Mapped[uuid.UUID] = mapped_column(ForeignKey("jobs.id"))
    url: Mapped[str] = mapped_column(Text)
    metadata: Mapped[dict] = mapped_column(JSON, default=dict)

    job: Mapped[Job] = relationship(back_populates="scraped_posts")
    comments: Mapped[list["Comment"]] = relationship(back_populates="post")


class Comment(Base, TimestampMixin):
    __tablename__ = "comments"

    id: Mapped[uuid.UUID] = mapped_column(primary_key=True, default=uuid.uuid4)
    post_id: Mapped[uuid.UUID] = mapped_column(ForeignKey("scraped_posts.id"))
    author: Mapped[str] = mapped_column(String(255), default="")
    comment: Mapped[str] = mapped_column(Text, default="")
    likes: Mapped[int] = mapped_column(Integer, default=0)
    reply_count: Mapped[int] = mapped_column(Integer, default=0)
    timestamp: Mapped[str] = mapped_column(String(80), default="")

    post: Mapped[ScrapedPost] = relationship(back_populates="comments")


class Transcript(Base, TimestampMixin):
    __tablename__ = "transcripts"

    id: Mapped[uuid.UUID] = mapped_column(primary_key=True, default=uuid.uuid4)
    job_id: Mapped[uuid.UUID] = mapped_column(ForeignKey("jobs.id"), unique=True)
    transcript: Mapped[str] = mapped_column(Text, default="")
    language: Mapped[str] = mapped_column(String(20), default="unknown")
    confidence: Mapped[float] = mapped_column(Float, default=0.0)

    job: Mapped[Job] = relationship(back_populates="transcript")


class FactCheck(Base, TimestampMixin):
    __tablename__ = "fact_checks"

    id: Mapped[uuid.UUID] = mapped_column(primary_key=True, default=uuid.uuid4)
    job_id: Mapped[uuid.UUID] = mapped_column(ForeignKey("jobs.id"), unique=True)
    provider: Mapped[str] = mapped_column(String(80))
    result: Mapped[dict] = mapped_column(JSON, default=dict)

    job: Mapped[Job] = relationship(back_populates="fact_check")


class PublishQueue(Base, TimestampMixin):
    __tablename__ = "publish_queue"

    id: Mapped[uuid.UUID] = mapped_column(primary_key=True, default=uuid.uuid4)
    job_id: Mapped[uuid.UUID] = mapped_column(ForeignKey("jobs.id"))
    channel: Mapped[str] = mapped_column(String(80))
    payload: Mapped[dict] = mapped_column(JSON, default=dict)
    status: Mapped[str] = mapped_column(String(30), default="queued")


class Failure(Base, TimestampMixin):
    __tablename__ = "failures"

    id: Mapped[uuid.UUID] = mapped_column(primary_key=True, default=uuid.uuid4)
    job_id: Mapped[uuid.UUID | None] = mapped_column(ForeignKey("jobs.id"), nullable=True)
    service_name: Mapped[str] = mapped_column(String(120))
    error_message: Mapped[str] = mapped_column(Text)
    stack_trace_summary: Mapped[str] = mapped_column(Text, default="")


class Notification(Base, TimestampMixin):
    __tablename__ = "notifications"

    id: Mapped[uuid.UUID] = mapped_column(primary_key=True, default=uuid.uuid4)
    service_name: Mapped[str] = mapped_column(String(120))
    target: Mapped[str] = mapped_column(String(120))
    payload: Mapped[dict] = mapped_column(JSON, default=dict)
    status: Mapped[str] = mapped_column(String(30), default="queued")
