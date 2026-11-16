# 天赋雷达 · 30 天反馈表模板

复制下方表头建立 `feedback.csv`，每行一条记录。`open_text` 列只在本机保留，上传前删除或留空。

```csv
pid,day,self_rating,behavior_tag,third_party_agreement,drop_reason,open_text
P01,0,4,structured_demo,1,,今天我主动做了一次梳理
P01,1,4,positive,0,,
P01,14,3,mixed,1,,
P01,30,4,positive,1,,
```

## 字段说明
| 字段 | 取值 | 说明 |
|---|---|---|
| pid | 匿名 ID | 如 P01，不含真实身份 |
| day | 0 / 1–29 / 14 / 30 | 第几天；0=前测，14=中测，30=后测 |
| self_rating | 1–5 整数 | 当天「我在天赋方向上行动了」的自评 |
| behavior_tag | positive / mixed / negative / none | 当天行为性质的粗标签 |
| third_party_agreement | 0 / 1 / 空 | 可信任的朋友是否也观察到相同倾向 |
| drop_reason | 文本（可选） | 退出原因；分析脚本只读是否非空 |
| open_text | 自由文本 | 只在本机保留，不上传 |

## 每日 1 题
> 今天有没有一件「不用别人催、你自己就想做，而且做起来比别人顺手」的事？写一句具体事件，再选一个 behavior_tag。

## 第 0/14/30 天量表
> 回想过去两周，你在自己识别出的天赋方向上主动行动的频率：1=几乎没有，5=几乎每天。选一个数字填 self_rating。

## 汇总命令
```bash
python3 talent-radar/research/analyze.py talent-radar/research/feedback.csv
```
输出字段见 `research/README.md`；样本不足 20 或 30 天留存低于 50% 时 confidence=insufficient，只作参考。
