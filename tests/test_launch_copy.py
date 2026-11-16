"""Launch copy guardrails: channels and honest positioning."""
import os
import unittest
from pathlib import Path


ROOT = Path(__file__).resolve().parent.parent


class TestLaunchCopy(unittest.TestCase):
    def test_launch_has_three_channels(self):
        text = (ROOT / "launch.md").read_text(encoding="utf-8")
        for heading in ["小红书", "V2EX", "即刻"]:
            self.assertIn(heading, text)
        self.assertIn("发布前检查", text)

    def test_launch_has_no_overclaims_in_copy_blocks(self):
        text = (ROOT / "launch.md").read_text(encoding="utf-8")
        copy_start = text.index("## 发布模板")
        copy_end = text.index("## 发布前检查")
        copy_text = text[copy_start:copy_end]
        for banned in ["科学测评认证", "心理诊断"]:
            self.assertNotIn(banned, copy_text)
        self.assertIn("分数没有信度效度认证", copy_text)


if __name__ == "__main__":
    unittest.main()
