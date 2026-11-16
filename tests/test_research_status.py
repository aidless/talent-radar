"""Research status must stay honest until real data exists."""
import unittest
from pathlib import Path


ROOT = Path(__file__).resolve().parent.parent


class TestResearchStatus(unittest.TestCase):
    def test_status_is_honest(self):
        text = (ROOT / "research" / "STATUS.md").read_text(encoding="utf-8")
        self.assertIn("材料就绪、未招募、无结果", text)
        self.assertIn("20–30", text)
        self.assertIn("30 天", text)
        self.assertIn("观察不足，未做结论", text)

    def test_status_has_no_fake_results(self):
        text = (ROOT / "research" / "STATUS.md").read_text(encoding="utf-8")
        self.assertNotIn("retest_corr=", text)
        self.assertIn("不写「信度高」「效度好」", text)


if __name__ == "__main__":
    unittest.main()
