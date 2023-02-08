# -*- coding: utf-8 -*-
"""
Spyder Editor

This is a temporary script file.
"""


import pandas as pd #熊猫很可爱，被治愈了。 
import matplotlib.pyplot as plt
import numpy as np
import scipy.stats as stats


IO = 'Christmas Movie Genre.xls'  
df = pd.read_excel(io=IO)
df_allmelt = df.melt(id_vars =['imdb_rating'], value_vars =['Main_Genre','Second_Genre','Third_Genre'],  var_name ='Variable_column', value_name ='Genre')
df_all = df_allmelt.loc[:,['imdb_rating','Genre']]
df_all_grouped = df_all.groupby(['Genre'])
df_fr = pd.DataFrame(index=[])

for name, group in df_all_grouped :
    if name == 'Comedy' :
      df_fr = df_fr.append(group)
      print(name)
    elif name == 'Drama':
        df_fr = df_fr.append(group)
        print(name)
    elif name == 'Family':
        df_fr = df_fr.append(group)
        print(name)
    elif name == 'Fantasy':
        df_fr = df_fr.append(group)
        print(name)
    elif name == 'Romance':
        df_fr = df_fr.append(group)
        print(name)
    else:
      group = group.replace(to_replace = name, value ="others",regex=True)
      df_fr=df_fr.append(group)    
 
print(df_fr)

df_main_grouped_2 = df_fr.groupby(['Genre'])
df_fr_2 = pd.DataFrame(index=[])

for name, group in df_main_grouped_2 :
    
    r = group['bins'] = pd.cut(x=group['imdb_rating'], bins=[0, 4.0, 6.0, 8.0, 10])
    fr_r = r.value_counts()
    fr_r = fr_r.rename(name)
    df_fr_2=df_fr_2.append(fr_r)
    
print(df_fr_2)

tick_label = df_fr_2.index
x = np.arange(len(tick_label))

y1 = df_fr_2.iloc[:,0]
y2 = df_fr_2.iloc[:,1]
y3 = df_fr_2.iloc[:,2]
y4 = df_fr_2.iloc[:,3]

plt.bar(x,y1,width=0.4,label='(4.0, 6.0]',color='#9370DB',zorder=5)
plt.bar(x,y2,width=0.4,bottom=y1,label='(6.0, 8.0]',color='#000080',zorder=5)
plt.bar(x,y3,width=0.4,bottom=y2,label='(8.0, 10.0]',color='#00bfc4',zorder=5)
plt.bar(x,y4,width=0.4,bottom=y3,label='(0.0, 4.0]',color='#f9766e',zorder=5)

plt.tick_params(axis='x',length=1)
plt.xticks(x , tick_label, rotation = 70)
plt.xlabel('Main_Genre',fontsize=12)
plt.ylabel('IMDB_Rating',fontsize=12)
plt.grid(axis='y',alpha=0.5,ls='--')
plt.legend(frameon=False)
plt.tight_layout()
plt.savefig('bar1.png', dpi=600)
plt.show()

print(stats.chi2_contingency(df_fr_2))