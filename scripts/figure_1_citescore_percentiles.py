"""Reproduce revised Figure 1 using the Zenodo dataset.

Download journal_citescore_2025_zenodo.csv from
https://doi.org/10.5281/zenodo.24541791
Usage: python scripts/figure_1_citescore_percentiles.py path/to/journal_citescore_2025_zenodo.csv
Requires pandas and matplotlib.
"""
import pandas as pd
import matplotlib.pyplot as plt
import textwrap
from pathlib import Path
import sys

source = Path(sys.argv[1]) if len(sys.argv)>1 else Path('data/journal_citescore_2025_zenodo.csv')
df = pd.read_csv(source).sort_values(['Worst percentile','Best percentile','Titles']).reset_index(drop=True)
y = range(len(df))
fig, ax = plt.subplots(figsize=(12,8))
ax.hlines(y, df['Worst percentile'], df['Best percentile'], color='0.60', linewidth=1.8)
ax.scatter(df['Worst percentile'], y, color='#2166AC', s=65, label='Lowest percentile', zorder=3)
ax.scatter(df['Best percentile'], y, color='#D95F02', s=65, label='Highest percentile', zorder=4)
ax.set_yticks(list(y), ['\n'.join(textwrap.wrap(t, 38)) for t in df.Titles], fontsize=11)
ax.invert_yaxis()
ax.set_xlim(0,100)
ax.set_xticks(range(0,101,10))
ax.set_xlabel('CiteScore 2025 percentile', fontsize=12)
ax.axvline(75, color='0.4', linestyle='--', linewidth=1.2, label='Q1 threshold')
ax.grid(axis='x', color='0.88', linestyle=':')
ax.set_axisbelow(True)
for spine in ['top','right','left']: ax.spines[spine].set_visible(False)
ax.tick_params(axis='y', length=0, pad=8)
h,l=ax.get_legend_handles_labels(); ax.legend([h[i] for i in [0,1,2]],[l[i] for i in [0,1,2]],loc='upper center',bbox_to_anchor=(0.5,-0.09),ncol=3,frameon=False)
fig.subplots_adjust(left=0.37,right=0.96,top=0.97,bottom=0.15)
fig.savefig('Figure_1_final.pdf',bbox_inches='tight')
fig.savefig('Figure_1_final.png',dpi=300,bbox_inches='tight')
