#!/usr/bin/env python3
"""Create a manuscript table from local batch outputs; never upload input data.

Q1 codes transcribed from the project's CiteScore 2025 category table.
A citing record is counted once per overlap measure, even if it has multiple ASJC codes.
"""
from pathlib import Path
from collections import defaultdict
import csv
import argparse

Q1_2025 = {
    "21101021440": ("1202", "1204", "1209", "3302"),
    "21101071896": ("3308",),
    "21101071123": ("3301", "3308"),
    "11400153315": ("3107",),
    "21101196159": ("1202", "1204", "1209", "3302"),
    "19700170105": ("3301", "3308"),
    "21100899296": ("3301", "3308", "3315"),
    "21100407655": ("3301", "3308"),
    "21100914192": ("1906", "1909", "2200"),
    "21101295952": ("1701", "1702", "1705", "1708"),
    "19700182325": ("3308",),
    "21101049551": ("3308",),
    "21100925710": ("2600",),
    "21100967057": ("1203", "3310"),
    "21100905026": ("1207",),
}

def read_csv(path):
    with path.open(encoding="utf-8-sig", newline="") as f:
        return list(csv.DictReader(f))

def build(summary_path, log_path, output_path):
    summaries = read_csv(summary_path)
    logs = read_csv(log_path)
    assert len(summaries) == len(Q1_2025) == 15, "Expected exactly 15 target journals"
    grouped = defaultdict(list)
    for r in logs:
        grouped[r["target_source_id"]].append(r)
    rows = []
    for s in summaries:
        source_id = s["source_id"]
        q1 = set(Q1_2025[source_id])
        target = set(s["target_asjc_codes"].split("|"))
        assert q1 <= target, f"Q1 codes absent from target ASJC for {s['journal_title']}"
        matched = [r for r in grouped[source_id] if r["match_status"] == "matched" and r["asjc_codes"]]
        n = len(matched)
        assert n == int(s["matched_with_asjc"]), f"Denominator mismatch: {s['journal_title']}"
        any_n = sum(bool(set(r["asjc_codes"].split("|")) & target) for r in matched)
        q1_n = sum(bool(set(r["asjc_codes"].split("|")) & q1) for r in matched)
        assert any_n == int(s["any_category_overlap_n"]), f"Any-overlap mismatch: {s['journal_title']}"
        rows.append({
            "Journal": s["journal_title"],
            "Citing records": int(s["citing_records"]),
            "Analyzed citing records (n)": n,
            "Any ASJC overlap (n)": any_n,
            "Any ASJC overlap (%)": round(100 * any_n / n, 2) if n else "",
            "Q1 ASJC overlap (n)": q1_n,
            "Q1 ASJC overlap (%)": round(100 * q1_n / n, 2) if n else "",
            "Q1 ASJC codes (CiteScore 2025)": "|".join(sorted(q1)),
        })
    output_path.parent.mkdir(parents=True, exist_ok=True)
    with output_path.open("w", encoding="utf-8-sig", newline="") as f:
        writer = csv.DictWriter(f, fieldnames=list(rows[0]))
        writer.writeheader()
        writer.writerows(rows)
    return rows

if __name__ == "__main__":
    parser = argparse.ArgumentParser()
    parser.add_argument("--summary", type=Path, default=Path("output/all_15_summary.csv"))
    parser.add_argument("--log", type=Path, default=Path("output/all_15_matching_log.csv"))
    parser.add_argument("--output", type=Path, default=Path("output/manuscript_table.csv"))
    args = parser.parse_args()
    rows = build(args.summary, args.log, args.output)
    print(f"Saved {len(rows)} journals to {args.output}")
