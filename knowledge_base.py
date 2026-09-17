from __future__ import annotations

import json
import math
import re
from collections import Counter
from dataclasses import dataclass
from pathlib import Path

from docx import Document


@dataclass(frozen=True)
class KnowledgeChunk:
    filename: str
    title: str
    category: str
    source: str
    text: str


@dataclass(frozen=True)
class SearchResult:
    filename: str
    title: str
    category: str
    source: str
    text: str
    score: float


def _tokens(text: str) -> list[str]:
    """为中英文资料生成轻量检索词：中文单字、双字词和英文单词。"""
    normalized = re.sub(r"\s+", "", text.lower())
    chinese = re.findall(r"[\u4e00-\u9fff]+", normalized)
    words = re.findall(r"[a-z0-9]+", normalized)
    result: list[str] = list(words)
    for sequence in chinese:
        result.extend(sequence)
        result.extend(sequence[index : index + 2] for index in range(len(sequence) - 1))
    return result


def _read_docx(path: Path) -> list[str]:
    document = Document(path)
    blocks = [paragraph.text.strip() for paragraph in document.paragraphs if paragraph.text.strip()]
    for table in document.tables:
        for row in table.rows:
            cells = [re.sub(r"\s+", " ", cell.text).strip() for cell in row.cells]
            line = " ｜ ".join(cell for cell in cells if cell)
            if line:
                blocks.append(line)
    return blocks


def _split_blocks(blocks: list[str], max_chars: int = 520) -> list[str]:
    chunks: list[str] = []
    current: list[str] = []
    length = 0
    for block in blocks:
        if current and length + len(block) > max_chars:
            chunks.append("\n".join(current))
            current, length = [], 0
        current.append(block)
        length += len(block)
    if current:
        chunks.append("\n".join(current))
    return chunks


class LocalKnowledgeBase:
    """无需联网的 TF-IDF 向量检索器，提供 RAG 的检索阶段。"""

    def __init__(self, root: Path):
        manifest = json.loads((root / "manifest.json").read_text(encoding="utf-8"))
        records = {item["filename"]: item for item in manifest["documents"]}
        chunks: list[KnowledgeChunk] = []
        for path in sorted((root / "documents").glob("*.docx")):
            record = records.get(path.name, {})
            for text in _split_blocks(_read_docx(path)):
                chunks.append(
                    KnowledgeChunk(
                        filename=path.name,
                        title=record.get("title", path.stem),
                        category=record.get("category", "未分类"),
                        source=record.get("source", "来源待核验"),
                        text=text,
                    )
                )
        self.chunks = chunks
        self.document_count = len({chunk.filename for chunk in chunks})
        self._term_counts = [Counter(_tokens(chunk.text)) for chunk in chunks]
        document_frequency: Counter[str] = Counter()
        for counts in self._term_counts:
            document_frequency.update(counts.keys())
        total = max(len(chunks), 1)
        self._idf = {
            token: math.log((total + 1) / (frequency + 1)) + 1
            for token, frequency in document_frequency.items()
        }

    def _vector(self, counts: Counter[str]) -> dict[str, float]:
        total = sum(counts.values()) or 1
        return {
            token: (count / total) * self._idf.get(token, math.log(len(self.chunks) + 1) + 1)
            for token, count in counts.items()
        }

    @staticmethod
    def _cosine(left: dict[str, float], right: dict[str, float]) -> float:
        shared = left.keys() & right.keys()
        numerator = sum(left[token] * right[token] for token in shared)
        left_norm = math.sqrt(sum(value * value for value in left.values()))
        right_norm = math.sqrt(sum(value * value for value in right.values()))
        return numerator / (left_norm * right_norm) if left_norm and right_norm else 0.0

    def search(self, query: str, top_k: int = 5) -> list[SearchResult]:
        query_vector = self._vector(Counter(_tokens(query)))
        scored: list[SearchResult] = []
        for chunk, counts in zip(self.chunks, self._term_counts):
            score = self._cosine(query_vector, self._vector(counts))
            if score > 0:
                scored.append(
                    SearchResult(
                        filename=chunk.filename,
                        title=chunk.title,
                        category=chunk.category,
                        source=chunk.source,
                        text=chunk.text,
                        score=score,
                    )
                )
        scored.sort(key=lambda item: item.score, reverse=True)
        return scored[:top_k]

