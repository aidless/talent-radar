# Contributing

Thanks for improving Talent Radar.

## Development

The OSS repository is flattened: `index.html`, `serve.py`, `README.md`, `tests/`, and `research/` live at the repository root. The downloadable product archive is `talent-radar-product.zip`.

Run the full suite before opening a pull request:

```bash
python3 -m unittest discover -s tests -p 'test_*.py'
node tests/test_datapool_js.js
python3 -m py_compile serve.py research/analyze.py
```

If tests are run from a checkout where the toolkit lives in `talent-radar/`, set `TALENT_RADAR_ROOT=/path/to/talent-radar`.

## Contribution rules

- Keep `index.html` self-contained and offline-first. New runtime dependencies need an explicit rationale.
- Keep anonymous contribution off by default; consent and a configured `TALENT_RADAR_RESEARCH_KEY` are mandatory.
- Treat results as hypotheses, not validated psychometric measurements. Avoid claims of clinical validity.
- Add a RED→GREEN regression test for each behavior change.
- Do not add real payment links, private tokens, or generated screenshots to the repository without an explicit owner decision.

## Pull requests

Describe the behavior change, the commands you ran, and any limitation you know about. CI runs the same Python and JavaScript checks on every push and pull request.
