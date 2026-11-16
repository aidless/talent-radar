# Talent Radar Growth Implementation Plan

> **For agentic workers:** REQUIRED SUB-SKILL: Use subagent-driven-development (recommended) or executing-plans to implement this plan task-by-task. Steps use checkbox (`- [ ]`) syntax for tracking.

**Goal:** Ship the five growth artifacts: payment-link replacement tooling, launch copy, real-user validation kit, data-pool runbook, and portfolio case-study page.

**Architecture:** All work stays inside the clean OSS mirror `/tmp/opencode/talent-radar-oss`. The existing product remains unchanged except for optional payment-link replacement via a helper script and documentation additions. CI continues to run Python and JavaScript checks; git push stays on SSH while GitHub API uses the gh keyring token.

**Tech Stack:** Python 3 standard library, unittest, Node.js for JS checks, single-file HTML/CSS, GitHub CLI API, Git over SSH.

**Spec:** `docs/superpowers/specs/2026-11-16-talent-radar-growth-design.md`

## Global Constraints
- Do not fabricate payment URLs, user counts, screenshots, reliability claims, survey results, or platform metrics.
- Keep `[购买链接]` in `sell/index.html` until a real payment URL is supplied.
- Product zip members must remain exactly: `index.html`, `sell/index.html`, `serve.py`, `prompts.md`, `README.md`, `launch.md`, `research/README.md`, `research/recruit.md`, `research/feedback-form.md`, `data/.gitkeep`.
- Source/zip sha256 must match for every zip member.
- Static GitHub Pages demo has no backend; AI deep-dive and data-pool endpoints require local `serve.py`.
- Real-user study status is “材料就绪、未招募、无结果” until actual data exists.
- Do not output the full GitHub token in any log, response, or committed file.
- Push with SSH remote; use gh only for API operations.

## Review Focus
- A fake or malformed payment URL must be rejected and must not modify product files — test in Task 1.
- Launch copy must avoid “科学测评/认证/诊断” overclaims — test in Task 2.
- Research analyzer must ignore open-text fields and mark insufficient data as “观察不足，未做结论” — test in Task 3.
- Data-pool thresholds must handle n=199/200/500 boundaries and unconfigured key — test in Task 4.
- Portfolio page must link only existing public URLs and state static-demo limitations — test in Task 5.

---

### Task 1: Payment-link replacement helper

**Files:**
- Create: `tools/set_payment_url.py`
- Create: `tests/test_payment_link.py`
- Modify: `README.md`
- Test: `tests/test_payment_link.py`

**Interfaces:**
- Consumes: existing `sell/index.html`, `README.md`, product zip member list.
- Produces: `set_payment_url(repo_root: Path, payment_url: str) -> dict` returning `{"ok": True, "url": ..., "replaced": N, "zip": "talent-radar-product.zip"}`.

- [ ] **Step 1: Write failing tests for URL validation and replacement**

```python
def test_rejects_non_http_url(tmp_repo):
    with pytest.raises(ValueError):
        set_payment_url(tmp_repo, "javascript:alert(1)")

def test_replaces_placeholder_and_rebuilds_zip(tmp_repo):
    result = set_payment_url(tmp_repo, "https://pay.example.com/talent-radar")
    assert result["ok"] is True
    assert result["replaced"] >= 1
    assert "[购买链接]" not in (tmp_repo / "sell/index.html").read_text()
    assert (tmp_repo / "talent-radar-product.zip").exists()
```

- [ ] **Step 2: Run tests to verify they fail**

Run: `python3 -m unittest tests.test_payment_link -v`
Expected: FAIL because `tools/set_payment_url.py` does not exist.

- [ ] **Step 3: Implement helper**

Implement `set_payment_url(repo_root: Path, payment_url: str) -> dict` in `tools/set_payment_url.py`. Validate scheme in `{"http", "https"}` and non-empty netloc; reject otherwise. Replace every `[购买链接]` occurrence in `sell/index.html`, rebuild the fixed 10-member zip with source/zip sha256 verification, and update the README payment status line.

- [ ] **Step 4: Run tests and full suite**

