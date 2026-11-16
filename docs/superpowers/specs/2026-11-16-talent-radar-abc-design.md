# 天赋雷达 A/B/C 扩展设计 spec

> 权威来源：用户 m00303 路线菜单 + m00308 "按顺序全做"。D（团队版/GitHub）、E（收手）冻结。

## 目标与顺序
1. A 匿名数据池：默认关闭的匿名贡献开关，schema 明确，n≥500 才写统计报告，30 天 <200 份则砍掉该功能。
2. B 真人验证：20–30 人试用，30 天反馈，产出可复核的信度/效度证据，反哺销售页与面试叙事。
3. C 上线收款闭环：销售页 `[购买链接占位]` 替换为真实链接（未给则占位交付并标注），zip 重建、发布文案。

## 硬约束
- 产品承诺"无网络请求·数据存 localStorage"必须与匿名上传共存：上传默认关闭，开启需显式二次确认，文案同步说明。
- 数据池只收去标识化字段，不收姓名/联系方式/开放文本原文；年龄职业只收分段。
- 统计报告门槛：有效样本 n≥500；30 天窗口内有效样本 <200 判"砍"，报告必须标注 actual n 与窗口。
- 真人验证：样本 20–30；周期 30 天；匿名 ID；收集自评-行为差距、重测一致性、第三方反馈；不得把无信度数据包装成"科学测评"。
- 收款链接未提供时：`[收款平台]` / `[购买链接]` 占位 + README 标注一行"替换占位后即可公开部署"，不得假装已上线。
- 工作区根含字面反斜杠；所有路径用工作区相对路径。不擅自 push / 部署到外部平台（用户未提供凭据与平台）。
- 只改天赋雷达相关文件；工作树有他人未提交改动，只 add 自己的文件。

## A 数据池细节
### schema（POST /api/contribute，JSON）
```
schema_version: 1
contributor_hash: string (匿名 SHA-256 前16位，前端生成)
created_at: ISO8601
answers: [{qid, value:1..5, weight, dtype:'beh'|'fb'|'self', ms_spent}]
scores: {dims: {k: {score, behMean, selfMean, vol}}, ranked:[k], top2gap:number}
meta: {age_band, occupation_band, straight_lined:boolean, interrupted:boolean,
       demo:false, source:'local'|'web'}
consent: {upload:true, timestamp:ISO8601, version:'1.0'}
```
- 服务端：`serve.py` 增加 `POST /api/contribute` 与 `GET /api/contributions/summary`（只在 X-Research-Key 头匹配环境变量 `TALENT_RADAR_RESEARCH_KEY` 时返回汇总；未配置 key 时两个接口均返回 503）。
- 存储：`talent-radar/data/contributions.jsonl`（append-only，本地文件）；`.gitignore` 忽略。
- 汇总 `summary()`：读全部行，按 schema_version 过滤，按 contributor_hash 去重（保留最新），标记 `straight_lined`/`interrupted`/`demo:true`/`consent.upload:false` 为无效；返回 `{window_days:30, valid_n, total_n, invalid_n, ready: valid_n>=500, verdict: 'ready'|'collecting'|'cut'}`；`cut` 条件为窗口内 valid_n<200。
- 前端：`index.html` 结果页加"匿名贡献开关"（默认关闭，`localStorage` 持久化）；开关打开时弹 `confirm()` 二次确认，说明上传字段；仅在用户主动点"上传本次结果"时 POST；失败只 toast 不阻塞使用。
- demo 模式（`?demo=1`）绝不上传。

### 测试（Node vm 内断言 + Python unittest）
- schema 必填字段齐全；`consent.upload:true` 且 version='1.0' 才接受，否则 400。
- 去重/无效标记正确；n=499 ready=false；n=500 ready=true；窗口内 199 cut=true、200 collecting。
- demo 模式前端没有 POST 调用。

## B 真人验证细节
### 交付文件
- `talent-radar/research/recruit.md`：20–30 人招募文案（纳入/排除标准、知情同意、匿名 ID、30 天时间线、退出权）。
- `talent-radar/research/feedback-form.md`：每日 1 题 + 第 0/14/30 天量表；字段：`pid, day, self_rating(1-5), behavior_event(文本本地留存不上传), feedback_tag, drop_reason`。
- `talent-radar/research/analyze.py`：输入 `feedback.csv`，输出 `{n, retest_corr, self_beh_gap_mean, gap_abs_p90, third_party_agreement, drop_rate, confidence:'provisional'|'insufficient'}`；n<20 或 30 天留存 <50% 判 insufficient；不输出"信度高/效度好"字样，只输出观察量。
- `talent-radar/research/README.md`：明确这是"自省工具验证"而非"科学测评认证"，结果如何写入销售页/面试叙事（只写实测数与口径）。

### 测试（Python unittest）
- n=19 insufficient；n=20 且留存 60% provisional。
- 重测相关计算使用 Pearson，缺失 day30 按 drop 处理不计入相关。
- 缺口 `self_beh_gap_mean` 与 `gap_abs_p90` 从实际 CSV 重算。

## C 收款闭环细节
- 链接：`sell/index.html` 中所有 `[购买链接占位]` 替换为 `PAYMENT_URL` 常量（默认 `[购买链接]`）；`README.md` 加部署说明。
- 发布文案：`talent-radar/launch.md`：标题、卖点 3 条、发布渠道模板（小红书/即刻/V2EX）、合规口径（只说"结构化自省工具"不说"科学测评"）、FAQ（隐私/退款/AI 深挖说明）。
- zip 重建：`zip -q -r -FS talent-radar-product.zip index.html sell/index.html serve.py prompts.md README.md launch.md research/*.md data/.gitkeep`（research/analyze.py 不进零售包，保留在研究目录）。
- 校验：`unzip -t` + 源/包内 sha256 一致 + smoke 全绿。

## Review Focus（plan 的测试没覆盖但会咬人的输入）
1. 用户在 file:// 打开时开贡献开关 → POST 必然失败：必须 toast 失败并保留本地结果，不阻塞测评。
2. 贡献开关打开后重复点击上传 → 去重按 contributor_hash，服务端不得重复计数。
3. 30 天窗口边界：第 30 天整点的样本纳入/排除口径必须固定并在 summary 输出。
4. 真人验证 CSV 里有开放文本反馈 → analyze.py 只读结构化列，不输出原文。
5. 收款链接仍是占位时 → README/发布文案必须明示"占位待替换"，不能表现为已可购买。
