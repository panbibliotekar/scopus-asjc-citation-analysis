"""Reproduce Figure 3 from manuscript Table 2 and publisher metadata.
Download journal_citescore_2025_zenodo.csv from
https://doi.org/10.5281/zenodo.24541791
Usage: python scripts/figure_3_publisher_overlap.py path/to/journal_citescore_2025_zenodo.csv
Requires pandas and matplotlib.
"""
import pandas as pd
import matplotlib.pyplot as plt
from pathlib import Path
import sys
# Journal-level values from manuscript Table 2, in percent.
rows=[('Banks and Bank Systems',43.18,88.51,20.83,41.18),('Carpathian Mathematical Publications',48.53,91.39,48.53,91.39),('Environmental Economics',59.28,85.05,21.62,54.23),('History of Science and Technology',14.17,39.17,11.67,39.17),('Innovative Marketing',42.55,80.74,21.31,45.20),('Investment Management and Financial Innovations',50.51,70.52,15.43,41.77),('Journal of Edge Computing',40.11,72.32,40.11,72.32),('Knowledge and Performance Management',38.50,80.36,26.10,64.08),('Mining of Mineral Deposits',39.95,67.03,39.95,67.03),('Problems and Perspectives in Management',37.02,77.03,17.01,49.24),('Psycholinguistics',35.53,69.74,33.33,64.47),('Public and Municipal Finance',60.71,90.38,33.79,59.62),('Ukrainian Geographical Journal',38.33,67.50,0,3.33),('Ukrainian Journal of Physical Optics',45.34,68.84,45.34,68.84),('Ukrainian Numismatic Annual',92.86,100,92.86,100)]
metrics=['Exact all','Broad all','Exact Q1','Broad Q1']
df=pd.DataFrame(rows,columns=['Titles']+metrics)
source=Path(sys.argv[1]) if len(sys.argv)>1 else Path('data/journal_citescore_2025_zenodo.csv')
df=df.merge(pd.read_csv(source)[['Titles','Publisher']],on='Titles',validate='one_to_one')
assert len(df)==15
df['BP']=df.Publisher.eq('LLC CPC Business Perspectives')
assert df.BP.sum()==7
print(df.groupby('BP')[metrics].median())
fig,axes=plt.subplots(1,4,figsize=(13,5.8),sharey=True)
for ax,m in zip(axes,metrics):
    for x,bp,color in [(0,True,'#2166AC'),(1,False,'#D95F02')]:
        vals=sorted(df.loc[df.BP.eq(bp),m]); offsets=[]
        # deterministic small horizontal offsets to distinguish close points
        for i,v in enumerate(vals):
            candidates=[0,-.09,.09,-.18,.18,-.27,.27]
            offsets.append(next((o for o in candidates if all(abs(v-w)>3.2 or abs(o-p)>.075 for w,p in zip(vals[:i],offsets))),0))
        ax.scatter([x+o for o in offsets],vals,s=48,color=color,zorder=3,clip_on=False)
        ax.hlines(pd.Series(vals).median(),x-.29,x+.29,color='0.18',linewidth=2.5,zorder=4)
    ax.set_title(m.replace(' all','\nAll ASJC').replace(' Q1','\nQ1 categories'),fontsize=13)
    ax.set_xticks([0,1],['BP','Other'],fontsize=11)
    ax.set_xlim(-.48,1.48); ax.set_ylim(0,100); ax.set_yticks(range(0,101,20)); ax.grid(axis='y',color='0.88',linestyle=':'); ax.set_axisbelow(True)
    for s in ['top','right','left']: ax.spines[s].set_visible(False)
    ax.tick_params(axis='both',length=0,pad=8)
axes[0].set_ylabel('Share of citing documents (%)',fontsize=12)
from matplotlib.lines import Line2D
fig.legend(handles=[Line2D([],[],marker='o',linestyle='',color='#2166AC',label='Business Perspectives (n = 7)'),Line2D([],[],marker='o',linestyle='',color='#D95F02',label='Other publishers (n = 8)'),Line2D([],[],color='0.18',lw=2.5,label='Median')],loc='lower center',ncol=3,frameon=False,fontsize=11)
fig.subplots_adjust(left=.075,right=.98,top=.86,bottom=.19,wspace=.22)
for ext in ['pdf','png']: fig.savefig('Figure_3_publisher_overlap.'+ext,dpi=300,bbox_inches='tight')
