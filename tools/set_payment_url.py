#!/usr/bin/env python3
"""Set the real payment URL, rebuild the fixed product zip, and verify it."""
from __future__ import annotations

import hashlib
import io
import sys
import zipfile
from pathlib import Path
from urllib.parse import urlparse

PLACEHOLDER = "[购买链接]"
ZIP_MEMBERS = (
    "index.html", "sell/index.html", "serve.py", "prompts.md", "README.md",
    "launch.md", "research/README.md", "research/recruit.md",
    "research/feedback-form.md", "data/.gitkeep",
)


def set_payment_url(repo_root: Path, payment_url: str) -> dict:
    root = Path(repo_root)
    parsed = urlparse(payment_url.strip())
    if parsed.scheme not in {"http", "https"} or not parsed.netloc:
        raise ValueError("payment URL must be an absolute http(s) URL")

    sell = root / "sell" / "index.html"
    text = sell.read_text(encoding="utf-8")
    count = text.count(PLACEHOLDER)
    if count == 0:
        raise ValueError("no [购买链接] placeholder left in sell/index.html")
    sell.write_text(text.replace(PLACEHOLDER, payment_url), encoding="utf-8")

    readme = root / "README.md"
    readme_text = readme.read_text(encoding="utf-8")
    status_line = "- `sell/`：销售页（含前 5 题试玩；"
    lines = readme_text.splitlines()
    for i, line in enumerate(lines):
        if line.startswith(status_line):
            lines[i] = f"- `sell/`：销售页（含前 5 题试玩；真实收款链接已配置：{payment_url}）"
            break
    readme.write_text("\n".join(lines) + "\n", encoding="utf-8")

    buf = io.BytesIO()
    with zipfile.ZipFile(buf, "w", zipfile.ZIP_DEFLATED) as z:
        for member in ZIP_MEMBERS:
            path = root / member
            if not path.exists():
                raise FileNotFoundError(member)
            z.write(path, member)
    payload = buf.getvalue()
    (root / "talent-radar-product.zip").write_bytes(payload)

    with zipfile.ZipFile(io.BytesIO(payload)) as z:
        if set(z.namelist()) != set(ZIP_MEMBERS):
            raise RuntimeError("zip member set changed")
        for member in ZIP_MEMBERS:
            src_hash = hashlib.sha256((root / member).read_bytes()).hexdigest()
            zip_hash = hashlib.sha256(z.read(member)).hexdigest()
            if src_hash != zip_hash:
                raise RuntimeError(f"sha256 mismatch for {member}")

    return {"ok": True, "url": payment_url, "replaced": count, "zip": "talent-radar-product.zip"}


def main() -> int:
    if len(sys.argv) != 2:
        print("usage: python3 tools/set_payment_url.py https://pay.example.com/...", file=sys.stderr)
        return 2
    root = Path(__file__).resolve().parent.parent
    try:
        result = set_payment_url(root, sys.argv[1])
    except (ValueError, FileNotFoundError, RuntimeError) as exc:
        print(f"error: {exc}", file=sys.stderr)
        return 1
    print(f"payment link configured; replaced {result['replaced']} placeholder(s)")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
