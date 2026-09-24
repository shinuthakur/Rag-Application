from enum import Enum
from urllib.parse import urlparse


class SourceType(str, Enum):
    PDF = "pdf"
    WEB = "web"
    YOUTUBE = "youtube"


def detect_source_type(source: str) -> SourceType:
    """
    Detect whether a source is a PDF URL, website URL,
    or YouTube URL.
    """

    source = source.strip()

    # --------------------------------------------------
    # YouTube
    # --------------------------------------------------

    parsed = urlparse(source)
    domain = parsed.netloc.lower()

    if (
        "youtube.com" in domain
        or "youtu.be" in domain
    ):
        return SourceType.YOUTUBE

    # --------------------------------------------------
    # PDF URL
    # --------------------------------------------------

    if parsed.path.lower().endswith(".pdf"):
        return SourceType.PDF

    # --------------------------------------------------
    # Default URL source
    # --------------------------------------------------

    if parsed.scheme in {"http", "https"}:
        return SourceType.WEB

    raise ValueError(
        "Unable to determine the source type."
    )