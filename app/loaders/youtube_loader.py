import re
import uuid

from youtube_transcript_api import YouTubeTranscriptApi

from app.loaders.base_loader import BaseLoader
from app.schemas.document import DocumentMetadata, SourceDocument


class YouTubeLoader(BaseLoader):
    """
    Loader for YouTube videos using their transcripts.
    """

    def load(self, source: str) -> SourceDocument:
        """
        Extract transcript text from a YouTube video.
        """

        video_id = self._extract_video_id(source)

        if not video_id:
            raise ValueError(
                "Could not extract a valid YouTube video ID."
            )

        try:
            api = YouTubeTranscriptApi()

            transcript = api.fetch(
                video_id,
                languages=["en"],
            )

        except Exception as exc:
            raise RuntimeError(
                f"Failed to fetch YouTube transcript: {source}"
            ) from exc

        if not transcript:
            raise ValueError(
                "No transcript was found for this video."
            )

        content_parts = []

        for item in transcript:
            text = item.text.strip()

            if text:
                content_parts.append(text)

        content = " ".join(content_parts)

        if not content:
            raise ValueError(
                "YouTube transcript contained no readable text."
            )

        document_id = str(uuid.uuid4())

        metadata = DocumentMetadata(
            document_id=document_id,
            source_type="youtube",
            source=source,
            title=f"YouTube Video {video_id}",
            extra={
                "video_id": video_id,
                "language": transcript.language,
                "language_code": transcript.language_code,
                "is_generated": transcript.is_generated,
            },
        )

        return SourceDocument(
            document_id=document_id,
            content=content,
            metadata=metadata,
        )

    @staticmethod
    def _extract_video_id(url: str) -> str | None:
        """
        Extract a YouTube video ID from common YouTube URL formats.
        """

        patterns = [
            r"(?:youtube\.com/watch\?v=)([^&]+)",
            r"(?:youtu\.be/)([^?&]+)",
            r"(?:youtube\.com/shorts/)([^?&]+)",
        ]

        for pattern in patterns:
            match = re.search(pattern, url)

            if match:
                return match.group(1)

        return None