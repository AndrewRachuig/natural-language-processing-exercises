import unicodedata
import re
import json

import nltk
from nltk.tokenize.toktok import ToktokTokenizer
from nltk.corpus import stopwords

import pandas as pd

import acquire

def basic_clean(string):
    string = string.lower()
    string = unicodedata.normalize('NFKD', string).encode('ascii', 'ignore').decode('utf-8', 'ignore')
    string = re.sub(r'[^a-z0-9\'\s]', '', string)
    return string

def tokenize(string):
    tokenizer = nltk.tokenize.ToktokTokenizer()
    return tokenizer.tokenize(string, return_str=True)

def stem(string):
    ps = nltk.porter.PorterStemmer()
    stems = [ps.stem(word) for word in string.split()]
    return ' '.join(stems)

def lemmatize(string):
    wnl = nltk.stem.WordNetLemmatizer()
    lemmas = [wnl.lemmatize(word) for word in string.split()]
    return ' '.join(lemmas)

def remove_stopwords(string, extra_words = None, exclude_words = None):
    stopword_list = stopwords.words('english')
    if extra_words != None:
        stopword_list = stopword_list.append(extrawords)
    if exclude_words != None:
        stopword_list = stopword_list.remove(exclude_words)
    words = string.split()
    filtered_words = [w for w in words if w not in stopword_list]
    return ' '.join(filtered_words)

def news_df_prepare():
    news_df = acquire.get_all_inshorts_articles()
    news_df.drop(columns = 'category', inplace=True)
    news_df.rename({'content':'original'}, axis=1, inplace=True)
    news_df['clean'] = news_df.original.apply(basic_clean)
    news_df['clean'] = news_df.clean.apply(tokenize)
    news_df['clean'] = news_df.clean.apply(remove_stopwords)
    news_df['stemmed'] = news_df.clean.apply(stem)
    news_df['lemmatized'] = news_df.clean.apply(lemmatize)
    return news_df

def codeup_df_prepare():
    codeup_df = acquire.get_all_codeup_blogs()
    codeup_df.drop(columns= ['date','link'], inplace=True)
    codeup_df.rename({'content':'original'}, axis=1, inplace=True)
    codeup_df['clean'] = codeup_df.original.apply(basic_clean)
    codeup_df['clean'] = codeup_df.clean.apply(tokenize)
    codeup_df['clean'] = codeup_df.clean.apply(remove_stopwords)
    codeup_df['stemmed'] = codeup_df.clean.apply(stem)
    codeup_df['lemmatized'] = codeup_df.clean.apply(lemmatize)
    return codeup_df
