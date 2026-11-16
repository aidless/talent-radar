# 匿名数据池运行手册

## 适用边界
数据池是可选研究副线，不影响主工具。默认关闭；未配置研究 key 时，前后端两个接口都返回 503。

## 启动
```bash
export TALENT_RADAR_RESEARCH_KEY='replace-with-a-private-key'
python3 serve.py
# http://127.0.0.1:8018
```

不要把 `TALENT_RADAR_RESEARCH_KEY` 写进仓库、README、Release notes 或截图。

## 接口
- `POST /api/contribute`：接收去标识化样本。请求体必须通过 `validate_contribution(payload)`：
  - `schema_version == 1`
  - `consent.upload is True` 且 `consent.version == "1.0"`
  - `meta.demo is not True`
  - `contributor_hash` 至少 8 字符
  - `created_at` 为可解析 ISO 时间
- `GET /api/contributions/summary`：需请求头 `X-Research-Key: <key>`。

未配置 key 时两个接口返回 503，正文含 `data pool disabled: TALENT_RADAR_RESEARCH_KEY not configured`。

## 有效样本口径
`serve.py:is_effective()` 要求：
- 在 30 天窗口内；
- 非 demo；
- `meta.straight_lined` 不为真；
- `meta.interrupted` 不为真；
- 通过完整 schema 与显式同意校验。

`summary()` 按 `contributor_hash` 去重，保留最新一条。阈值：
- `valid_n >= 500` → `verdict=ready`，可考虑写聚合观察；
- `valid_n < 200` → `verdict=cut`，30 天内样本不足，停止该轮数据池结论；
- 其余 → `verdict=collecting`。

## 隐私
- 前端贡献开关默认关闭，试玩模式不显示上传。
- 用户必须手动勾选并二次确认。
- 上传内容是去标识化分数与结构化元数据，开放文本不进入汇总。
- `data/contributions.jsonl` 不入库，由 `.gitignore` 排除。

## 验证命令
```bash
python3 -m unittest discover -s tests -p 'test_datapool.py' -v
node tests/test_datapool_js.js
python3 -m py_compile serve.py
```

边界断言现读位置：`tests/test_datapool.py` 中 `test_cut_at_199`、`test_dedup_and_summary_threshold`、`test_ready_at_500`。
