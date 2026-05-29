from datetime import datetime
from uuid import UUID

from pydantic import BaseModel, HttpUrl


class JobCreate(BaseModel):
    url: HttpUrl
    source_type: str = "video"


class JobRead(BaseModel):
    id: UUID
    url: str
    source_type: str
    status: str
    attempts: int
    last_error: str | None = None
    created_at: datetime

    model_config = {"from_attributes": True}
