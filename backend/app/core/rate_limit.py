import time
from collections import defaultdict, deque
from collections.abc import Callable

from fastapi import Request, Response
from starlette.middleware.base import BaseHTTPMiddleware

from app.core.config import get_settings


class InMemoryRateLimitMiddleware(BaseHTTPMiddleware):
    def __init__(self, app):
        super().__init__(app)
        self.hits: dict[str, deque[float]] = defaultdict(deque)

    async def dispatch(self, request: Request, call_next: Callable) -> Response:
        limit = get_settings().rate_limit_per_minute
        key = request.client.host if request.client else "unknown"
        now = time.time()
        window = self.hits[key]
        while window and now - window[0] > 60:
            window.popleft()
        if len(window) >= limit:
            return Response("Rate limit exceeded", status_code=429)
        window.append(now)
        return await call_next(request)
