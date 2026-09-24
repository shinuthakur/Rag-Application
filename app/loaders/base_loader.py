from abc import ABC, abstractmethod

from app.schemas.document import SourceDocument


class BaseLoader(ABC):
    """
    Base interface for all source loaders.
    """

    @abstractmethod
    def load(self, source: str) -> SourceDocument:
        """
        Load and convert a source into a SourceDocument.
        """
        raise NotImplementedError