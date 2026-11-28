"""Unit tests for document loaders."""

from pathlib import Path

from agentsieve.ingestion.loaders import TextFileLoader


def test_text_file_loader_loads_document(tmp_path: Path) -> None:
    file_path = tmp_path / "fastapi.txt"
    file_path.write_text(
        "FastAPI is a modern web framework for building APIs.",
        encoding="utf-8",
    )

    documents = list(TextFileLoader(file_path).load())

    assert len(documents) == 1

    document = documents[0]

    assert document.id == "fastapi"
    assert document.content == ("FastAPI is a modern web framework for building APIs.")
    assert document.source == str(file_path)
    assert document.metadata["file_name"] == "fastapi.txt"
