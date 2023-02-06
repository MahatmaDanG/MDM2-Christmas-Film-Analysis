import pandas as pd
from thenumbers import xmasnew3 #thenumbers is the file that Alex uploaded (xmas_filter.py)
import matplotlib.pyplot as plt

moviesdb = pd.read_csv('df/movies.csv')
ratingsdb = pd.read_csv('df/ratings_xmas.csv')
tagsdb = pd.read_csv('df/tags_xmas.csv')
xmasdb = pd.read_csv('christmas_movies.csv')  #read xmas films table (from kagloo)

#print(type(xmasdb.title))

moviesdb['title']=moviesdb['title'].str.replace(' ', '').str.replace('(', '').str.replace(')', '').str.replace('0', '').str.replace('1', '').str.replace('2', '').str.replace('3', '').str.replace('4', '').str.replace('5', '').str.replace('6', '').str.replace('7', '').str.replace('8', '').str.replace('9', '')
moviesdb['title']=moviesdb['title'].str.upper()
moviesdb['title']=moviesdb['title'].str.replace(' ', '').str.upper()

xmasdb['title'] = xmasdb['title'].str.replace(' ','')# remove spaces from title
xmasdb['title'] = xmasdb['title'].str.upper() # convert title to upper case

xmasdb['votes'] = xmasdb['votes'].str.replace(',','')

xmasdb['gross'] = xmasdb['gross'].str.replace('M','').str.replace('$', '')
xmasdb['gross'] = xmasdb['gross'].astype(float) * 1e6

merged=pd.merge(moviesdb, ratingsdb, how='outer', on='movieId')
merged2 = merged.drop_duplicates(subset='movieId')
merged2.set_index('movieId', inplace=True)
mergedtags=pd.merge(merged2, tagsdb, how='outer', on ='movieId')

filtered = mergedtags[mergedtags['title'].isin(xmasnew3['Movie'])]
mergedprofit = pd.merge(filtered, xmasnew3, how='outer', left_on='title', right_on='Movie')

mergetot = pd.merge(mergedprofit, xmasdb, how='outer', on='title')
mergetot.drop(['type', 'img_src', 'userId_x', 'userId_y','timestamp_x', 'timestamp_y', 'Unnamed: 0', 'movieId', 'Release Date', 'Movie', 'runtime', 'release_year'], axis='columns', inplace=True) 
