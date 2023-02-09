#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Created on Mon Jan 30 15:57:52 2023

@author: trekz1
"""

import pandas as pd
import matplotlib.pyplot as plt
import numpy as np
from sklearn.linear_model import LinearRegression


xmas_db = pd.read_csv('christmas_movies.csv')  #read xmas films table
big_db = pd.read_csv('top 6359 movie budgets - Sheet1.csv') #read general films table
TM_db = pd.read_csv('RTdb/rotten_tomatoes_movies.csv')

# remove commas and dollar signs in the 3 numerical columns and convert them to integers:

big_db['Production Budget'] = big_db['Production Budget'].str.replace(',', '') # remove all commas in this column
big_db['Production Budget'] = big_db['Production Budget'].str.replace('$', '') # remove all dollar signs in column
big_db['Production Budget'] = big_db['Production Budget'].astype(int) # convert to integers

big_db['Domestic Gross'] = big_db['Domestic Gross'].str.replace(',', '') # remove all commas in this column
big_db['Domestic Gross'] = big_db['Domestic Gross'].str.replace('$', '') # remove all dollar signs in column
big_db['Domestic Gross'] = big_db['Domestic Gross'].astype(int) # convert to integers

big_db['Worldwide Gross'] = big_db['Worldwide Gross'].str.replace(',', '') # remove all commas in this column
big_db['Worldwide Gross'] = big_db['Worldwide Gross'].str.replace('$', '') # remove all dollar signs in column
big_db['Worldwide Gross'] = big_db['Worldwide Gross'].astype(int) # convert to integers

big_db['Movie'] = big_db['Movie'].str.replace(' ','') # remove spaces from title
big_db['Movie'] = big_db['Movie'].str.upper() # convert title to upper case

xmas_db['title'] = xmas_db['title'].str.replace(' ','') # remove spaces from title
xmas_db['title'] = xmas_db['title'].str.upper() # convert title to upper case

TM_db['movie_title'] = TM_db['movie_title'].str.replace(' ', '')
TM_db['movie_title'] = TM_db['movie_title'].str.upper()

#filtering for the numbers data
filtered = big_db[big_db['Movie'].isin(xmas_db['title'])]
filtered.to_csv('temp.csv',index=False)

xmasnew = pd.read_csv('temp.csv')

xmasnew.drop(['Domestic Profit', 'Worldwide Profit'], axis='columns', inplace=True)     
xmasnew2 = xmasnew.reset_index(drop=True)
xmasnew2['Worldwide Net Revenue'] = xmasnew2.apply(lambda x: x['Worldwide Gross'] - x['Production Budget'], axis=1)
xmasnew3 = xmasnew2.sort_values(by='Worldwide Net Revenue', ascending = False).reset_index(drop=True)
xmasnew3.drop(['Unnamed: 0', 'Release Date',  'Worldwide Gross', 'Domestic Gross'], axis='columns', inplace=True) 

xmasmerge=pd.merge(xmas_db, xmasnew3, how='outer', left_on='title', right_on='Movie')

#filltering for the RT db
filteredRT = TM_db[TM_db['movie_title'].isin(xmas_db['title'])]
filteredRT2 = filteredRT.reset_index(drop=True)

RTmerge=pd.merge(xmasmerge, filteredRT2, how='outer', left_on='Movie', right_on='movie_title')
#RTmerge1=RTmerge.dropna(subset=['title']).reset_index(drop=True)
RTmerge1 = RTmerge[pd.notnull(RTmerge['title'])].reset_index(drop=True)
RTmerge2=RTmerge1.drop_duplicates(subset='title').reset_index(drop=True)
RTmerge2.drop(['runtime_x', 'release_year', 'img_src', 'Movie', 'runtime_y'], axis='columns', inplace=True)
#RTmerge2.to_csv('test.csv')

RTmerge2= RTmerge2[RTmerge2.type != 'TV Episode'].reset_index(drop=True)
RTmerge2=RTmerge2.fillna(0)

print('Meta Score=',RTmerge2['Worldwide Net Revenue'].corr(RTmerge2['meta_score']))
print('IMDB=',RTmerge2['Worldwide Net Revenue'].corr(RTmerge2['imdb_rating']))
print('Audience=',RTmerge2['Worldwide Net Revenue'].corr(RTmerge2['audience_rating']))
print('TM=',RTmerge2['Worldwide Net Revenue'].corr(RTmerge2['tomatometer_rating']))
#print('Votes=',RTmerge2['Worldwide Net Revenue'].corr(RTmerge2['votes']))

low = (0, 1, 0)
medium = (0, 0, 1)
mediumhigh = (0, 0.8, 1)
high = (1, 0, 0)

grossranges = []

for value in RTmerge2['Worldwide Net Revenue']:
    if value > float(100000000.0):
        grossranges.append(high)
        
    elif value <= float(100000000.0) and value > float(50000000.0):
        grossranges.append(mediumhigh)
    
    elif value <=float(50000000.0) and value > float(10000000.0):
        grossranges.append(medium)
        
    elif value <= float(10000000.0):
        grossranges.append(low) 

fig, axs = plt.subplots(2, 2)

x1 = RTmerge2.meta_score
x2 = RTmerge2.imdb_rating
x3 = RTmerge2.audience_rating
x4 = RTmerge2.tomatometer_rating
y = RTmerge2['Worldwide Net Revenue']

plt.style.use("seaborn")

a, b = np.polyfit(x1, y, 1)
axs[0,0].scatter(x1, y, 
            c=grossranges,
            cmap='jet',
            alpha=0.8,
            
)
axs[0,0].plot(x1, a*x1+b, color='black', linestyle='--', linewidth=2.5)
axs[0,0].set_xlabel('Meta Score')

a1, b1 = np.polyfit(x2, y, 1)
axs[0,1].scatter(x2, y, 
            c=grossranges,
            cmap='jet',
            alpha=0.8,
            
)
axs[0,1].plot(x2, a1*x2+b1, color='black', linestyle='--', linewidth=2.5)
axs[0,1].set_xlabel('IMDB Rating')

a2, b2 = np.polyfit(x3, y, 1)
axs[1,0].scatter(x3, y, 
            c=grossranges,
            cmap='jet',
            alpha=0.8,
            
)
axs[1,0].plot(x3, a2*x3+b2, color='black', linestyle='--', linewidth=2.5)
axs[1,0].set_xlabel('Audience Rating')

a3, b3 = np.polyfit(x4, y, 1)
axs[1,1].scatter(x4, y, 
            c=grossranges,
            cmap='jet',
            alpha=0.8,
            
)
axs[1,1].plot(x4, a3*x4+b3, color='black', linestyle='--', linewidth=2.5)
axs[1,1].set_xlabel('TM Rating')

for ax in axs.flat:
    ax.set(ylabel='Worldwide Net Revenue')

plt.show()

features = RTmerge2[['meta_score','imdb_rating','audience_rating','tomatometer_rating']]
target = y

lr = LinearRegression()
lr.fit(features,target)
print(lr.intercept_)
coeff=(lr.coef_)
