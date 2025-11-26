from __future__ import annotations

import math
from dataclasses import dataclass
from pathlib import Path
from typing import List, Sequence

import ollama

from app.core.config import get_settings
from app.services.llm import LLMService

RAG_SYSTEM_PROMPT = (
    "You are a helpful assistant that only answers using the provided context. "
    "If the context is insufficient, reply that you do not know. "
    "Cite information conversationally and keep answers concise."
)


@dataclass
class DocumentChunk:
    content: str
    source: str


class RAGService:
    def __init__(self) -> None:
        self.settings = get_settings()
        self.llm = LLMService()
        self.documents_dir = Path(self.settings.rag_documents_dir)
        self.embedding_model = self.settings.rag_embedding_model
        self.top_k = self.settings.rag_top_k
        self.min_score = self.settings.rag_min_score
        self.chunks, self.embeddings = self._build_index()

    def answer(self, query: str) -> tuple[str, List[dict]]:
        question = (query or "").strip()
        if not question:
            return "Please provide a question for the assistant to look up.", []

        if not self.chunks or not self.embeddings:
            return (
                "The knowledge base is empty. Add markdown or text files to the "
                f"'{self.documents_dir}' directory and retry.",
                [],
            )

        query_embedding = self._embed_text(question)
        if not query_embedding:
            return (
                "I could not embed the question with the configured embedding model.",
                [],
            )

        ranked_chunks = self._rank_chunks(query_embedding)
        if not ranked_chunks:
            return (
                "I could not find relevant information in the knowledge base for that question.",
                [],
            )

        context = self._build_context(ranked_chunks)
        prompt = (
            f"{RAG_SYSTEM_PROMPT}\n\n"
            f"Context:\n{context}\n\n"
            f"Question: {question}\nAnswer:"
        )
        answer = self.llm.generate(prompt)

        sources = [
            {"source": chunk.source, "preview": chunk.content[:280]}
            for chunk in ranked_chunks
        ]
        final_answer = answer or "I could not compose an answer from the retrieved context."
        return final_answer, sources

    def _build_index(self) -> tuple[List[DocumentChunk], List[Sequence[float]]]:
        chunks: List[DocumentChunk] = []
        for idx, path in enumerate(self._iter_document_paths()):
            text = self._read_text(path)
            for chunk_id, chunk in enumerate(self._chunk_text(text), start=1):
                formatted = chunk.strip()
                if not formatted:
                    continue
                chunks.append(
                    DocumentChunk(
                        content=formatted,
                        source=self._format_source(path, chunk_id),
                    )
                )

        embeddings = self._embed_documents(chunks)
        return chunks, embeddings

    def _iter_document_paths(self) -> List[Path]:
        paths: List[Path] = []
        if self.documents_dir.exists():
            for ext in ("*.md", "*.txt"):
                paths.extend(sorted(self.documents_dir.rglob(ext)))

        if not paths:
            fallback = Path("README.md")
            if fallback.exists():
                paths.append(fallback)
        return paths

    def _read_text(self, path: Path) -> str:
        try:
            return path.read_text(encoding="utf-8")
        except UnicodeDecodeError:
            return path.read_text(encoding="utf-8", errors="ignore")

    def _chunk_text(self, text: str, max_chars: int = 1200) -> List[str]:
        paragraphs = [p.strip() for p in text.split("\n\n") if p.strip()]
        chunks: List[str] = []
        current: List[str] = []
        size = 0
        for paragraph in paragraphs:
            paragraph_size = len(paragraph)
            if size + paragraph_size >= max_chars and current:
                chunks.append("\n\n".join(current))
                current = [paragraph]
                size = paragraph_size
                continue
            current.append(paragraph)
            size += paragraph_size
        if current:
            chunks.append("\n\n".join(current))
        return chunks or [text]

    def _format_source(self, path: Path, chunk_id: int) -> str:
        try:
            relative = path.relative_to(Path.cwd())
        except ValueError:
            relative = path
        return f"{relative.as_posix()}#chunk-{chunk_id}"

    def _embed_documents(self, chunks: Sequence[DocumentChunk]) -> List[Sequence[float]]:
        embeddings: List[Sequence[float]] = []
        for chunk in chunks:
            embeddings.append(self._embed_text(chunk.content))
        return embeddings

    def _embed_text(self, text: str) -> Sequence[float]:
        if not text:
            return []
        response = ollama.embeddings(model=self.embedding_model, prompt=text)
        return response.get("embedding", [])

    def _rank_chunks(self, query_embedding: Sequence[float]) -> List[DocumentChunk]:
        scored = []
        for chunk, embedding in zip(self.chunks, self.embeddings):
            score = self._cosine_similarity(query_embedding, embedding)
            if score >= self.min_score:
                scored.append((score, chunk))
        scored.sort(key=lambda item: item[0], reverse=True)
        return [chunk for _, chunk in scored[: self.top_k]]

    def _build_context(self, chunks: Sequence[DocumentChunk]) -> str:
        parts = []
        for chunk in chunks:
            parts.append(f"Source: {chunk.source}\n{chunk.content}")
        return "\n\n".join(parts)

    def _cosine_similarity(
        self, a: Sequence[float], b: Sequence[float]
    ) -> float:
        if not a or not b or len(a) != len(b):
            return 0.0
        dot = sum(x * y for x, y in zip(a, b))
        norm_a = math.sqrt(sum(x * x for x in a))
        norm_b = math.sqrt(sum(y * y for y in b))
        if not norm_a or not norm_b:
            return 0.0
        return dot / (norm_a * norm_b)

