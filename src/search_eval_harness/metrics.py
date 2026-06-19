from __future__ import annotations

import re
from dataclasses import dataclass
from statistics import mean
from urllib.parse import urlparse


@dataclass(frozen=True)
class EvalScore:
    citation_coverage: float
    source_diversity: float
    snippet_density: float
    freshness_hint_rate: float
    hallucinated_citations: list[int]


def score_answer(answer: str, sources: list[dict]) -> EvalScore:
    source_ids = set(range(1, len(sources) + 1))
    cited_ids = {int(match) for match in re.findall(r"\[(\d+)\]", answer)}
    hallucinated = sorted(cited_ids - source_ids)

    citation_coverage = 1.0
    if cited_ids:
        citation_coverage = (len(cited_ids) - len(hallucinated)) / len(cited_ids)

    domains = {domain_for(source.get("url", "")) for source in sources if source.get("url")}
    source_diversity = len(domains) / len(sources) if sources else 0.0

    snippets = [snippet_text(source) for source in sources]
    snippet_density = mean([len(snippet.split()) for snippet in snippets]) if snippets else 0.0

    freshness_hits = sum(1 for snippet in snippets if has_freshness_hint(snippet))
    freshness_hint_rate = freshness_hits / len(snippets) if snippets else 0.0

    return EvalScore(
        citation_coverage=round(citation_coverage, 3),
        source_diversity=round(source_diversity, 3),
        snippet_density=round(snippet_density, 1),
        freshness_hint_rate=round(freshness_hint_rate, 3),
        hallucinated_citations=hallucinated,
    )


def domain_for(url: str) -> str:
    return urlparse(url).netloc.replace("www.", "")


def snippet_text(source: dict) -> str:
    snippets = source.get("snippets") or source.get("snippet") or []
    if isinstance(snippets, str):
        return snippets
    return " ".join(str(item) for item in snippets)


def has_freshness_hint(text: str) -> bool:
    return bool(re.search(r"\b(20\d{2}|today|yesterday|last week|latest|recent)\b", text, re.IGNORECASE))
