# -*- coding: cp1252 -*-
import re
import csv
import operator
import math
import numpy as np
import matplotlib.pyplot as plt
from collections import Counter

stop_words = ['a', 'does', 'anyone', '’ve', 'found', 'are', 'seems', 'has', 'using','based', 'add','been',
            'for', 'support', 'to', 'in', 'if', 'How', 'of', 'I', 'find','from', 'an', 'prevent', 'get',
            'and', 'the', 'not', 'with', 'can', 'code', 'text','same', '-', 'do', 'on', 'only', 'which',
              'me', 'all', 'be', 'when', 'how', '<p>', 'instead', 'Title', 'check', 'my', 'using','can',
              'by', 'is', 'or', 'about', 'above', 'after', 'again', 'against', 'all', 'am', 'an','name',
              'and', 'any', 'are', "aren't", 'as', 'at', 'be', 'because', 'been', 'before', 'being','specific',
              'below', 'between', 'both', 'but', 'by', "can't", 'cannot','could', "couldn't", 'did','+','/',
              "didn't", 'do', 'does', "doesn't", 'doing', "don't", 'down', 'during', 'each', 'few','access',
              'for', 'from', 'further', 'had', "hadn't", 'has', "hasn't", 'have', "haven't", 'having','new',
              'he', "he'd", "he'll", "he's", 'her', 'here', "here's", 'hers', 'herself', 'him', 'himself','change',
              'his','how',"how's",'i',"i'd","i'll","i'm","i've",'if','in','into','is',"isn't",'it',"it's",'another',
              'its',"itself","let's",'me','more','most',"mustn't",'my','myself','no','nor','not','of','off','use',
              'on','once','only','or','other','ought','our','ours ','ourselves','out','over','own','same','working',
              "shan't",'she',"she'd","she'll","she's",'should',"shouldn't",'so','some', 'such', 'than', 'that','2','why',
              "that's",'the','their','theirs','them','themselves','then','there',"there's", 'these','they','way','make',
              "they'd","they'll","they're","they've",'this','those','through','to', 'too','under','until','up','inside',
              'very','was', "wasn't",'we',"we'd","we'll","we're","we've",'were',"weren't",'what',"what's",'when','work',
              "when's", 'where',"where's",'which','while','who',"who's",'whom', 'why',"why's",'with',"won't",'would',
              "wouldn't", 'what', 'you',"you'd","you'll","you're","you've",'your','yours','yourself','yourselves']


#open SampleTrain
ifile  = open('SampleTrain.csv', "rb")
reader = csv.reader(ifile)

title_list = []
keywords_list = []

#grab keywords in tag
for row in reader:
    new_row = [x.lower() for x in row]
    if new_row[0] == 'id':
        continue
    #grab the key words in title and put into a list
    title_words = new_row[1].split(" ")
    key_words = new_row[3].split(" ")
    #put keywords into a super list
    for words in key_words:
        keywords_list.append(words)

#store the top100 words as a dictionary
top100 = dict(Counter(keywords_list).most_common(200))
total_words = sum(top100.values())
#show histogram of distribution of words
words_array = np.asarray(list(top100.values()))
plt.hist(words_array,50)
plt.show()
#print top100
print total_words

ifile.close()
