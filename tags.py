import pandas as pd

xmasdb = pd.read_csv('christmas_movies.csv')
moviesdb = pd.read_csv('movies.csv')
tagsdb = pd.read_csv('tags_xmas.csv')

moviesdb['title']=moviesdb['title'].str.replace(' ', '').str.replace('(', '').str.replace(')', '').str.replace('0', '').str.replace('1', '').str.replace('2', '').str.replace('3', '').str.replace('4', '').str.replace('5', '').str.replace('6', '').str.replace('7', '').str.replace('8', '').str.replace('9', '')
moviesdb['title']=moviesdb['title'].str.upper()
moviesdb['title']=moviesdb['title'].str.replace(' ', '').str.upper()

xmasdb['title'] = xmasdb['title'].str.replace(' ','')# remove spaces from title
xmasdb['title'] = xmasdb['title'].str.upper() # convert title to upper case

mergedtags=pd.merge(moviesdb, tagsdb, how='outer', on ='movieId') #merging the movies to the tags

filtered = mergedtags[mergedtags['title'].isin(xmasdb['title'])]
merged = pd.merge(filtered, xmasdb, how='outer', on='title')
merged.drop(['type', 'img_src', 'userId', 'timestamp', 'movieId', 'runtime', 'release_year', 'gross', 'stars', 'director', 'imdb_rating', 'meta_score', 'votes', 'rating', 'genre'], axis='columns', inplace=True) 

tagcount = merged['tag'].value_counts() #counting the number of times those tags appear (each row I believe)

print(tagcount[0:49]) #only prints the first 49 (frequency starts at 25 counts)
