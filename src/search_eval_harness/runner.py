from __future__ import annotations

import json
import os
import urllib.parse
import urllib.request
from dataclasses import asdict
from typing import Iterable

from .metrics import score_answer


SEARCH_ENDPOINT = "https://ydc-index.io/v1/search"


def load_queries(path: str) -> list[dict]:
    queries = []
    with open(path, "r", encoding="utf-8") as handle:
        for line in handle:
            line = line.strip()
            if line:
                queries.append(json.loads(line))
    return queries


def load_fixture(path: str) -> list[dict]:
    with open(path, "r", encoding="utf-8") as handle:
        payload = json.load(handle)
    return payload.get("results", {}).get("web", payload.get("web", []))


def fetch_live_results(query: str, count: int = 5) -> list[dict]:
    api_key = os.environ.get("YDC_API_KEY")
    if not api_key:
        raise RuntimeError("Set YDC_API_KEY to run live evaluations.")

    params = urllib.parse.urlencode({"query": query, "count": count})
    request = urllib.request.Request(
        f"{SEARCH_ENDPOINT}?{params}",
        headers={"X-API-Key": api_key, "Accept": "application/json"},
    )
    with urllib.request.urlopen(request, timeout=20) as response:
        payload = json.loads(response.read().decode("utf-8"))
    return payload.get("results", {}).get("web", [])


def source_backed_answer(query: str, sources: list[dict]) -> str:
    if not sources:
        return f"No sources found for {query}."
    pieces = []
    for index, source in enumerate(sources[:3], start=1):
        snippet = source.get("snippets", [""])[0] if isinstance(source.get("snippets"), list) else source.get("snippet", "")
        pieces.append(f"{snippet} [{index}]")
    return " ".join(piece for piece in pieces if piece.strip())


def run_eval(queries: Iterable[dict], fixture_sources: list[dict] | None = None, live: bool = False) -> list[dict]:
    rows = []
    for item in queries:
        query = item["query"]
        sources = fetch_live_results(query) if live else list(fixture_sources or item.get("sources", []))
        answer = item.get("answer") or source_backed_answer(query, sources)
        score = score_answer(answer, sources)
        rows.append({"query": query, "answer": answer, **asdict(score)})
    return rows
