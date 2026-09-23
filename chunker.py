"""
Stage 2 of the pipeline: splitting documents into chunks.

⚠️ THIS IS THE FILE YOU CHANGE IN MILESTONE 3.

`split_documents` below is deliberately plain. It cuts every document into
fixed-size pieces with a fixed overlap and pays no attention to where sentences
or paragraphs end. It works, and it is not good.

On a corpus of short posts it may not cut anything at all: `campus_life` comes
out as 88 documents and 88 chunks, because almost nothing in it reaches 800
characters. That is the baseline, not a bug — Milestone 3 is where you decide
whether one post should stay one chunk.

Your job in Milestone 3 is to replace the *body* of `split_documents` with a
strategy that fits the documents you actually read in Milestone 1. Keep the
name and the shape of what it returns — the rest of the pipeline calls it, and
your README has to name the function that produced your chunks.

If you get stuck for 30 minutes, `fallback_split` is the original. Switch back
to it, write down what you saw, and move on. That's a real observation about
your pipeline, not giving up.
"""

from dataclasses import dataclass

import config
from ingest import Document


@dataclass
class Chunk:
    """One piece of one document."""

    text: str
    source: str        # which file it came from
    index: int         # which chunk within that file, starting at 0
    produced_by: str   # the function that made it — cite this in your README

    @property
    def label(self) -> str:
        return f"{self.source}#{self.index}"


def fallback_split(
    documents: list[Document],
    chunk_size: int | None = None,
    overlap: int | None = None,
) -> list[Chunk]:
    """
    The starter's original chunker. Fixed-size character windows with overlap.

    Keep this function. Milestone 3's stop rule points back at it, and having
    something to compare your own strategy against is useful in unit 2.
    """
    chunk_size = chunk_size or config.CHUNK_SIZE
    overlap = overlap or config.CHUNK_OVERLAP

    if overlap >= chunk_size:
        raise ValueError("overlap has to be smaller than chunk_size")

    chunks: list[Chunk] = []
    for doc in documents:
        start = 0
        index = 0
        while start < len(doc.text):
            piece = doc.text[start : start + chunk_size].strip()
            if piece:
                chunks.append(
                    Chunk(
                        text=piece,
                        source=doc.source,
                        index=index,
                        produced_by="chunker.py::fallback_split",
                    )
                )
                index += 1
            start += chunk_size - overlap

    return chunks


_DEPENDENT_OPENERS = (
    "it ", "it's", "its ", "this ", "that ", "these ", "those ",
    "also ", "however ", "so ", "but ",
)


def _split_into_paragraphs(text: str) -> list[str]:
    """Paragraphs are blocks separated by a blank line."""
    return [p.strip() for p in text.split("\n\n") if p.strip()]


def _depends_on_previous(paragraph: str) -> bool:
    """Rough check: does this paragraph read like a continuation rather than
    a standalone thought? A pronoun or connector opener with nothing inside
    this chunk to point back to loses the reader.
    """
    return paragraph.lower().startswith(_DEPENDENT_OPENERS)


def _group_paragraphs(title: str, paragraphs: list[str], target: int) -> list[str]:
    """Group paragraphs into ~target-character chunks, title repeated in
    each. Never splits inside a paragraph. A paragraph that depends on the
    one before it stays with it even past target.
    """
    chunks: list[str] = []
    current: list[str] = []
    current_len = len(title)

    for paragraph in paragraphs:
        added_len = len(paragraph) + 2  # + the blank line joining it
        must_merge = current and _depends_on_previous(paragraph)

        if current and current_len + added_len > target and not must_merge:
            chunks.append(title + "\n\n" + "\n\n".join(current))
            current = [paragraph]
            current_len = len(title) + added_len
        else:
            current.append(paragraph)
            current_len += added_len

    if current:
        chunks.append(title + "\n\n" + "\n\n".join(current))

    return chunks


def split_documents(documents: list[Document]) -> list[Chunk]:
    """
    Paragraph-aware chunker for the campus_life corpus. See README.md's
    "Chunking Strategy" for the reasoning: posts that fit within
    config.CHUNK_SIZE stay whole; longer posts split on paragraph
    boundaries, with the title repeated in every piece so the building,
    course, or service being discussed stays identifiable.
    """
    target = config.CHUNK_SIZE
    chunks: list[Chunk] = []

    for doc in documents:
        paragraphs = _split_into_paragraphs(doc.text)
        if not paragraphs:
            continue

        title, body = paragraphs[0], paragraphs[1:]

        if len(doc.text) <= target or not body:
            pieces = [doc.text]
        else:
            pieces = _group_paragraphs(title, body, target)

        for index, piece in enumerate(pieces):
            chunks.append(
                Chunk(
                    text=piece,
                    source=doc.source,
                    index=index,
                    produced_by="chunker.py::split_documents",
                )
            )

    return chunks


def describe(chunks: list[Chunk]) -> str:
    """A one-line summary, printed after indexing."""
    if not chunks:
        return "0 chunks"
    lengths = [len(c.text) for c in chunks]
    return (
        f"{len(chunks)} chunks, "
        f"{sum(lengths) // len(lengths)} characters on average "
        f"(shortest {min(lengths)}, longest {max(lengths)}), "
        f"produced by {chunks[0].produced_by}"
    )


if __name__ == "__main__":
    from ingest import load_documents

    chunks = split_documents(load_documents())
    print(describe(chunks))
