from app.loaders.base_loader import BaseLoader
from app.loaders.pdf_loader import PDFLoader
from app.loaders.source_detector import SourceType
from app.loaders.web_loader import WebLoader
from app.loaders.youtube_loader import YouTubeLoader


def get_loader(
    source_type: SourceType,
) -> BaseLoader:
    """
    Return the appropriate loader for a source type.
    """

    if source_type == SourceType.PDF:
        return PDFLoader()

    if source_type == SourceType.WEB:
        return WebLoader()

    if source_type == SourceType.YOUTUBE:
        return YouTubeLoader()

    raise ValueError(
        f"Unsupported source type: {source_type}"
    )