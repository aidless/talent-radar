# 天赋雷达 A/B/C 扩展 Implementation Plan

> **For agentic workers:** REQUIRED SUB-SKILL: Use subagent-driven-development (recommended) or executing-plans to implement this plan task-by-task. Steps use checkbox (`- [ ]`) syntax for tracking.

**Goal:** 按顺序完成 A 匿名数据池、B 真人验证、C 收款闭环，所有产物落在 `talent-radar/`。

**Architecture:** `serve.py` 扩展两个本地 API + append-only JSONL 存储；`index.html` 加默认关闭的匿名贡献开关；`research/analyze.py` 离线算 30 天验证量；零售 zip 重建纳入 launch 与研究文档。三任务共享同一工作树，不新开服务端口。

**Tech Stack:** Python 3 stdlib (`http.server`, `hashlib`, `statistics`)、原生 JS (Chrome `crypto.subtle` / fallback)、Node vm 冒烟、zip/unzip、sha256sum。

**Spec:** `docs/superpowers/specs/2026-11-16-talent-radar-abc-design.md`

## Global Constraints
- 顺序 A→B→C，D/E 冻结（`docs/...design.md` 首行）。
- 匿名上传默认关闭；demo (`?demo=1`) 绝不上传；二次确认弹窗。
- 有效 n≥500 才 ready；30 天窗口内 <200 → cut；summary 必须输出 actual n 与窗口天数。
- 真人验证 20–30 人 / 30 天 / 匿名 ID；不足 20 或留存 <50% → insufficient。
- 收款链接未给时用 `[购买链接]` 占位 + README 明示待替换；不擅自部署/push。
- 工作区路径含字面反斜杠，用相对路径；只 add 自己的文件。

## Review Focus
1. file:// 下点上传 → 失败 toast 且本地结果保留（Task 1 测试）。
2. 重复上传按 contributor_hash 去重（Task 1 服务端测试）。
3. 30 天窗口边界口径固定（Task 1 测试）。
4. analyze.py 不输出开放文本原文（Task 2 测试）。
5. 占位链接时 README 明示待替换（Task 3 检查）。

---

### Task 1: A 匿名数据池

**Files:**
- Modify: `talent-radar/serve.py`（追加 `/api/contribute`、`/api/contributions/summary`）
- Modify: `talent-radar/index.html`（结果页增贡献开关 + 上传按钮 + JS）
- Create: `talent-radar/data/.gitkeep`
- Test: `talent-radar/tests/test_datapool.py`、`talent-radar/tests/test_datapool_js.js`

**Interfaces:**
- Produces: `summary(window_days=30) -> {window_days,valid_n,total_n,invalid_n,ready,verdict}`；`POST /api/contribute` 接受 spec schema；`windowContribution()` 返回贡献 JSON。

- [ ] **Step 1** 写 `tests/test_datapool.py`：用 tempfile JSONL 注入 499/500/199/200 样本与重复 hash/demo/consent=false，断言 ready/verdict 与去重计数（RED）。
- [ ] **Step 2** 运行 `python3 -m unittest talent-radar/tests/test_datapool.py -v`，确认因无实现而 FAIL。
- [ ] **Step 3** 实现 `serve.py` 中 `validate_contribution(payload)->bool|str`、`summary(path, window_days=30)`、两个路由（未配置 `TALENT_RADAR_RESEARCH_KEY` 返回 503；GET summary 校验 `X-Research-Key`）。
- [ ] **Step 4** 运行同命令，确认 PASS。
- [ ] **Step 5** 写 `tests/test_datapool_js.js`：Node vm 打桩 DOM/crypto/fetch，`?demo=1` 时点击上传不产生 fetch；非 demo 且开关关时无 fetch；开关开+二次确认后 POST body 含 consent.version='1.0'（RED）。
- [ ] **Step 6** 运行 `node talent-radar/tests/test_datapool_js.js`，确认 FAIL。
- [ ] **Step 7** 在 `index.html` 结果页加 `#contrib-toggle`（默认 unchecked、存 localStorage `talent-radar-contrib-v1`）、`#contrib-upload` 按钮；`windowContribution()` 按 spec 组装；`submitContribution()` 弹 confirm → fetch(`/api/contribute`) → toast 成功/失败，catch 不阻塞；`isDemo` 时隐藏整个卡片。
- [ ] **Step 8** 运行同命令，确认 PASS。
- [ ] **Step 9** 提交：`git add talent-radar/serve.py talent-radar/index.html talent-radar/data/.gitkeep talent-radar/tests/test_datapool.py talent-radar/tests/test_datapool_js.js && git commit -m "feat: opt-in anonymous contribution pool"`

