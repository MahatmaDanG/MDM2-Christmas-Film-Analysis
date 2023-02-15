# -*- coding: utf-8 -*-
"""
Created on Tue Feb 14 23:03:32 2023

@author: hanwe
"""

import pandas as pd #熊猫很可爱。被治愈了。 
import matplotlib.pyplot as plt
import numpy as np
import scipy.stats as stats


df_xmas =  pd.read_csv('christmas_movies.csv')  #read xmas films table
df_profit = pd.read_csv('movies_Worldwide_Net_Revenue.csv')  #read profit table
df_genre = pd.read_csv('movies_genre.csv')  #read genre table


df_fliter = df_xmas[df_xmas['title'].isin(df_genre['movie_title'])]
df_fliter = df_fliter[df_fliter['title'].isin(df_profit['Movie'])]
df_fliter = df_xmas[df_xmas['title'].isin(df_fliter['title'])]  #make a fliter dataframe to list the xmas films which has data in other dataframes

df_genre = df_genre[df_genre['movie_title'].isin(df_fliter['title'])] #filtering the genres data
df_profit = df_profit[df_profit['Movie'].isin(df_fliter['title'])] #filtering the profits data

df_profit.drop_duplicates('Movie',inplace = True)
df_genre.drop_duplicates('movie_title',inplace = True) # remove the repeated data

df_genre = df_genre.sort_values(by=['movie_title'])
df_profit = df_profit.sort_values(by=['Movie'])
df_genre.reset_index(drop=True, inplace=True)
df_profit.reset_index(drop=True, inplace=True) #Align the orders and reset the indexes

Worldwide_Net_Revenue=df_profit['Worldwide Net Revenue']
df_genre['Worldwide_Net_Revenue'] = Worldwide_Net_Revenue
df_fd = df_genre  #got the final dataframe

df_melt = df_fd.melt(id_vars =['Worldwide_Net_Revenue'], value_vars =['Main Genre','2nd Genre','3rd Genre','4th Genre','5th Genre','6th Genre','7th Genre'],  var_name ='Variable_column', value_name ='Genre')
df_fd_cal = df_melt.loc[:,['Worldwide_Net_Revenue','Genre']] #got the dataframe used in calculation

df_grouped = df_fd_cal.groupby(['Genre'])#count the frequency of films seperately by 'genre' groups
df_fr = pd.DataFrame(index=[])

for name, group in df_grouped :
    
    r = group['bins'] = pd.cut(x=group['Worldwide_Net_Revenue'], bins=[-1000000000, 0, 10000000, 50000000, 100000000,10000000000])
    fr_r = r.value_counts()
    fr_r = fr_r.rename(name)
    df_fr=df_fr.append(fr_r)
tick_label = df_fr.index
x = np.arange(len(tick_label))

y1 = df_fr.iloc[:,0]
y2 = df_fr.iloc[:,3]
y3 = df_fr.iloc[:,4]
y4 = df_fr.iloc[:,2]

plt.bar(x,y1,width=0.4,label='0-10M',color='#9370DB',zorder=5)
plt.bar(x,y2,width=0.4,bottom=y1,label='10M-50M',color='#000080',zorder=5)
plt.bar(x,y3,width=0.4,bottom=y1,label='50M-100M',color='#00bfc4',zorder=5)
plt.bar(x,y4,width=0.4,bottom=y1,label='100M<',color='#f9766e',zorder=5)

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