Run: `python3 -m unittest discover -s tests -p 'test_*.py' && node tests/test_datapool_js.js`
Expected: all tests PASS.

- [ ] **Step 5: Commit and push**

```bash
git add tools/set_payment_url.py tests/test_payment_link.py README.md talent-radar-product.zip
git commit -m "feat: add configurable payment link helper"
ssh -o BatchMode=yes -T git@github.com >/dev/null
git push origin main
```

### Task 2: Launch copy expansion

**Files:**
- Modify: `launch.md`
- Test: `tests/test_launch_copy.py`

**Interfaces:**
- Consumes: product positioning from README and sell page.
- Produces: launch copy sections for Xiaohongshu, V2EX, Jike with titles, body, comment follow-up, and preflight checklist.

- [ ] **Step 1: Write failing copy-guard tests**

```python
def test_launch_has_three_channels():
    text = Path("launch.md").read_text(encoding="utf-8")
    for heading in ["小红书", "V2EX", "即刻"]:
        assert heading in text

def test_launch_has_no_overclaims():
    text = Path("launch.md").read_text(encoding="utf-8")
    for banned in ["科学测评认证", "心理诊断", "信度效度认证"]:
        assert banned not in text
```

- [ ] **Step 2: Run tests to verify they fail**

Run: `python3 -m unittest tests.test_launch_copy -v`
Expected: FAIL for missing full channel sections or missing checklist.

- [ ] **Step 3: Expand launch.md**

Add full copy blocks with exact posting text, first-comment text, and a preflight checklist. Keep honest phrasing and keep `[购买链接]` as placeholder where a payment link is needed.

- [ ] **Step 4: Run tests and full suite**

Run: `python3 -m unittest discover -s tests -p 'test_*.py' && node tests/test_datapool_js.js`
Expected: all tests PASS.

- [ ] **Step 5: Commit and push**

```bash
git add launch.md tests/test_launch_copy.py
git commit -m "docs: expand launch copy for three channels"
git push origin main
```

### Task 3: Real-user validation kit status and evidence

**Files:**
- Create: `research/STATUS.md`
- Modify: `research/README.md`
- Test: `tests/test_research_status.py`

**Interfaces:**
- Consumes: `research/analyze.py`, `research/recruit.md`, `research/feedback-form.md`.
- Produces: status document with explicit “材料就绪、未招募、无结果” and go/no-go criteria.

- [ ] **Step 1: Write failing status tests**

```python
def test_status_is_honest():
    text = Path("research/STATUS.md").read_text(encoding="utf-8")
    assert "材料就绪、未招募、无结果" in text
    assert "20–30" in text
    assert "30 天" in text

def test_status_has_no_fake_results():
    text = Path("research/STATUS.md").read_text(encoding="utf-8")
    for banned in ["retest_corr=", "信度高", "效度好"]:
        assert banned not in text
```

- [ ] **Step 2: Run tests to verify they fail**

Run: `python3 -m unittest tests.test_research_status -v`
Expected: FAIL because `research/STATUS.md` does not exist.

- [ ] **Step 3: Write status document**

Create `research/STATUS.md` with status, target sample, timeline, data fields, go/no-go rules, and a results placeholder that explicitly says no results exist yet.

- [ ] **Step 4: Run tests and full suite**

Run: `python3 -m unittest discover -s tests -p 'test_*.py' && node tests/test_datapool_js.js`
Expected: all tests PASS.

- [ ] **Step 5: Commit and push**

```bash
git add research/STATUS.md research/README.md tests/test_research_status.py talent-radar-product.zip
git commit -m "docs: add honest validation study status"
git push origin main
```

### Task 4: Data-pool runbook and boundary regression

**Files:**
- Create: `docs/DATA-POOL.md`
- Modify: `tests/test_datapool.py`
- Test: `tests/test_datapool.py`

**Interfaces:**
- Consumes: `serve.py:validate_contribution`, `serve.py:is_effective`, `serve.py:summary`, `RESEARCH_KEY`.
- Produces: operator runbook covering key setup, privacy, endpoints, thresholds, and cut rule.

