"""Unit tests for document domain models."""

from agentsieve.ingestion.documents import Document


def test_document_defaults_metadata_to_empty_dict() -> None:
    document = Document(
        id="doc-1",
        content="FastAPI is a modern web framework.",
        source="https://example.com/docs",
    )

    assert document.id == "doc-1"
    assert document.content == "FastAPI is a modern web framework."
    assert document.source == "https://example.com/docs"
    assert document.metadata == {}


def test_document_accepts_metadata() -> None:
    document = Document(
        id="doc-1",
        content="FastAPI documentation.",
        source="https://example.com/docs",
        metadata={
            "title": "Introduction",
            "section": "First Steps",
        },
    )

    assert document.metadata["title"] == "Introduction"
    assert document.metadata["section"] == "First Steps"
