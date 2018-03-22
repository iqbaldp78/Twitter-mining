import tweepy
from tweepy import OAuthHandler
import requests
from tweepy import Stream
from tweepy import OAuthHandler
from collections import defaultdict
import sys

consumer_key = 'eDmm8YP3zw6LW2tQm5UvzQiSB'
consumer_secret = 'WMlHYOI2F09u1RvxThnEr9Rmmt6fkObAxGY022FKZXEWX5E1ci'
access_token = '273774576-LOL4953DUWMz62XZhZqdKH8IGXFacCnD2hyi7xwh'
access_secret = 'ezDHV9MHnP4Yc8YMeZY7LwAPOgZTBONxyqx5MAvZ4CeM0'

auth = OAuthHandler(consumer_key, consumer_secret)
auth.set_access_token(access_token, access_secret)

# print(auth)

api = tweepy.API(auth)
user = api.get_user("twitter")
# print(user)
# print(type(tweepy))
# print(api.home_timeline)


# for status in tweepy.Cursor(api.home_timeline).items(10):
#     # Process a single status
#     # print(status.text)
#     print("status.text")

# for tweet in tweepy.Cursor(api.user_timeline).items():
#     # process_or_store(tweet._json)
#     print(tweet.text)

# trends = api.trends_available()

# print(trends)


# for trend in trends:
#     # process_or_store(tweet._json)
#     print(trend)

import json
import nltk
from nltk.tokenize import word_tokenize
import re

with open('data/stream_apple.json', 'r') as f:
    line = f.readline()  # read only the first tweet/line
    tweet = json.loads(line)  # load it as Python dict
    # print(json.dumps(tweet, indent=4)) # pretty-print

# nltk.download('punkt')
# tweet = 'RT @marcobonzanini: just an example! :D http://example.com #NLP'
# print(word_tokenize(tweet))
# ['RT', '@', 'marcobonzanini', ':', 'just', 'an', 'example', '!', ':', 'D', 'http', ':', '//example.com', '#', 'NLP']

emoticons_str = r"""
    (?:
        [:=;] # Eyes
        [oO\-]? # Nose (optional)
        [D\)\]\(\]/\\OpP] # Mouth
    )"""

regex_str = [
    emoticons_str,
    r'<[^>]+>',  # HTML tags
    r'(?:@[\w_]+)',  # @-mentions
    r"(?:\#+[\w_]+[\w\'_\-]*[\w_]+)",  # hash-tags
    r'http[s]?://(?:[a-z]|[0-9]|[$-_@.&amp;+]|[!*\(\),]|(?:%[0-9a-f][0-9a-f]))+',  # URLs

    r'(?:(?:\d+,?)+(?:\.?\d+)?)',  # numbers
    r"(?:[a-z][a-z'\-_]+[a-z])",  # words with - and '
    r'(?:[\w_]+)',  # other words
    r'(?:\S)'  # anything else
]

tokens_re = re.compile(r'(' + '|'.join(regex_str) + ')', re.VERBOSE | re.IGNORECASE)
emoticon_re = re.compile(r'^' + emoticons_str + '$', re.VERBOSE | re.IGNORECASE)


def tokenize(s):
    return tokens_re.findall(s)


def preprocess(s, lowercase=False):
    tokens = tokenize(s)
    if lowercase:
        tokens = [token if emoticon_re.search(token) else token.lower() for token in tokens]
    return tokens


tweet = 'RT @marcobonzanini: just an example! :D http://example.com #NLP'
# print(preprocess(tweet))
# ['RT', '@marcobonzanini', ':', 'just', 'an', 'example', '!', ':D', 'http://example.com', '#NLP']

import json

with open('data/stream_apple.json', 'r') as f:
    for line in f:
        tweet = json.loads(line)
        # print(tweet)
        tokens = preprocess(tweet['text'])
        # print("tokens ", tokens)
        # # do_something_else(tokens)

import operator
import json
from collections import Counter

from nltk.corpus import stopwords
import string

# nltk.download('stopwords')
punctuation = list(string.punctuation)
stop = stopwords.words('english') + punctuation + ['rt', 'via']
terms_stop = [term for term in preprocess(tweet['text']) if term not in stop]
# print("terms_stop", terms_stop)
# print("len(sys.argv)", len(sys.argv))
# print("sys.argv[1]", sys.argv)

fname = 'data/stream_apple.json'
with open(fname, 'r') as f:
    # print("len(sys.argv)", len(sys.argv))
    count_all = Counter()
    com = defaultdict(lambda: defaultdict(int))
    search_word = sys.argv[1]  # pass a term as a command-line argument
    # print("search_word",search_word)
    count_search = Counter()

    for line in f:
        tweet = json.loads(line)
        # Create a list with all the terms
        terms_all = [term for term in preprocess(tweet['text'])]

        # Count terms only once, equivalent to Document Frequency
        terms_single = set(terms_all)
        # Count hashtags only
        terms_hash = [term for term in preprocess(tweet['text'])
                      if term.startswith(('#', '@'))]
        # Count terms only (no hashtags, no mentions)
        terms_only = [term for term in preprocess(tweet['text'])
                      if term not in stop
                      and not term.startswith(('#', '@','...',"'",'RT'))]
        if search_word in terms_only:
            count_search.update(terms_only)
        print("Co-occurrence for %s:" % search_word)
        print(count_search.most_common(20))
        # mind the ((double brackets))
        # startswith() takes a tuple (not a list) if
        # we pass a list of inputs
        # Update the counter
        # print("terms_only", terms_only)
        # print("terms_only",['RT' in x for x in terms_only])

        for i in range(len(terms_only) - 1):
            for j in range(i + 1, len(terms_only)):
                w1, w2 = sorted([terms_only[i], terms_only[j]])
                if w1 != w2:
                    com[w1][w2] += 1

        # For each term, look for the most common co-occurrent terms

        count_all.update(terms_hash)



    com_max = []
    import sys

    for t1 in com:
        t1_max_terms = sorted(com[t1].items(), key=operator.itemgetter(1), reverse=True)[:5]
        for t2, t2_count in t1_max_terms:
            com_max.append(((t1, t2), t2_count))
    # Get the most frequent co-occurrences
    terms_max = sorted(com_max, key=operator.itemgetter(1), reverse=True)
    # print("terms_max", terms_max[:5])

    # Print the first 5 most frequent words
    # print("count_all", count_all.most_common(5))

from nltk import bigrams

terms_bigram = bigrams(terms_stop)
# print("terms_bigram", list(terms_bigram))


import vincent

word_freq = count_search.most_common(20)
print("word_freq",word_freq)
labels, freq = zip(*word_freq)
data = {'data': freq, 'x': labels}
bar = vincent.Bar(data, iter_idx='x')
bar.to_json('data/grafik.json')
# bar.to_json('data/grafik.json', html_out=True, html_path='chart.html')