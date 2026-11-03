"""Reproduce Figure 1 for the journal classification anomalies manuscript.

Values transcribed from manuscript Tables 1; verify against source data before publication.
Requires: matplotlib, pandas.
"""
import pandas as pd
import matplotlib.pyplot as plt

data = [
    ("Banks and Bank Systems", 44, 85),
    ("Carpathian Mathematical Publications", 80, 80),
    ("Environmental Economics", 48, 90),
    ("History of Science and Technology", 74, 91),
    ("Innovative Marketing", 45, 86),
    ("Investment Management and Financial Innovations", 55, 81),
    ("Journal of Edge Computing", 76, 82),
    ("Knowledge and Performance Management", 47, 89),
    ("Mining of Mineral Deposits", 78, 85),
    ("Problems and Perspectives in Management", 53, 86),
    ("Psycholinguistics", 28, 79),
    ("Public and Municipal Finance", 53, 80),
    ("Ukrainian Geographical Journal", 25, 76),
    ("Ukrainian Journal of Physical Optics", 88, 88),
    ("Ukrainian Numismatic Annual", 77, 87),
]
df = pd.DataFrame(data, columns=["Journal", "Lowest", "Highest"])

fig, ax = plt.subplots(figsize=(18, 12))
y = range(len(df))
for i, row in df.iterrows():
    ax.plot([row["Lowest"], row["Highest"]], [i, i],
            color="0.60", linewidth=2, zorder=1)
ax.scatter(df["Lowest"], y, color="#2166AC", s=100,
           label="Lowest percentile", zorder=3)
ax.scatter(df["Highest"], y, color="#D95F02", s=100,
           label="Highest percentile", zorder=4)
ax.set_yticks(list(y))
ax.set_yticklabels(df["Journal"], fontsize=20, fontweight="medium")
ax.invert_yaxis()
ax.set_xlim(20, 100)
ax.set_xticks(range(20, 101, 10))
ax.set_xlabel("CiteScore 2025 percentile", fontsize=20, labelpad=12)
ax.tick_params(axis="x", labelsize=16)
ax.axvline(75, color="0.45", linestyle="--", linewidth=1.2, alpha=0.7)
ax.grid(axis="x", color="0.88", linestyle=":", linewidth=0.9)
ax.set_axisbelow(True)
for spine in ["top", "right", "left"]:
    ax.spines[spine].set_visible(False)
ax.tick_params(axis="y", length=0, pad=12)
ax.legend(loc="upper center", bbox_to_anchor=(0.5, -0.08),
          ncol=2, frameon=False, fontsize=16)
fig.subplots_adjust(left=0.51, right=0.97, top=0.97, bottom=0.15)
fig.savefig("Figure_1_CiteScore_percentiles.pdf", bbox_inches="tight")
fig.savefig("Figure_1_CiteScore_percentiles.png",
            dpi=600, bbox_inches="tight")
plt.show()
