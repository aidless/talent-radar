"""Portfolio page must link real assets and state honest limits."""
import unittest
from pathlib import Path


ROOT = Path(__file__).resolve().parent.parent


class TestPortfolio(unittest.TestCase):
    def test_portfolio_links_existing_assets(self):
        html = (ROOT / "portfolio" / "index.html").read_text(encoding="utf-8")
        for url in [
            "https://github.com/aidless/talent-radar",
            "https://aidless.github.io/talent-radar/",
            "https://github.com/aidless/talent-radar/releases/tag/v1.0.0",
        ]:
            self.assertIn(url, html)

    def test_portfolio_states_limits(self):
        html = (ROOT / "portfolio" / "index.html").read_text(encoding="utf-8")
        self.assertIn("静态 Demo", html)
        self.assertIn("心理测评认证", html)
        self.assertIn("材料就绪、未招募、无结果", html)


if __name__ == "__main__":
    unittest.main()
