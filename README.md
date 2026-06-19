# Agent Search Eval Harness

A lightweight evaluation harness for search-grounded AI agents.

I built this for the moment after the demo works, when the next question is: "Can we measure whether this answer was actually grounded?" It runs offline with fixtures or live against You.com Search API results.

## What It Measures

- `citation_coverage`: percent of cited IDs that map to retrieved sources
- `source_diversity`: ratio of unique domains to total sources
- `snippet_density`: average source snippet length
- `freshness_hint_rate`: percent of sources that mention a recent year or date
- `hallucinated_citations`: citations in an answer that do not exist in retrieved sources

## Quickstart

```bash
python -m venv .venv
source .venv/bin/activate
python -m pip install -e .
```

Run the fixture-backed eval:

```bash
search-eval datasets/eval_queries.jsonl --fixture examples/sample_search_response.json
```

Run with live You.com Search API results:

```bash
export YDC_API_KEY="your-api-key"
search-eval datasets/eval_queries.jsonl --live
```

## Why This Helps

Good AI examples need a feedback loop. This repo keeps the loop small: retrieve sources, draft an answer, score the citations, and make the weak spots visible enough for a developer to fix.

## Example Output

```text
query                                 coverage  diversity  density  hallucinated
What does You.com provide for dev...  1.00      0.33       15.3     []
How can an MCP server help AI ass...  1.00      0.33       15.3     []
```

## License

MIT
