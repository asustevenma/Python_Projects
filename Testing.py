import csv
import pandas as pd
import numpy as np
import string
import re
import glob
import os
import operator
import nltk
from nltk.corpus import stopwords
from stemming.porter2 import stem
from nltk.classify.api import ClassifierI

# Read CSV file and build a dataframe #
path = '#user-defined#'
csvFiles = glob.glob(path + "/*.csv")
Doc = os.listdir(path)

file_list = []
name_list = []
test_df = pd.DataFrame()
for file_name, file in zip(Doc, csvFiles):
    df = pd.read_csv(file, index_col=None, header=0)
    df['Twitter_ID'] = file_name[:-4]
    file_list.append(df)
test_df = pd.concat(file_list)

# Manipulating text data #
id_list = []
time_list = []
text_list = []
influencer_tweets = []
for index, row in test_df.iterrows():
    #id_list.append(row['id'][2:])
    #time_list.append(row['created_at'])
    #text_list.append(row['text'][2:])
    tweet_tuple = list([row['id'][2:-1], row['text'][2:], row['Twitter_ID']])
    influencer_tweets.append(tweet_tuple)
print("Original tweet =>")
print(influencer_tweets[0])
print()

# Text processing #
tweets_test = []
regex = re.compile('[%s]' % re.escape(string.punctuation))
sw = stopwords.words("english")

for (tweet_id, words, twitter_id) in influencer_tweets:
    new_words = words.split()
    for mouse in new_words:
        if mouse.startswith('@'):
            new_words.remove(mouse)
    words_removed = [''.join(c for c in s if c not in string.punctuation) for s in new_words]
    words_lowered = [e.lower() for e in words_removed]
    for single_word in words_lowered:
        if single_word.startswith('http'):
            words_lowered.remove(single_word)
    words_nonstopped = [w for w in words_lowered if w not in sw]
    words_stemmed = [stem(txt) for txt in words_nonstopped]
    tweets_test.append([tweet_id, words_stemmed, twitter_id])
print("Tweet after text processing =>")
print(tweets_test[0])

count_pos=0
count_neg=0
# Add sentiment in the tuple #
for i in range(len(test_df)):
    tweets_test[i] += list([classifier.classify(extract_features(tweets_test[i][1]))])
    if(classifier.classify(extract_features(tweets_test[i][1]))=="Pos"):
        count_pos= count_pos+1
    else:
        count_neg= count_neg+1

per_senti_pos=count_pos/(count_pos+count_neg)*100
per_senti_neg=count_neg/(count_pos+count_neg)*100
print()
print("Total Number of Tweets:",len(test_df))
print("Number of Positive Tweets:",count_pos)
print("Number of Negetive Tweets:",count_neg)
print("Percentage of Positive Tweets:",per_senti_pos)
print("Percentage of Negetive Tweets:",per_senti_neg)

# Convert to dataframe
lable = ['Tweet_ID', 'Tweets', 'Twitter_ID', 'Sentiment']
tweet_dataframe = pd.DataFrame(tweets_test, columns = lable)

# Extract Negative tweets #
#Negative_ids = []
#for t in range(len(test_df)):
#    if (tweets_test[t][2] == 'Neg'):
#        Negative_ids.append(tweets_test[t][0])
##print(Negative_ids)
#
#Negative_tweets = []
#for l in range(len(test_df)):
#    if influencer_tweets[l][0] in Negative_ids:
#        Negative_tweets.append(tuple([influencer_tweets[l][0],influencer_tweets[l][1]]))
#print()
#print("Negative_tweets =>")
#print(Negative_tweets)