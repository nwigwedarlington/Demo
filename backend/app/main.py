from contextlib import asynccontextmanager

from fastapi import FastAPI

from app.api.routes import router
from app.core.logging import configure_logging
from app.core.rate_limit import InMemoryRateLimitMiddleware
from app.db.base import Base
from app.db.session import engine
from app.models import entities  # noqa: F401


@asynccontextmanager
async def lifespan(app: FastAPI):
    configure_logging()
    async with engine.begin() as conn:
        await conn.run_sync(Base.metadata.create_all)
    yield


app = FastAPI(title="Facebook Fact-Check Automation Platform", lifespan=lifespan)
app.add_middleware(InMemoryRateLimitMiddleware)
app.include_router(router)
