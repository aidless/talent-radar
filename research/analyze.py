#!/usr/bin/env python3
"""30 天真人对验证：只读结构化列，输出观察量，不宣称信度/效度认证。"""
import csv
import json
import math
import sys

STRUCTURED = ("pid", "day", "self_rating", "behavior_tag", "third_party_agreement", "drop_reason")


def _pearson(xs, ys):
    n = len(xs)
    if n < 2:
        return None
    mx, my = sum(xs) / n, sum(ys) / n
    num = sum((a - mx) * (b - my) for a, b in zip(xs, ys))
    dx = sum((a - mx) ** 2 for a in xs)
    dy = sum((b - my) ** 2 for b in ys)
    if dx == 0 or dy == 0:
        return 0.0
    return num / math.sqrt(dx * dy)


def analyze(csv_path):
    with open(csv_path, newline="", encoding="utf-8") as f:
        rows = [{k: r.get(k, "") for k in STRUCTURED} for r in csv.DictReader(f)]
    pids = sorted({r["pid"] for r in rows if r["pid"]})
    n = len(pids)
    by_pid = {}
    for r in rows:
        try:
            r["day"] = int(r["day"])
            r["self_rating"] = float(r["self_rating"])
        except (ValueError, TypeError):
            continue
        by_pid.setdefault(r["pid"], {})[r["day"]] = r
    d0 = {}
    d30 = {}
    for pid, days in by_pid.items():
        if 0 in days:
            d0[pid] = days[0]["self_rating"]
        if 30 in days:
            d30[pid] = days[30]["self_rating"]
    pairs = [(d0[p], d30[p]) for p in d0 if p in d30]
    retest = _pearson([a for a, _ in pairs], [b for _, b in pairs])
    gaps = [d0[p] - d30[p] for p in d0 if p in d30]
    gap_mean = (sum(gaps) / len(gaps)) if gaps else 0.0
    abs_sorted = sorted(abs(g) for g in gaps)
    if abs_sorted:
        idx = min(len(abs_sorted) - 1, int(math.ceil(0.9 * len(abs_sorted))) - 1)
        p90 = abs_sorted[idx]
    else:
        p90 = 0.0
    agreements = [1 if r["third_party_agreement"] == "1" else 0
                  for r in rows if r["third_party_agreement"] in ("0", "1")]
    agreement = sum(agreements) / len(agreements) if agreements else None
    retained = len(d30)
    drop_rate = 1 - retained / n if n else 1.0
    confidence = "provisional" if (20 <= n <= 30 and retained >= n * 0.5) else "insufficient"
    return {
        "n": n, "retained_day30": retained, "retest_corr": retest,
        "self_beh_gap_mean": round(gap_mean, 4), "gap_abs_p90": round(p90, 4),
        "third_party_agreement": agreement, "drop_rate": round(drop_rate, 4),
        "confidence": confidence,
    }


if __name__ == "__main__":
    print(json.dumps(analyze(sys.argv[1]), ensure_ascii=False, indent=2))
