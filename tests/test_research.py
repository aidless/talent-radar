"""B 真人验证测试：RED 阶段，research/analyze.py 尚未实现。"""
import csv
import os
import sys
import tempfile
import unittest

sys.path.insert(0, os.path.abspath(os.path.join(os.path.dirname(__file__), "..", "research")))
import analyze  # noqa: E402

FIELDS = ["pid", "day", "self_rating", "behavior_tag", "third_party_agreement", "drop_reason", "open_text"]


def row(pid, day, self_rating, agreement="", drop="", open_text=""):
    return {"pid": pid, "day": day, "self_rating": self_rating,
            "behavior_tag": "positive", "third_party_agreement": agreement,
            "drop_reason": drop, "open_text": open_text}


def write_csv(path, rows):
    with open(path, "w", newline="", encoding="utf-8") as f:
        w = csv.DictWriter(f, fieldnames=FIELDS)
        w.writeheader()
        w.writerows(rows)


class TestResearch(unittest.TestCase):
    def test_n19_insufficient(self):
        with tempfile.TemporaryDirectory() as d:
            p = os.path.join(d, "f.csv")
            rows = [row(f"p{i}", 0, 3) for i in range(19)]
            write_csv(p, rows)
            out = analyze.analyze(p)
            self.assertEqual(out["confidence"], "insufficient")

    def test_n20_retention_provisional(self):
        with tempfile.TemporaryDirectory() as d:
            p = os.path.join(d, "f.csv")
            rows = []
            for i in range(20):
                rows.append(row(f"p{i}", 0, 2 + (i % 4)))
                if i < 12:  # 60% retention at day30
                    rows.append(row(f"p{i}", 30, 2 + (i % 4)))
            write_csv(p, rows)
            out = analyze.analyze(p)
            self.assertEqual(out["n"], 20)
            self.assertEqual(out["confidence"], "provisional")
            self.assertAlmostEqual(out["drop_rate"], 0.4, places=2)

    def test_open_text_never_in_output(self):
        with tempfile.TemporaryDirectory() as d:
            p = os.path.join(d, "f.csv")
            write_csv(p, [row("p1", 0, 3, open_text="SECRET PRIVATE TEXT")])
            out = analyze.analyze(p)
            self.assertNotIn("SECRET", repr(out))

    def test_gap_recomputed(self):
        with tempfile.TemporaryDirectory() as d:
            p = os.path.join(d, "f.csv")
            rows = [
                row("p1", 0, 5, agreement="1"), row("p1", 30, 3, agreement="1"),
                row("p2", 0, 2, agreement="0"), row("p2", 30, 4, agreement="0"),
            ]
            write_csv(p, rows)
            out = analyze.analyze(p)
            # self_rating 均值 across all rows = 3.5; gap 按 day0/day30 同 pid 差的重算另列
            self.assertAlmostEqual(out["self_beh_gap_mean"], 0.0, places=2)
            self.assertIn("gap_abs_p90", out)
            self.assertIn("third_party_agreement", out)

    def test_missing_day30_excluded_from_retest(self):
        with tempfile.TemporaryDirectory() as d:
            p = os.path.join(d, "f.csv")
            rows = [row("p1", 0, 5), row("p2", 0, 2), row("p1", 30, 4)]
            write_csv(p, rows)
            out = analyze.analyze(p)
            self.assertEqual(out["n"], 2)
            self.assertIsNone(out["retest_corr"])  # 仅 1 个配对，无法算相关


if __name__ == "__main__":
    unittest.main()
