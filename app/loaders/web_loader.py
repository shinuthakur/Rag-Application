import uuid
from urllib.parse import urlparse

import requests
from bs4 import BeautifulSoup
from requests import RequestException

from app.loaders.base_loader import BaseLoader
from app.schemas.document import DocumentMetadata, SourceDocument


class WebLoader(BaseLoader):
    """
    Loader for normal web pages.
    """

    def load(self, source: str) -> SourceDocument:
        """
        Download a webpage and extract readable text.
        """

        parsed = urlparse(source)

        if parsed.scheme not in {"http", "https"} or not parsed.netloc:
            raise ValueError(
                "Invalid website URL. URL must start with http:// or https://"
            )

        try:
            response = requests.get(
                source,
                timeout=20,
                headers={
                    "User-Agent": (
                        "Mozilla/5.0 (Windows NT 10.0; Win64; x64) "
                        "AppleWebKit/537.36 "
                        "(KHTML, like Gecko) "
                        "Chrome/131.0 Safari/537.36"
                    )
                },
            )
            response.raise_for_status()

        except RequestException as exc:
            raise RuntimeError(
                f"Failed to load webpage: {source}"
            ) from exc

        soup = BeautifulSoup(
            response.text,
            "html.parser",
        )

        # Remove elements that usually do not contain useful content.
        for element in soup(
            [
                "script",
                "style",
                "noscript",
                "svg",
                "nav",
                "footer",
                "header",
                "form",
                "aside",
            ]
        ):
            element.decompose()

        title = (
            soup.title.get_text(strip=True)
            if soup.title
            else source
        )

        content = soup.get_text(
            separator="\n",
            strip=True,
        )

        if not content:
            raise ValueError(
                "No readable text was found on the webpage."
            )

        # Normalize excessive blank lines.
        lines = [
            line.strip()
            for line in content.splitlines()
            if line.strip()
        ]

        content = "\n".join(lines)

        document_id = str(uuid.uuid4())

        metadata = DocumentMetadata(
            document_id=document_id,
            source_type="web",
            source=source,
            title=title,
        )

        return SourceDocument(
            document_id=document_id,
            content=content,
            metadata=metadata,
        )