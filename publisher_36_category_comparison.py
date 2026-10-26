"""Compare Law and Social Sciences (miscellaneous) in citing environments.

Input: all_15_asjc_frequencies.csv (not included in repository).
Outputs: publisher_36_category_all15.csv and
         publisher_36_category_group_summary.csv (generated locally).
"""
from pathlib import Path
import pandas as pd

base = Path(__file__).resolve().parent
freq = pd.read_csv(base / "all_15_asjc_frequencies.csv")
bp = {
    "Environmental Economics",
    "Knowledge and Performance Management",
    "Problems and Perspectives in Management",
    "Innovative Marketing",
    "Banks and Bank Systems",
    "Investment Management and Financial Innovations",
    "Public and Municipal Finance",
}
rows = []
for journal, sub in freq.groupby("journal_title"):
    den = int(sub.denominator.iloc[0])
    assert sub.denominator.nunique() == 1
    row = {
        "journal": journal,
        "group": "Business Perspectives" if journal in bp else "Other publishers",
        "denominator": den,
    }
    for code, slug in [(3308, "law"), (3301, "ss_misc")]:
        values = sub.loc[sub.asjc_code.eq(code), "citing_documents"]
        assert len(values) <= 1
        n = int(values.iloc[0]) if len(values) else 0
        row[f"{slug}_n"] = n
        row[f"{slug}_pct"] = round(100 * n / den, 4)
    rows.append(row)

df = pd.DataFrame(rows).sort_values(["group", "journal"])
assert len(df) == 15 and (df.group == "Business Perspectives").sum() == 7
df.to_csv(base / "publisher_36_category_all15.csv", index=False)

summary_rows = []
for group, subset in [("All journals", df), *list(df.groupby("group"))]:
    for slug in ["law", "ss_misc"]:
        values = subset[f"{slug}_pct"]
        summary_rows.append({
            "group": group,
            "category": slug,
            "journals": len(subset),
            "mean_pct": round(values.mean(), 2),
            "median_pct": round(values.median(), 2),
            "min_pct": round(values.min(), 2),
            "max_pct": round(values.max(), 2),
            "pooled_n": int(subset[f"{slug}_n"].sum()),
            "pooled_denominator": int(subset.denominator.sum()),
            "pooled_pct": round(
                100 * subset[f"{slug}_n"].sum() / subset.denominator.sum(), 2
            ),
        })
summary = pd.DataFrame(summary_rows)
summary.to_csv(base / "publisher_36_category_group_summary.csv", index=False)
print(summary.to_string(index=False))

# ASJC categories are nonexclusive; do not add category percentages.
