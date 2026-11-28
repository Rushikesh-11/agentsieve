"""Unit tests for document chunking."""

import pytest

from agentsieve.ingestion.chunking import FixedSizeChunker
from agentsieve.ingestion.documents import Document


def test_fixed_size_chunker_splits_document() -> None:
    document = Document(
        id="doc-1",
        content="ABCDEFGHIJ",
        source="test.txt",
    )

    chunks = list(FixedSizeChunker(chunk_size=4).chunk(document))

    assert [chunk.content for chunk in chunks] == [
        "ABCD",
        "EFGH",
        "IJ",
    ]


def test_fixed_size_chunker_preserves_document_metadata() -> None:
    document = Document(
        id="doc-1",
        content="ABCDEFGH",
        source="test.txt",
        metadata={"title": "Test Document"},
    )

    chunks = list(FixedSizeChunker(chunk_size=4).chunk(document))

    assert chunks[0].source == "test.txt"
    assert chunks[0].metadata["title"] == "Test Document"
    assert chunks[0].metadata["chunk_index"] == 0
    assert chunks[1].metadata["chunk_index"] == 1


def test_fixed_size_chunker_supports_overlap() -> None:
    document = Document(
        id="doc-1",
        content="ABCDEFGHIJ",
        source="test.txt",
    )

    chunks = list(
        FixedSizeChunker(
            chunk_size=4,
            chunk_overlap=2,
        ).chunk(document)
    )

    assert [chunk.content for chunk in chunks] == [
        "ABCD",
        "CDEF",
        "EFGH",
        "GHIJ",
        "IJ",
    ]


@pytest.mark.parametrize(
    ("chunk_size", "chunk_overlap"),
    [
        (0, 0),
        (-1, 0),
        (4, -1),
        (4, 4),
        (4, 5),
    ],
)
def test_fixed_size_chunker_rejects_invalid_configuration(
    chunk_size: int,
    chunk_overlap: int,
) -> None:
    with pytest.raises(ValueError):
        FixedSizeChunker(
            chunk_size=chunk_size,
            chunk_overlap=chunk_overlap,
        )