### Task 2: B 真人验证

**Files:**
- Create: `talent-radar/research/recruit.md`, `feedback-form.md`, `README.md`, `analyze.py`
- Test: `talent-radar/tests/test_research.py`

**Interfaces:**
- Produces: `analyze(csv_path) -> dict{n,retest_corr,self_beh_gap_mean,gap_abs_p90,third_party_agreement,drop_rate,confidence}`

- [ ] **Step 1** 写 `tests/test_research.py`：生成临时 CSV（19人→insufficient；20人留存60%→provisional；含开放文本列确认不出现在输出；缺 day30 不计入 Pearson；gap 从实际列重算）（RED）。
- [ ] **Step 2** 运行 `python3 -m unittest talent-radar/tests/test_research.py -v`，确认 FAIL。
- [ ] **Step 3** 实现 `research/analyze.py`（stdlib `csv`/`statistics`；Pearson 手算；只读 `pid,day,self_rating,behavior_tag,third_party_agreement,drop_reason` 列；输出 JSON 到 stdout）。
- [ ] **Step 4** 运行同命令，确认 PASS。
- [ ] **Step 5** 写 `research/recruit.md`（20–30 人、30 天、匿名 ID、知情同意、退出权、纳入排除标准）、`feedback-form.md`（Day 0/14/30 + 每日 1 题）、`README.md`（只报观察量、禁止"科学测评认证"话术、结果如何写销售页/面试叙事）。
- [ ] **Step 6** 检查三份 md 不含"认证/信度高/效度好"字样：`grep -nE '认证|信度高|效度好' talent-radar/research/*.md || echo OK`。
- [ ] **Step 7** 提交：`git add talent-radar/research talent-radar/tests/test_research.py && git commit -m "docs+tool: 30-day human validation protocol"`

### Task 3: C 收款闭环

**Files:**
- Modify: `talent-radar/sell/index.html`, `talent-radar/README.md`
- Create: `talent-radar/launch.md`
- Test: `talent-radar/tests/test_handover.py`

**Interfaces:**
- Consumes: A/B 产物路径。
- Produces: `talent-radar-product.zip` 含 8 项；sha256 源/包一致；`unzip -t` 通过。

- [ ] **Step 1** 写 `tests/test_handover.py`：断言 sell/index.html 无 `[购买链接占位]`、README 含"占位待替换"、launch.md 含 3 条卖点与 FAQ、zip 内 sha256 与磁盘文件一致（RED）。
- [ ] **Step 2** 运行 `python3 -m unittest talent-radar/tests/test_handover.py -v`，确认 FAIL。
- [ ] **Step 3** 将 `sell/index.html` 的 `[购买链接占位]` 全部换成 `[购买链接]`（保留为 PAYMENT_URL 占位常量，用户给链接后一行替换）；README 加部署说明；写 `launch.md`（标题/卖点/渠道模板/合规口径/FAQ）。
- [ ] **Step 4** 写 `tests/test_handover.py` 的 zip 校验部分：重建 `talent-radar-product.zip`（`zip -q -r -FS ... index.html sell/index.html serve.py prompts.md README.md launch.md research/*.md data/.gitkeep`），断言 zip 内每项 sha256 与源一致、`unzip -t` 返回 0。
- [ ] **Step 5** 运行全量：`python3 -m unittest discover -s talent-radar/tests -v && node talent-radar/tests/test_datapool_js.js && node --check /tmp/talent-radar-script.js`，确认全绿。
- [ ] **Step 6** 提交：`git add talent-radar/sell/index.html talent-radar/README.md talent-radar/launch.md talent-radar/tests/test_handover.py talent-radar-product.zip && git commit -m "feat: launch handover with payment placeholder"`

## Final
- 全量 smoke + zip hash + 最终复核（fresh reviewer 对整个 BASE→HEAD diff，不只看 HEAD~1）。
- 交付：present zip、launch.md、README.md；说明收款链接仍是占位，给出一行替换命令。
