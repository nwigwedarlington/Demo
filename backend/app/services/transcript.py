from app.core.config import get_settings
from app.schemas.factcheck import TranscriptResult


class TranscriptService:
    async def extract(self, url: str) -> TranscriptResult:
        settings = get_settings()
        if settings.transcript_free_demo_mode:
            return TranscriptResult(
                transcript=f"Demo transcript for {url}. Configure Whisper or subtitles for real extraction.",
                language="en",
                confidence=0.5,
            )
        return await self._extract_live(url)

    async def _extract_live(self, url: str) -> TranscriptResult:
        # Priority: native subtitles, OCR subtitles, then speech-to-text via Whisper/ffmpeg.
        raise NotImplementedError("Connect ffmpeg, OCR, and Whisper pipeline for production media extraction")
