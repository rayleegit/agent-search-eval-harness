from __future__ import annotations

import argparse
import json

from .runner import load_fixture, load_queries, run_eval


def main(argv: list[str] | None = None) -> int:
    parser = argparse.ArgumentParser(description="Evaluate search-grounded answers.")
    parser.add_argument("queries", help="JSONL file with query records.")
    parser.add_argument("--fixture", help="Use the same You.com-style fixture for every query.")
    parser.add_argument("--live", action="store_true", help="Fetch live You.com Search API results.")
    parser.add_argument("--json", action="store_true", help="Print machine-readable JSON.")
    args = parser.parse_args(argv)

    queries = load_queries(args.queries)
    fixture_sources = load_fixture(args.fixture) if args.fixture else None
    rows = run_eval(queries, fixture_sources=fixture_sources, live=args.live)

    if args.json:
        print(json.dumps(rows, indent=2))
        return 0

    print(f"{'query':40} coverage  diversity  density  hallucinated")
    for row in rows:
        query = row["query"][:37] + "..." if len(row["query"]) > 40 else row["query"]
        print(
            f"{query:40} {row['citation_coverage']:<8.2f} "
            f"{row['source_diversity']:<9.2f} {row['snippet_density']:<7.1f} "
            f"{row['hallucinated_citations']}"
        )
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
