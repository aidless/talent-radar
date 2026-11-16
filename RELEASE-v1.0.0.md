# v1.0.0 发布说明（待在 GitHub Releases 页面发布）

由于本机 GitHub HTTPS token 失效（`gh api` 返回 `Bad credentials`，HTTP 401），本文件提供可直接粘贴的发布内容；关联产物为仓库根目录 `talent-radar-product.zip`。

## 标题

v1.0.0 — Talent Radar

## 说明

First stable OSS release.

Talent Radar is a local-first structured self-reflection tool: 40 questions across 10 dimensions, three-track weighting (behavior / feedback / self-assessment), radar output, self-vs-behavior gap and tied-rank sensitivity notes, plus three copyable AI prompts.

Included:
- Offline single-file self-assessment (`index.html`)
- 1080×1440 share-card PNG generation
- Three Prompt templates: deep dive / falsification / action plan
- Local AI deep-dive server (`serve.py`, optional)
- Opt-in anonymous data pool with explicit consent; disabled without `TALENT_RADAR_RESEARCH_KEY`
- 20–30 participant, 30-day validation protocol and analyzer (`research/`)
- Product archive with 10 files

Verification at release time:
- 15 Python tests passed
- 6 JavaScript tests passed
- `python3 -m py_compile serve.py research/analyze.py` passed
- `unzip -t talent-radar-product.zip` reported no errors

Limitations:
- Not a validated psychometric instrument; scores are hypotheses for further observation.
- GitHub Pages serves the static demo only; AI deep-dive and data-pool endpoints need a local `serve.py`.
- The sales page still contains `[购买链接]` placeholder because no real payment URL has been supplied.

## 手动发布步骤

1. 打开 https://github.com/aidless/talent-radar/releases/new
2. Tag 填 `v1.0.0`，target 选 `2ed038e` 或更新后的 main。
3. 标题和说明粘贴上文。
4. 上传 `talent-radar-product.zip`。
5. 点击 Publish release。
