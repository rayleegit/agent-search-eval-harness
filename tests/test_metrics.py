import unittest

from search_eval_harness.metrics import score_answer


class MetricsTests(unittest.TestCase):
    def test_detects_hallucinated_citations(self):
        score = score_answer("Claim [1] and unsupported [3].", [
            {"url": "https://example.com", "snippets": ["Recent source from 2026."]},
            {"url": "https://docs.you.com", "snippets": ["Another source."]},
        ])

        self.assertEqual(score.hallucinated_citations, [3])
        self.assertEqual(score.citation_coverage, 0.5)

    def test_scores_source_diversity(self):
        score = score_answer("Claim [1].", [
            {"url": "https://example.com/a", "snippets": ["One."]},
            {"url": "https://www.example.com/b", "snippets": ["Two."]},
        ])

        self.assertEqual(score.source_diversity, 0.5)

    def test_counts_freshness_hints(self):
        score = score_answer("Claim [1].", [
            {"url": "https://example.com/a", "snippets": ["Latest update in 2026."]},
            {"url": "https://docs.you.com/b", "snippets": ["Stable reference."]},
        ])

        self.assertEqual(score.freshness_hint_rate, 0.5)


if __name__ == "__main__":
    unittest.main()
