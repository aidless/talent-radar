"""A 数据池服务端测试：RED 阶段，summary/validate 尚未实现。"""
import json
import os
import sys
import tempfile
import unittest
from datetime import datetime, timedelta, timezone

sys.path.insert(0, os.path.abspath(os.path.join(os.path.dirname(__file__), "..")))
import serve  # noqa: E402


def sample(pid, days_ago=1, valid=True, demo=False, consent=True):
    return {
        "schema_version": 1,
        "contributor_hash": "h" + pid + "0000000000000000"[:14],
        "created_at": (datetime.now(timezone.utc) - timedelta(days=days_ago)).isoformat(),
        "answers": [{"qid": "q1", "value": 4, "weight": 1.0, "dtype": "beh", "ms_spent": 1200}],
        "scores": {"dims": {"lang": {"score": 70, "behMean": 0.8, "selfMean": 0.6, "vol": 0.2}},
                   "ranked": ["lang"], "top2gap": 5},
        "meta": {"age_band": "25-34", "occupation_band": "tech",
                 "straight_lined": not valid, "interrupted": not valid,
                 "demo": demo, "source": "web"},
        "consent": {"upload": consent, "timestamp": datetime.now(timezone.utc).isoformat(),
                    "version": "1.0"},
    }


class TestDataPool(unittest.TestCase):
    def test_validate_requires_consent(self):
        self.assertFalse(serve.validate_contribution(sample("a", consent=False)))

    def test_validate_accepts_good(self):
        self.assertTrue(serve.validate_contribution(sample("a")))

    def test_dedup_and_summary_threshold(self):
        with tempfile.TemporaryDirectory() as d:
            p = os.path.join(d, "c.jsonl")
            rows = [sample(f"h{i}") for i in range(499)]
            rows.append(sample("h0"))  # duplicate
            with open(p, "w", encoding="utf-8") as f:
                for r in rows:
                    f.write(json.dumps(r, ensure_ascii=False) + "\n")
            s = serve.summary(p)
            self.assertEqual(s["valid_n"], 499)
            self.assertFalse(s["ready"])
            self.assertEqual(s["verdict"], "collecting")
            self.assertEqual(s["window_days"], 30)

    def test_ready_at_500(self):
        with tempfile.TemporaryDirectory() as d:
            p = os.path.join(d, "c.jsonl")
            with open(p, "w", encoding="utf-8") as f:
                for i in range(500):
                    f.write(json.dumps(sample(f"h{i}")) + "\n")
            s = serve.summary(p)
            self.assertEqual(s["valid_n"], 500)
            self.assertTrue(s["ready"])
            self.assertEqual(s["verdict"], "ready")

    def test_cut_at_199(self):
        with tempfile.TemporaryDirectory() as d:
            p = os.path.join(d, "c.jsonl")
            with open(p, "w", encoding="utf-8") as f:
                for i in range(199):
                    f.write(json.dumps(sample(f"h{i}")) + "\n")
            s = serve.summary(p)
            self.assertEqual(s["valid_n"], 199)
            self.assertEqual(s["verdict"], "cut")

    def test_demo_and_bad_flags_invalid(self):
        with tempfile.TemporaryDirectory() as d:
            p = os.path.join(d, "c.jsonl")
            rows = [sample("h1", demo=True), sample("h2", valid=False)]
            with open(p, "w", encoding="utf-8") as f:
                for r in rows:
                    f.write(json.dumps(r) + "\n")
            s = serve.summary(p)
            self.assertEqual(s["valid_n"], 0)
            self.assertEqual(s["invalid_n"], 2)


if __name__ == "__main__":
    unittest.main()
