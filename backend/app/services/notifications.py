from datetime import UTC, datetime

import httpx

from app.core.config import get_settings


class NotificationService:
    async def telegram_failure(
        self, service_name: str, url: str, error: str, stack_trace_summary: str
    ) -> None:
        settings = get_settings()
        message = (
            "🚨 WORKFLOW FAILURE\n"
            f"Service: {service_name}\n"
            f"URL: {url}\n"
            f"Error: {error}\n"
            f"Timestamp: {datetime.now(UTC).isoformat()}\n"
            f"Trace: {stack_trace_summary[:800]}"
        )
        if not settings.telegram_bot_token or not settings.telegram_chat_id:
            return
        endpoint = f"https://api.telegram.org/bot{settings.telegram_bot_token}/sendMessage"
        async with httpx.AsyncClient(timeout=10) as client:
            await client.post(endpoint, json={"chat_id": settings.telegram_chat_id, "text": message})
