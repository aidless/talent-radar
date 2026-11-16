# 真人验证研究目录

这里记录 30 天真人使用的观察量，不是心理测评认证。

## 文件
- `recruit.md`：20–30 人招募文案、纳入排除、知情同意、时间线。
- `feedback-form.md`：每日 1 题 + 第 0/14/30 天量表与 CSV 模板。
- `analyze.py`：只读结构化列，输出 `n / retained_day30 / retest_corr / self_beh_gap_mean / gap_abs_p90 / third_party_agreement / drop_rate / confidence`。

## 判据
- 样本 20–30 人；30 天留存 ≥50% → `confidence=provisional`。
- 样本 <20 或留存 <50% → `confidence=insufficient`，只能写「观察不足，未做结论」。
- `retest_corr` 是第 0 天与第 30 天自评的 Pearson 相关；配对数 <2 时为 null。
- `third_party_agreement` 是第三方观察标记=1 的占比，只反映标记比例，不证明客观正确。

## 写作口径（销售页与面试叙事）
- 可以写：「我做了 20–30 人、30 天的真实使用记录，观察到自评—行为差距与第三方标记的初步一致性，样本与留存量见 README。」
- 只写实测数与口径；不写「信度高」「效度好」「科学测评认证」。
- 面试时主动说明这是产品验证而非心理测量学研究，短板是样本小、无对照组、自评仍带主观性。
