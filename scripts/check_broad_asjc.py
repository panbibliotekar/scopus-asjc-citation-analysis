#!/usr/bin/env python3
"""Broad ASJC area robustness check. Reads local CSVs; writes local CSVs only.

ASJC broad areas are identified by the first two digits of four-digit ASJC codes.
A citing record counts at most once per measure; source multi-assignment is allowed.
"""
import argparse
import csv
from collections import Counter, defaultdict
from pathlib import Path
from build_manuscript_table import Q1_2025

def read(path):
    with path.open(encoding="utf-8-sig", newline="") as f:
        return list(csv.DictReader(f))

def codes(value):
    return {x.strip() for x in value.split("|") if x.strip()}

def broad(items):
    return {c[:2] for c in items if len(c) == 4 and c.isdigit()}

def write(path, rows):
    path.parent.mkdir(parents=True, exist_ok=True)
    with path.open("w", encoding="utf-8-sig", newline="") as f:
        writer = csv.DictWriter(f, fieldnames=list(rows[0]))
        writer.writeheader()
        writer.writerows(rows)

def run(summary_path, log_path, output_dir):
    summaries = read(summary_path)
    logs = read(log_path)
    grouped = defaultdict(list)
    for record in logs:
        grouped[record["target_source_id"]].append(record)
    assert len(summaries) == 15, "Expected 15 journals"
    comparisons, distributions = [], []
    for item in summaries:
        sid = item["source_id"]
        target = codes(item["target_asjc_codes"])
        q1 = set(Q1_2025[sid])
        assert q1 <= target, f"Q1 code mismatch for {item['journal_title']}"
        target_broad, q1_broad = broad(target), broad(q1)
        eligible = [r for r in grouped[sid] if r["match_status"] == "matched" and codes(r["asjc_codes"])]
        n = len(eligible)
        assert n == int(item["matched_with_asjc"]), f"Denominator mismatch: {sid}"
        counts = Counter()
        area_counts = Counter()
        for record in eligible:
            citing = codes(record["asjc_codes"])
            citing_broad = broad(citing)
            counts["exact_any"] += bool(citing & target)
            counts["broad_any"] += bool(citing_broad & target_broad)
            counts["exact_q1"] += bool(citing & q1)
            counts["broad_q1"] += bool(citing_broad & q1_broad)
            area_counts.update(citing_broad)
        assert counts["exact_any"] == int(item["any_category_overlap_n"]), f"Exact overlap mismatch: {sid}"
        comparison = {"journal": item["journal_title"], "source_id": sid, "n": n,
                      "target_broad_areas": "|".join(sorted(target_broad)),
                      "q1_broad_areas": "|".join(sorted(q1_broad))}
        for metric in ("exact_any", "broad_any", "exact_q1", "broad_q1"):
            comparison[metric + "_n"] = counts[metric]
            comparison[metric + "_pct"] = round(100 * counts[metric] / n, 2) if n else ""
        comparisons.append(comparison)
        for area, number in sorted(area_counts.items()):
            distributions.append({"journal": item["journal_title"], "source_id": sid,
                                  "broad_area": area, "citing_documents": number,
                                  "denominator": n, "percent": round(100 * number / n, 2) if n else "",
                                  "is_target_broad_area": area in target_broad,
                                  "is_q1_broad_area": area in q1_broad})
    write(output_dir / "broad_asjc_comparison_15.csv", comparisons)
    write(output_dir / "broad_asjc_group_distribution.csv", distributions)
    print(f"Analyzed {len(comparisons)} journals, {sum(x['n'] for x in comparisons)} eligible records.")
    print(f"Saved to {output_dir}")

if __name__ == "__main__":
    parser = argparse.ArgumentParser()
    parser.add_argument("--summary", type=Path, default=Path("output/all_15_summary.csv"))
    parser.add_argument("--log", type=Path, default=Path("output/all_15_matching_log.csv"))
    parser.add_argument("--output-dir", type=Path, default=Path("output"))
    args = parser.parse_args()
    run(args.summary, args.log, args.output_dir)
