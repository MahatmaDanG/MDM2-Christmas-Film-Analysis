#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Created on Mon Jan 30 15:57:52 2023

@author: trekz1
"""

import pandas as pd

xmas_db = pd.read_csv('christmas_movies.csv')  #read xmas films table
big_db = pd.read_csv('top 6359 movie budgets - Sheet1.csv') #read general films table
big_db['Domestic Profit'] = ''  #empty columns for domestic profit and worldwide profit
big_db['Worldwide Profit'] = ''

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
 




#for loop to find both domestic and worldwide profit (profit = gross - budget) 
'''
for pb in big_db.loc[:,'Production Budget']:
    for dg in big_db.loc[:,'Domestic Gross']:
        dp = dg - pb
        dp = str(dp)
        big_db['Domestic Profit'] = big_db['Domestic Profit'] + dp
        
    for wg in big_db.loc[:,'Worldwide Gross']:
        wp = wg - pb
        wp = str(wp)
        big_db['Worldwide Profit'] = big_db['Worldwide Profit'] + wp
'''

filtered = big_db[big_db['Movie'].isin(xmas_db['title'])]
filtered.to_csv('temp.csv',index=False)