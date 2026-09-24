from pathlib import Path

from app.loaders.pdf_loader import PDFLoader
from app.loaders.web_loader import WebLoader
from app.loaders.youtube_loader import YouTubeLoader


def print_document(document):
    print("\n" + "=" * 70)
    print("DOCUMENT LOADED")
    print("=" * 70)

    print(f"Document ID : {document.document_id}")
    print(f"Source Type : {document.metadata.source_type}")
    print(f"Source      : {document.metadata.source}")
    print(f"Title       : {document.metadata.title}")

    print("\nContent preview:")
    print("-" * 70)

    print(document.content[:1000])

    print("\nTotal characters:")
    print(len(document.content))


def test_pdf():
    pdf_path = Path(
        "data/uploads/test.pdf"
    )

    loader = PDFLoader()

    document = loader.load(
        str(pdf_path)
    )

    print_document(document)


def test_web():
    url = "https://en.wikipedia.org/wiki/Retrieval-augmented_generation"

    loader = WebLoader()

    document = loader.load(url)

    print_document(document)


def test_youtube():
    url = "https://youtu.be/FsVh7z4c6Io?si=2s8LCPVTYOWY9U9E"

    loader = YouTubeLoader()

    document = loader.load(url)

    print_document(document)


if __name__ == "__main__":

    print("\nRAG LOADER TEST")
    print("==============================")

    print("\n1. Testing PDF...")
    test_pdf()

    print("\n2. Testing Website...")
    test_web()

    print("\n3. Testing YouTube...")
    # Uncomment after putting a real YouTube URL.
    # test_youtube()