"""Document loading interfaces and implementations."""

from collections.abc import Iterable
from pathlib import Path
from typing import Protocol

from agentsieve.ingestion.documents import Document


class DocumentLoader(Protocol):
    """Protocol implemented by document loaders."""

    def load(self) -> Iterable[Document]:
        """Load documents from a source."""
        ...


class TextFileLoader:
    """Load a plain-text file as a single AgentSieve document."""

    def __init__(self, path: str | Path) -> None:
        self.path = Path(path)

    def load(self) -> Iterable[Document]:
        """Load the configured text file."""
        content = self.path.read_text(encoding="utf-8")

        yield Document(
            id=self.path.stem,
            content=content,
            source=str(self.path),
            metadata={
                "file_name": self.path.name,
            },
        )
