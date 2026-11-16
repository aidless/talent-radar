# Talent Radar Post-Release Implementation Plan

> **For agentic workers:** REQUIRED SUB-SKILL: Use executing-plans to implement this plan task-by-task. Steps use checkbox (`- [ ]`) syntax for tracking.

**Goal:** Turn the published `aidless/talent-radar` repository into a trustworthy OSS project with CI, live demo, versioned release, portfolio evidence, and an honest payment-link handoff.

**Architecture:** Keep the clean mirror at `/tmp/opencode/talent-radar-oss` as the release tree. Add repository facade files and a CI workflow there, build a root-level static Pages demo that does not overwrite the main tool, create a version tag and release artifact, write evidence-backed portfolio bullets, and document the still-missing real payment URL rather than inventing one.

**Tech Stack:** GitHub Actions (ubuntu-latest, Python 3.11, Node 20), static HTML/CSS/JS, GitHub Pages, `gh`/SSH git, zip, Python unittest, Node smoke tests.

**Spec:** `docs/superpowers/specs/2026-11-16-talent-radar-abc-design.md`, the public repo contents, and the user's m00511 instruction "全做".

## Global Constraints

- `origin` is `ssh://git@github.com/aidless/talent-radar.git`; push only this clean mirror, never the shared deepseek workspace.
- HTTPS `gh` token is invalid (HTTP 401); SSH git works. API/Release operations must be attempted explicitly and reported with actual output if blocked.
- Do not fabricate screenshots, badge status, release assets, payment links, or resume numbers.
- Every claimed test/CI/Pages/Release state must be verified by a fresh command output before it is reported.
- Payment URL remains `[购买链接]`; no real URL was supplied.

## Review Focus

- Broken local test paths after flattening the OSS tree: `tests/test_handover.py` still uses `ROOT/talent-radar`; add a portable root override and verify all tests from the OSS root.
- Pages demo must not be confused with the full local tool: disclose that AI deep-dive and data-pool require `serve.py`.
- Release must have real assets; a notes-only Release is a failed release.
- Resume bullets must use only public, recomputable facts from the repo and tests.
- README badge must point to an existing workflow path; no decorative dead links.

---

### Task 1: Repository facade and CI

**Files:**
- Create: `.github/workflows/tests.yml`
- Create: `CONTRIBUTING.md`
- Modify: `README.md`
- Create/Modify: `docs/assets/` screenshot assets only if real files are available; otherwise link to Pages demo.
- Modify: `tests/test_handover.py` for portable OSS-root paths.

**Interfaces:**
- Consumes: existing `tests/test_datapool.py`, `tests/test_research.py`, `tests/test_handover.py`, `tests/test_datapool_js.js`.
- Produces: CI command parity with local tests, contributor instructions, README badges/demo link.

- [ ] **Step 1: Add a failing guard test for the OSS root path** that asserts `ROOT` resolves to the repository root and the handover files exist there.
- [ ] **Step 2: Run it and confirm it fails** with current `ROOT/talent-radar` path.
- [ ] **Step 3: Make `tests/test_handover.py` portable** by resolving `TD = os.environ.get("TALENT_RADAR_ROOT", ROOT)`.
- [ ] **Step 4: Add `.github/workflows/tests.yml`** running Python unittest and JS smoke on push/PR.
- [ ] **Step 5: Add `CONTRIBUTING.md`** covering setup, tests, issue/PR hygiene, privacy constraints.
- [ ] **Step 6: Update README** with CI badge, Pages demo link, contributor link, and explicit static-demo limitation.
- [ ] **Step 7: Run full local suite** and commit only changed OSS files.

### Task 2: GitHub Pages demo

**Files:**
- Create: `docs/demo/index.html` (static landing page with iframe to `../../index.html` locally and a note for Pages).
- Modify: `README.md` with Pages URL.
- Configure: GitHub repository Pages settings via API if credentials permit; otherwise produce exact manual click path and verify public URL status.

**Interfaces:**
- Consumes: repository root `index.html`.
- Produces: public demo URL `https://aidless.github.io/talent-radar/`.

- [ ] **Step 1: Write a guard test** asserting `docs/demo/index.html` exists and links to the main tool.
- [ ] **Step 2: Run it and confirm it fails** before creating demo.
- [ ] **Step 3: Create a static demo page** that embeds or links root `index.html` and states AI/data-pool limitations.
- [ ] **Step 4: Add Pages setup instructions** to README and CONTRIBUTING.
- [ ] **Step 5: Attempt Pages API configuration**; if auth is blocked, record exact command/output and provide manual path.
- [ ] **Step 6: Verify public Pages URL** with curl; report actual status.

### Task 3: v1.0.0 Release

**Files:**
- Modify: `README.md` version references.
- Create: `RELEASE_NOTES_v1.0.0.md`.
- Attach: `talent-radar-product.zip` (already built; reverify hash).

**Interfaces:**
- Consumes: verified zip and test suite from Task 1.
- Produces: tag `v1.0.0` and Release with attached zip.

- [ ] **Step 1: Write a guard test** that `RELEASE_NOTES_v1.0.0.md` exists and contains required facts.
- [ ] **Step 2: Run it and confirm it fails.**
- [ ] **Step 3: Write release notes** with 40 questions/10 dimensions, three prompts, default-off data pool, validation protocol, known limitations.
- [ ] **Step 4: Verify zip integrity and source hashes.**
- [ ] **Step 5: Commit, tag `v1.0.0`, push tag.**
- [ ] **Step 6: Attempt `gh release create` with zip asset**. If HTTPS auth blocks it, use SSH-only git tag and document manual asset-upload path with exact URL.
- [ ] **Step 7: Verify Release asset state** with `gh release view --json assets` if auth permits; otherwise fetch public release page and report status.

### Task 4: Portfolio/resume evidence

**Files:**
- Create: `docs/portfolio/talent-radar-bullets.md`
- Modify only if full resume sync is safe: `/home/liuzewen/make_resume_pdf.py`, CN/EN Markdown, CN/EN HTML.

**Interfaces:**
- Consumes: verified public repo, tests, Pages/Release evidence from Tasks 1–3.
- Produces: short CN/EN bullets that survive fact audit.

- [ ] **Step 1: Draft bullets using only public repo facts** and no unverified numeric claims.
- [ ] **Step 2: Write a guard check** that each bullet maps to a public artifact URL or command output.
- [ ] **Step 3: If resume files are stable, add one concise side-line entry to all five synced files; otherwise keep bullets in `docs/portfolio/` only.
- [ ] **Step 4: Rebuild PDFs and verify page count/A4/text-layer if resume files were touched.**
- [ ] **Step 5: Commit OSS-side portfolio doc and any resume changes made by this task.**

### Task 5: Payment-link handoff

**Files:**
- Modify: `README.md`, `sell/index.html` only if a real URL is supplied.
- Create: `docs/payment-link-handoff.md`.

**Interfaces:**
- Consumes: user-provided real payment URL, if any.
- Produces: explicit handoff note; no invented URL.

- [ ] **Step 1: Confirm no real payment URL was supplied in the current request.**
- [ ] **Step 2: Create handoff doc** with exact replacement target `[购买链接]`, rebuild commands, and release follow-up.
- [ ] **Step 3: Keep placeholder unchanged.**
- [ ] **Step 4: Commit handoff doc.**

### Final Verification

- Run full Python and JS suites from the OSS root.
- Verify git status clean after commits.
- Verify remote HEAD matches local HEAD.
- Verify public repo HTTP 200.
- Verify Pages/Release states with actual command output; report blocked API calls explicitly.
