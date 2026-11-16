# Talent Radar · 天赋雷达

[![CI](https://github.com/aidless/talent-radar/actions/workflows/ci.yml/badge.svg)](https://github.com/aidless/talent-radar/actions/workflows/ci.yml)

一个本地优先的结构化自省工具：40 道题覆盖 10 个维度，行为题 / 他人反馈题 / 自评题三轨加权，输出雷达图、自评—行为差距、排序敏感度提示，以及三段可复制的 AI 追问 Prompt。

这不是心理测评认证工具，结果只作为自我观察与后续验证的假设。

## 功能
- **在线 Demo**：[https://aidless.github.io/talent-radar/](https://aidless.github.io/talent-radar/)（静态版；由 `pages.yml` 从 main 分支自动部署，AI 深挖与数据池接口需本地 `serve.py`）。
- **快速自测**：40 题 × 10 维，端到端本地运行，结果存浏览器 localStorage。
- **雷达结果**：组合命名、top3 维度、自评 vs 行为差距、并列敏感度、30 天验证实验方向。
- **分享卡片**：1080×1440 PNG，Canvas 本地绘制，不上传图片。
- **Prompt 三件套**：深度挖掘 / 反证官 / 落地，文本可直接复制到任意 AI 对话。
- **求职定位**：基于结果生成可复制的定位句、简历段落与 STAR 故事骨架。
- **本地 AI 深挖**（可选）：`serve.py` 同源托管并反代本机 OpenAI-compatible 网关，解决 file:// 下的 CORS 问题。
- **匿名数据池**（默认关闭）：用户手动勾选 + 二次确认才上传去标识化分数；未配置研究 key 时服务端返回 503。
- **真人验证协议**：`research/` 提供 20–30 人、30 天的招募与反馈模板；`analyze.py` 只读取结构化列，不导出开放文本。

## 快速开始
```bash
# 方式 1：直接双击 index.html（完整自测、导出、Prompt 复制均可用）
# 方式 2：本地服务（AI 深挖、数据池需要）
python3 serve.py
# 打开 http://127.0.0.1:8018
```

## 测试
```bash
python3 -m unittest discover -s tests -p 'test_*.py'
node tests/test_datapool_js.js
python3 -m py_compile serve.py research/analyze.py
```

## 目录
- `index.html`：单文件主工具
- `serve.py`：本地服务 + 数据池接口
- `prompts.md`：Prompt 三件套
- `sell/`：销售页（含前 5 题试玩；`[购买链接]` 占位待替换，真实收款链接未配置）
- `research/`：真人验证协议与分析脚本
- `tests/`：Python / JS 测试
- `docs/`：设计 spec 与实施计划
- `launch.md`：发布文案与 FAQ
- `talent-radar-product.zip`：打包产物（10 文件）

## 隐私
- 默认不发起任何网络请求；答题数据只存本机 localStorage。
- 只有手动开启匿名贡献并二次确认后，才会向服务端发送去标识化分数。
- 试玩模式（`?demo=1`）不落盘、不上传。
- 服务端可选，未配置 `TALENT_RADAR_RESEARCH_KEY` 时数据池接口返回 503。

## Contributing
见 [CONTRIBUTING.md](CONTRIBUTING.md)。CI 在每次 push 与 pull request 上运行 Python / JavaScript 检查。

## License
MIT，见 [LICENSE](LICENSE)。
