from app.loaders.source_detector import (
    SourceType,
    detect_source_type,
)


def test_detect_youtube_url():
    result = detect_source_type(
        "https://www.youtube.com/watch?v=abc123"
    )

    assert result == SourceType.YOUTUBE


def test_detect_youtube_short_url():
    result = detect_source_type(
        "https://youtu.be/abc123"
    )

    assert result == SourceType.YOUTUBE


def test_detect_pdf_url():
    result = detect_source_type(
        "https://example.com/document.pdf"
    )

    assert result == SourceType.PDF


def test_detect_web_url():
    result = detect_source_type(
        "https://example.com/article"
    )

    assert result == SourceType.WEB