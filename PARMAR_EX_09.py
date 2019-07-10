#AUTHOR NAME : NISHIT PARMAR

#CWID : 10432431

#EX 09

import urllib2

from bs4 import BeautifulSoup

import re

from operator import itemgetter

from wordcloud import WordCloud

import matplotlib.pyplot as plt

import pandas as pd

"""
IDS THAT WERE TRIED : 
    1)iron_man
    2)the_incredible_hulk
    3)the_amazing_spider_man
    4)avengers_infinity_war
    5)thor
    
"""

movie_id = raw_input('Enter movie ID: ')

stopwords= open("stopwords_en.txt")

page = urllib2.urlopen('https://www.rottentomatoes.com/m/'+ movie_id +'/reviews/')

soup = BeautifulSoup(page,'lxml')

score_d = { "A+" : 1, "A" : 0.96, "A-" : 0.92, "B+" : 0.89,
              "B" : 0.86, "B-" : 0.82, "C+" : 0.79, "C" : 0.76, "C-" : 0.72, 
              "D+" : 0.69, "D" : 0.66, "D-" : 0.62}
              
pages = soup.find('span',{'class':re.compile('pageInfo')}).text.strip().split(' ')[3]

current = 1

score = []

while current <= int(pages):
    
    page = urllib2.urlopen('https://www.rottentomatoes.com/m/'+ movie_id +'/reviews/?page='+str(current))
    
    soup = BeautifulSoup(page,'lxml')
    
    review = soup.findAll('div',{'class':re.compile('review_desc')})
    
    for i in review:
        
        r = i.find('div',{'class':re.compile('the_review')}).text.strip()
        
        try:
            
            rating = i.find('div',{'class':re.compile('small subtle')}).text.strip()
            
            if "Original Score" in rating:
                
                rating = re.split('[|:/]',rating)
                
                rating = float(rating[2].strip())/float(rating[3].strip())
                
            else: continue
            
        except:
            
            continue
            
        score.append([r, rating])
        
    current += 1
    
score = sorted(score, key=itemgetter(1), reverse = True)

print

print("The top 20 reviews are listed:", score[:20])

print

score = sorted(score, key=itemgetter(1))

print

print("The bottom 20 reviews are listed :", score[:20])

print

data = pd.read_table(stopwords)

stopwords.close()

data = data.iloc[:,0].values.tolist()

wordc=[]

for review in score:

    words = review[0].split(' ')

    for word in words:

        if word not in data:

            wordc.append(word)    


word = WordCloud(background_color="white", max_words=15,stopwords=data)

word.generate(" ".join(wordc))

word.to_file("file1.png")

plt.imshow(word)

plt.axis('off')

plt.show()

