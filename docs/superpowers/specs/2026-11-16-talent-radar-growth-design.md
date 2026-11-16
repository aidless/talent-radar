# Talent Radar 增长与证据闭环设计

## Intent
把已经开源的 Talent Radar 从“能用的工具”推进到“可传播、可验证、可复盘”的产品闭环。用户明确要求“全做”，范围固定为五项：收款链接、发布文案、真人验证、数据池、作品集页面。

## Goals
1. 收款入口可配置：没有真实支付 URL 时保留 `[购买链接]`，不编造地址；收到真实 URL 后可一键替换、重建 zip、更新 Release 资产。
2. 发布文案可直接发：小红书、V2EX、即刻各一版，口径诚实，不宣称心理测评认证。
3. 真人验证可执行：20–30 人、30 天记录、第 0/14/30 天量表、匿名聚合，样本不足时只能写“观察不足，未做结论”。
4. 数据池可运行且有门槛：默认关闭、二次确认、30 天窗口、有效样本 n≥500 才 ready，n<200 则 cut。
5. 作品集页面可展示：连接仓库、Demo、Release，明确这是商业小工具副线，列真实能力与限制。

## Non-goals
- 不做心理测量学认证、不做诊断、不宣称信度效度已验证。
- 不伪造用户数、准确率、截图、收款链接或平台数据。
- 不把静态 Demo 说成完整服务：Demo 无后端 AI 深挖与数据池功能。
- 不启动真实招募投递或真实收款上架；本轮只产出可直接使用的材料与本地闭环。

## Constraints
- 工作目录固定为 `/tmp/opencode/talent-radar-oss`，这是干净 OSS 镜像；主工作区有大量他人改动，禁止把主工作区整体托管。
- GitHub HTTPS 通道已修好；gh keyring 保存用户提供的 token，输出必须遮蔽 token。
- git HTTPS 受本机失效代理 `http://127.0.0.1:7897` 影响；git push 继续走 SSH remote。
- 产品 zip 必须保持 10 个固定成员，且源/包 sha256 一致。
- 真人验证原始开放文本不进入汇总；`analyze.py` 只读结构化列。
- 所有新增数量、链接、CI 状态必须来自现读命令/文件。

## Approaches
1. **最小闭环（选中）**：在现有仓库内增加文案/页面/助手脚本，复用已有测试、CI、Release、Pages；改动小、风险低、可一次性验证。缺点是真人验证与数据池仍需真实用户/真实部署后才有数据。
2. **另建增长仓库**：把文案、作品集、招募拆到独立 repo；结构更干净但会切断与现有 GitHub/Demo/Release 的直接证据链，增加维护面。
3. **接入在线表单/数据库**：立即开始收集真实数据；需要部署、凭据、隐私配置和持续运维，超出当前仓库内闭环。

选择 1：用户要的是“全做”现有五项，且现有仓库已有 CI、Pages、Release、测试与隐私口径，最快形成可验证交付。

## Design
- **收款链接**：新增 `tools/set_payment_url.py`，接口 `set_payment_url(repo_root: Path, payment_url: str) -> dict`。脚本校验 URL 必须是 http/https，替换 `sell/index.html` 中所有 `[购买链接]`，重建固定成员 zip，写回 README 的付款状态行。未提供真实 URL 时只保留占位，不调用该脚本。
- **发布文案**：扩展 `launch.md`，保留现有三平台模板，增加完整版小红书/V2EX/即刻文案、标题备选、评论区引导和发布前检查清单。
- **真人验证**：保留 `research/recruit.md`、`research/feedback-form.md`、`research/analyze.py`；新增 `research/STATUS.md` 记录当前状态为“材料就绪、未招募、无结果”，并写清 minimal go/no-go、数据字段和复盘模板。
- **数据池**：现有 `serve.py` 已实现默认关闭、校验、window=30、n≥500 ready / n<200 cut；新增 `docs/DATA-POOL.md` 作为运行手册，增加测试覆盖“无 key 503、有效样本计数、阈值边界、README 隐私口径”。
- **作品集**：新增 `portfolio/index.html` 单页面，用真实链接连接 GitHub、Demo、Release；展示能力边界、技术要点、验证状态和限制；加入 `portfolio/README.md` 说明如何展示与更新。

## Builder choices
- 作品集页面采用无依赖单文件 HTML，沿用项目“本地优先、双击可看”的风格。
- 文案加入仓库而不是外链，便于面试和发布时逐字引用。
- 收款替换做成脚本而不是直接改死链接，因为当前没有真实支付 URL；这是防止伪造链接的核心措施。
