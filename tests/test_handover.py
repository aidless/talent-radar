"""C 收款闭环测试：RED 阶段，launch.md 与 zip 更新尚未完成。"""
import hashlib
import os
import subprocess
import unittest
import zipfile

ROOT = os.path.abspath(os.path.join(os.path.dirname(__file__), "..", ".."))
TD = os.path.join(ROOT, "talent-radar")


class TestHandover(unittest.TestCase):
    def test_no_placeholder_phrase_in_sell(self):
        with open(os.path.join(TD, "sell", "index.html"), encoding="utf-8") as f:
            self.assertNotIn("[购买链接占位]", f.read())

    def test_readme_marks_placeholder(self):
        with open(os.path.join(TD, "README.md"), encoding="utf-8") as f:
            text = f.read()
        self.assertIn("占位待替换", text)

    def test_launch_exists_with_required_parts(self):
        p = os.path.join(TD, "launch.md")
        self.assertTrue(os.path.exists(p))
        with open(p, encoding="utf-8") as f:
            text = f.read()
        self.assertIn("卖点", text)
        self.assertIn("FAQ", text)
        self.assertIn("结构化自省工具", text)

    def test_zip_integrity(self):
        zp = os.path.join(TD, "talent-radar-product.zip")
        self.assertTrue(os.path.exists(zp))
        self.assertEqual(subprocess.run(["unzip", "-t", zp], capture_output=True).returncode, 0)
        members = [
            "index.html", "sell/index.html", "serve.py", "prompts.md", "README.md",
            "launch.md", "research/README.md", "research/recruit.md",
            "research/feedback-form.md", "data/.gitkeep",
        ]
        with zipfile.ZipFile(zp) as z:
            names = z.namelist()
            for m in members:
                self.assertIn(m, names)
                src = os.path.join(TD, m)
                if os.path.exists(src):
                    with open(src, "rb") as f:
                        self.assertEqual(hashlib.sha256(f.read()).hexdigest(),
                                         hashlib.sha256(z.read(m)).hexdigest(), m)


if __name__ == "__main__":
    unittest.main()
