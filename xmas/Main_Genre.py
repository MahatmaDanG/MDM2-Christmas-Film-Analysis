# -*- coding: utf-8 -*-
"""
Created on Wed Feb 15 17:19:18 2023

@author: hanwe
"""

import pandas as pd #熊猫很可爱。被治愈了。 
import matplotlib.pyplot as plt
import numpy as np
import scipy.stats as stats

df_genre = pd.read_csv('movies_genre.csv')  #read genre table
df_profit = pd.read_csv('movies_Worldwide_Net_Revenue.csv')  #read profit table

df_fliter = df_genre[df_genre['movie_title'].isin(df_profit['Movie'])]

df_genre = df_genre[df_genre['movie_title'].isin(df_fliter['movie_title'])] #filtering the genres data
df_profit = df_profit[df_profit['Movie'].isin(df_fliter['movie_title'])] #filtering the profits data

df_profit.drop_duplicates('Movie',inplace = True)
df_genre.drop_duplicates('movie_title',inplace = True) # remove the repeated data


df_genre = df_genre.sort_values(by=['movie_title'])
df_profit = df_profit.sort_values(by=['Movie'])
df_genre.reset_index(drop=True, inplace=True)
df_profit.reset_index(drop=True, inplace=True) #Align the orders and reset the indexes

Worldwide_Net_Revenue=df_profit['Worldwide Net Revenue']
df_genre['Worldwide_Net_Revenue'] = Worldwide_Net_Revenue
df_fd = df_genre  #got the final dataframe

df_fd_cal = df_fd.loc[:,['Worldwide_Net_Revenue','Main Genre']] #got the dataframe used in calculation

df_grouped = df_fd_cal.groupby(['Main Genre'])#count the frequency of films seperately by 'Main Genre' groups
df_fr = pd.DataFrame(index=[])

for name, group in df_grouped :
    
    r = group['bins'] = pd.cut(x=group['Worldwide_Net_Revenue'], bins=[-1000000000, 0, 60000000, 70000000, 10000000000])
    fr_r = r.value_counts()
    fr_r = fr_r.rename(name)
    df_fr=df_fr.append(fr_r)
#60000000 is the average of all the films, 70000000 is the average of the selected films
tick_label = df_fr.index
x = np.arange(len(tick_label))

y1 = df_fr.iloc[:,0]
y2 = df_fr.iloc[:,1]
y3 = df_fr.iloc[:,2]
y4 = df_fr.iloc[:,3]

plt.bar(x,y1,width=0.4,label='(-40000000, 0]',color='#9370DB',zorder=5)
plt.bar(x,y2,width=0.4,bottom=y1,label='(0, 60000000]',color='#000080',zorder=5)
plt.bar(x,y3,width=0.4,bottom=y1,label='(60000000, 70000000]',color='#00bfc4',zorder=5)
plt.bar(x,y4,width=0.4,bottom=y1,label='(70000000, 10000000000]',color='#f9766e',zorder=5)

plt.tick_params(axis='x',length=1)
plt.xticks(x , tick_label, rotation = 90)
plt.xlabel('Genre',fontsize=6)
plt.ylabel('Worldwide_Net_Revenue',fontsize=12)
plt.grid(axis='y',alpha=0.5,ls='--')
plt.legend(frameon=False)
plt.tight_layout()
plt.savefig('bar3.png', dpi=600)
plt.show()

print(stats.chi2_contingency(df_fr))