- [ ] **Step 1: Write failing boundary tests**

```python
def test_summary_boundaries(tmp_path):
    rows = make_rows(n=200)
    assert summary(tmp_path / "a.jsonl")["verdict"] == "collecting"
    rows = make_rows(n=500)
    assert summary(tmp_path / "b.jsonl")["verdict"] == "ready"

def test_summary_cut_below_200(tmp_path):
    rows = make_rows(n=199)
    assert summary(tmp_path / "c.jsonl")["verdict"] == "cut"
```

- [ ] **Step 2: Run tests to verify they fail**

Run: `python3 -m unittest tests.test_datapool -v`
Expected: FAIL because the boundary tests are absent.

- [ ] **Step 3: Add tests and runbook**

Add boundary tests using existing helper patterns. Write `docs/DATA-POOL.md` with local commands, environment variable, API request examples, privacy rules, and decision thresholds copied verbatim from design.

- [ ] **Step 4: Run tests and full suite**

Run: `python3 -m unittest discover -s tests -p 'test_*.py' && node tests/test_datapool_js.js`
Expected: all tests PASS.

- [ ] **Step 5: Commit and push**

```bash
git add docs/DATA-POOL.md tests/test_datapool.py
git commit -m "docs: add data pool runbook and boundary tests"
git push origin main
```

### Task 5: Portfolio case-study page

**Files:**
- Create: `portfolio/index.html`
- Create: `portfolio/README.md`
- Create: `tests/test_portfolio.py`
- Test: `tests/test_portfolio.py`

**Interfaces:**
- Consumes: public URLs `https://github.com/aidless/talent-radar`, `https://aidless.github.io/talent-radar/`, `https://github.com/aidless/talent-radar/releases/tag/v1.0.0`.
- Produces: single-file case-study page and a maintenance note.

- [ ] **Step 1: Write failing page contract tests**

```python
def test_portfolio_links_existing_assets():
    html = Path("portfolio/index.html").read_text(encoding="utf-8")
    for url in [
        "https://github.com/aidless/talent-radar",
        "https://aidless.github.io/talent-radar/",
        "https://github.com/aidless/talent-radar/releases/tag/v1.0.0",
    ]:
        assert url in html

def test_portfolio_states_limits():
    html = Path("portfolio/index.html").read_text(encoding="utf-8")
    assert "静态 Demo" in html
    assert "心理测评认证" in html
```

- [ ] **Step 2: Run tests to verify they fail**

Run: `python3 -m unittest tests.test_portfolio -v`
Expected: FAIL because `portfolio/index.html` does not exist.

- [ ] **Step 3: Build portfolio page**

Create a dependency-free single HTML page with hero, evidence links, architecture summary, honest limitations, and next-step checklist. Include a note that this is a commercial-tool side line, not a validated psychometric instrument.

- [ ] **Step 4: Run tests and full suite**

Run: `python3 -m unittest discover -s tests -p 'test_*.py' && node tests/test_datapool_js.js && python3 -m py_compile serve.py research/analyze.py tools/set_payment_url.py`
Expected: all tests PASS.

- [ ] **Step 5: Commit and push**

```bash
git add portfolio/index.html portfolio/README.md tests/test_portfolio.py
git commit -m "feat: add portfolio case study page"
git push origin main
```

### Final Task: Verification and delivery

- [ ] **Step 1: Verify full suite**

Run: `python3 -m unittest discover -s tests -p 'test_*.py' && node tests/test_datapool_js.js && python3 -m py_compile serve.py research/analyze.py tools/set_payment_url.py`
Expected: all PASS.

- [ ] **Step 2: Verify zip and public assets**

Run: `unzip -t talent-radar-product.zip && curl -sS -o /dev/null -w '%{http_code}\n' https://aidless.github.io/talent-radar/ && gh release view v1.0.0 --json assets --jq '.assets | length'`
Expected: `No errors detected`, `200`, `1`.

- [ ] **Step 3: Report completion**

List the five artifacts, exact public URLs, and remaining external blockers: real payment URL, real recruits, real contributions.
