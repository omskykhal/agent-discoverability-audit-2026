"""Quick stats from results.csv for the findings report."""

import csv
from collections import Counter
from pathlib import Path

R = Path(__file__).resolve().parent.parent / "data" / "results.csv"

with open(R, encoding="utf-8") as f:
    rows = list(csv.DictReader(f))

n = len(rows)
print(f"Total scanned: {n}\n")

scores = [int(r["total_score"]) for r in rows]
avg = sum(scores) / n
print(f"Average score: {avg:.2f} / 100")
print(f"Max:           {max(scores)}")
print(f"Min:           {min(scores)}")
print(f"Median:        {sorted(scores)[n // 2]}\n")

tier_counts = Counter(r["tier"] for r in rows)
print("Tier distribution:")
for tier, count in tier_counts.most_common():
    print(f"  {tier:25s} {count:3d}  ({count*100/n:.0f}%)")
print()

CHECK_NAMES = [
    "1  llms.txt",
    "2  skill.md",
    "3  ai-agent.json",
    "4  agent-card.json (A2A)",
    "5  ucp manifest",
    "6  openapi/swagger",
    "7  capability clarity",
    "8  i/o schema",
    "9  pricing metadata",
    "10 contact/auth/ratelimit",
]

print("Per-check pass rates:")
for i in range(1, 11):
    col = f"check{i}_passed"
    passes = sum(1 for r in rows if r[col] == "Y")
    print(f"  {CHECK_NAMES[i-1]:30s} {passes:3d}/{n}  ({passes*100/n:.0f}%)")
print()

print("Top 10 scorers:")
top = sorted(rows, key=lambda r: -int(r["total_score"]))[:10]
for r in top:
    print(f"  {int(r['total_score']):3d}  {r['name']:25s}  ({r['category']})")
print()

print("Score distribution:")
buckets = Counter()
for s in scores:
    if s == 0:
        buckets["0"] += 1
    elif s < 20:
        buckets["1-19"] += 1
    elif s < 40:
        buckets["20-39"] += 1
    elif s < 60:
        buckets["40-59"] += 1
    elif s < 80:
        buckets["60-79"] += 1
    else:
        buckets["80+"] += 1
for b in ["0", "1-19", "20-39", "40-59", "60-79", "80+"]:
    print(f"  {b:6s} {buckets.get(b, 0):3d}  ({buckets.get(b, 0)*100/n:.0f}%)")
print()

print("Category breakdown (avg score):")
cat_data = {}
for r in rows:
    cat = r["category"]
    cat_data.setdefault(cat, []).append(int(r["total_score"]))
for cat, sc in sorted(cat_data.items(), key=lambda x: -sum(x[1])/len(x[1])):
    print(f"  {cat:18s} avg={sum(sc)/len(sc):4.1f}  n={len(sc)}")
