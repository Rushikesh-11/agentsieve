"""Document chunking interfaces and implementations."""

from collections.abc import Iterable
from typing import Protocol

from agentsieve.ingestion.documents import Document


class DocumentChunker(Protocol):
    """Protocol implemented by document chunkers."""

    def chunk(self, document: Document) -> Iterable[Document]:
        """Split a document into smaller documents."""
        ...


class FixedSizeChunker:
    """Split documents into fixed-size character chunks."""

    def __init__(self, chunk_size: int, chunk_overlap: int = 0) -> None:
        if chunk_size <= 0:
            raise ValueError("chunk_size must be greater than zero.")

        if chunk_overlap < 0:
            raise ValueError("chunk_overlap cannot be negative.")

        if chunk_overlap >= chunk_size:
            raise ValueError("chunk_overlap must be smaller than chunk_size.")

        self.chunk_size = chunk_size
        self.chunk_overlap = chunk_overlap

    def chunk(self, document: Document) -> Iterable[Document]:
        """Split a document into fixed-size character chunks."""
        step = self.chunk_size - self.chunk_overlap

        for index, start in enumerate(range(0, len(document.content), step)):
            content = document.content[start : start + self.chunk_size]

            yield Document(
                id=f"{document.id}-chunk-{index}",
                content=content,
                source=document.source,
                metadata={
                    **document.metadata,
                    "chunk_index": index,
                },
            )
