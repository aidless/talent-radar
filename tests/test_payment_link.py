"""Payment-link helper tests: URL validation and deterministic zip rebuild."""
import hashlib
import os
import shutil
import sys
import tempfile
import unittest
import zipfile
from pathlib import Path

sys.path.insert(0, os.path.abspath(os.path.join(os.path.dirname(__file__), "..")))
from tools.set_payment_url import set_payment_url  # noqa: E402

MEMBERS = (
    "index.html", "sell/index.html", "serve.py", "prompts.md", "README.md",
    "launch.md", "research/README.md", "research/recruit.md",
    "research/feedback-form.md", "data/.gitkeep",
)


class TestPaymentLink(unittest.TestCase):
    def setUp(self):
        self.tmp = tempfile.TemporaryDirectory()
        self.root = Path(self.tmp.name)
        src = Path(__file__).resolve().parent.parent
        for name in MEMBERS:
            dst = self.root / name
            dst.parent.mkdir(parents=True, exist_ok=True)
            shutil.copy(src / name, dst)

    def tearDown(self):
        self.tmp.cleanup()

    def test_rejects_non_http_url(self):
        with self.assertRaises(ValueError):
            set_payment_url(self.root, "javascript:alert(1)")
        self.assertIn("[购买链接]", (self.root / "sell/index.html").read_text(encoding="utf-8"))

    def test_replaces_placeholder_and_rebuilds_zip(self):
        result = set_payment_url(self.root, "https://pay.example.com/talent-radar")
        self.assertTrue(result["ok"])
        self.assertGreaterEqual(result["replaced"], 1)
        self.assertNotIn("[购买链接]", (self.root / "sell/index.html").read_text(encoding="utf-8"))
        self.assertIn("https://pay.example.com/talent-radar", (self.root / "README.md").read_text(encoding="utf-8"))
        zp = self.root / "talent-radar-product.zip"
        self.assertTrue(zp.exists())
        with zipfile.ZipFile(zp) as z:
            self.assertEqual(set(z.namelist()), set(MEMBERS))
            for member in MEMBERS:
                src_hash = hashlib.sha256((self.root / member).read_bytes()).hexdigest()
                self.assertEqual(src_hash, hashlib.sha256(z.read(member)).hexdigest(), member)


if __name__ == "__main__":
    unittest.main()
