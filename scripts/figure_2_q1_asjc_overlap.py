"""Reproduce Figure 2 for the journal classification anomalies manuscript.

Values transcribed from manuscript Tables 2; verify against source data before publication.
Requires: matplotlib, pandas.
"""
import pandas as pd
import matplotlib.pyplot as plt

data = [
    ("Banks and Bank Systems", 20.83, 41.18),
    ("Carpathian Mathematical Publications", 48.53, 91.39),
    ("Environmental Economics", 21.62, 54.23),
    ("History of Science and Technology", 11.67, 39.17),
    ("Innovative Marketing", 21.31, 45.2),
    ("Investment Management and Financial Innovations", 15.43, 41.77),
    ("Journal of Edge Computing", 40.11, 72.32),
    ("Knowledge and Performance Management", 26.1, 64.08),
    ("Mining of Mineral Deposits", 39.95, 67.03),
    ("Problems and Perspectives in Management", 17.01, 49.24),
    ("Psycholinguistics", 33.33, 64.47),
    ("Public and Municipal Finance", 33.79, 59.62),
    ("Ukrainian Geographical Journal", 0, 3.33),
    ("Ukrainian Journal of Physical Optics", 45.34, 68.84),
    ("Ukrainian Numismatic Annual", 92.86, 100),
]
df = pd.DataFrame(data, columns=["Journal", "Exact_Q1", "Broad_Q1"])

fig, ax = plt.subplots(figsize=(18, 12))
y = range(len(df))
for i, row in df.iterrows():
    ax.plot([row["Exact_Q1"], row["Broad_Q1"]], [i, i],
            color="0.60", linewidth=2, zorder=1)
ax.scatter(df["Exact_Q1"], y, color="#2166AC", s=100,
           label="Exact Q1 overlap", zorder=3)
ax.scatter(df["Broad_Q1"], y, color="#D95F02", s=100,
           label="Broad Q1 overlap", zorder=4)
ax.set_yticks(list(y))
ax.set_yticklabels(df["Journal"], fontsize=20, fontweight="medium")
ax.invert_yaxis()
ax.set_xlim(0, 100)
ax.set_xticks(range(0, 101, 10))
ax.set_xlabel("Share of citing documents (%)", fontsize=20, labelpad=12)
ax.tick_params(axis="x", labelsize=16)
ax.grid(axis="x", color="0.88", linestyle=":", linewidth=0.9)
ax.set_axisbelow(True)
for spine in ["top", "right", "left"]:
    ax.spines[spine].set_visible(False)
ax.tick_params(axis="y", length=0, pad=12)
ax.legend(loc="upper center", bbox_to_anchor=(0.5, -0.08),
          ncol=2, frameon=False, fontsize=16)
fig.subplots_adjust(left=0.51, right=0.97, top=0.97, bottom=0.15)
fig.savefig("Figure_2_Q1_ASJC_overlap.pdf", bbox_inches="tight")
fig.savefig("Figure_2_Q1_ASJC_overlap.png",
            dpi=600, bbox_inches="tight")
plt.show()
