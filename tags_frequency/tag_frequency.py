# -*- coding: utf-8 -*-
"""
Created on Thu Feb 16 18:48:40 2023

@author: hanwe
"""


import pandas as pd #熊猫很可爱。被治愈了。 
import matplotlib.pyplot as plt
import numpy as np
import scipy.stats as stats
import wordcloud as wc

df = pd.read_csv('tag.csv')


df_counted = df['tag'].value_counts().rename_axis('tag').reset_index(name = 'frequency')

df_fr = df_counted.head(49)

fr = dict(zip(df_fr['tag'],df_fr['frequency']))

tags = wc.WordCloud(\
   width = 1000, height = 700,\
   background_color = "white",
   font_path = "msyh.ttc"
    )
tags.fit_words(fr)
plt.imshow(tags)
plt.axis('off')
plt.savefig('bar5.png', dpi=600)
plt.show()

df_fr.to_csv('tags49.csv')