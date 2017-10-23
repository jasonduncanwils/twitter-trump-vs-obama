'''-----------------------------------------------------
Retrieve both Barack's tweets and Trumpster's tweets and
determine the most used words
------------------------------------------------------'''
import json  # Import package to process JSON data
from twitter import Twitter, OAuth  # Import package for twitter handling
import operator
import string
from nltk.corpus import stopwords

'''-----------------------------------------------------
Functions
------------------------------------------------------'''


def strip_non_ascii(string):
    # Returns the string without non ASCII characters
    stripped = (c for c in string if 0 < ord(c) < 127)
    return ''.join(stripped)


def word_count(str):
    counts = dict()
    words = str.split()

    for word in words:
        if word in counts:
            counts[word] += 1
        else:
            counts[word] = 1

    return counts


'''-----------------------------------------------------
Retrieve tweets
------------------------------------------------------'''

barack_twitter_handle = "BarackObama"
trump_twitter_handle = "realDonaldTrump"

ACCESS_TOKEN = raw_input('Access token:')
ACCESS_SECRET = raw_input('Access secret:')
API_KEY = raw_input('API key:')
API_SECRET = raw_input('API secret:')
File_path_for_tweets = raw_input('Folder for tweet storage:')

oauth = OAuth(ACCESS_TOKEN, ACCESS_SECRET, API_KEY, API_SECRET)
twitter = Twitter(auth=oauth)  # Connect to Twitter REST API

# Get Barack's 200 most recent tweets
barack_tweets = twitter.statuses.user_timeline(screen_name=barack_twitter_handle, count=200)
barack_tweets_filename = File_path_for_tweets + "/Tweets-barack.txt"

f = open(barack_tweets_filename, 'w')
for tweet in barack_tweets:
    f.write(json.dumps(tweet) + '\n') # write a new line for each tweet to make it easier to retrieve
f.close()

# Get Donald's 200 most recent tweets
donald_tweets = twitter.statuses.user_timeline(screen_name=trump_twitter_handle, count=200)
donald_tweets_filename = File_path_for_tweets + "/Tweets-trumpster.txt"

f = open(donald_tweets_filename, 'w')
for tweet in donald_tweets:
    f.write(json.dumps(tweet) + '\n') # write a new line for each tweet to make it easier to retrieve
f.close()

'''-----------------------------------------------------
Parse and Analyze Tweets
------------------------------------------------------'''
stop = set(stopwords.words('english'))
handles_to_review = [barack_twitter_handle, trump_twitter_handle]

for handle in handles_to_review:
    print '==============================='
    print handle
    print '==============================='

    if handle == barack_twitter_handle:
        tweets_filename = barack_tweets_filename

    if handle == trump_twitter_handle:
        tweets_filename = donald_tweets_filename

    tweets_core_words = ''
    MAGA_count = 0
    FAKENEWS_count = 0

    with open(tweets_filename) as f:
        for line in f:
            try:
                tweet = json.loads(line.strip())  # Read in one line of the file, convert it into a json object
                if 'text' in tweet and 'retweeted_status' not in tweet:  # only messages contains 'text' is a tweet
                    core_words = [i for i in tweet['text'].lower().split() if i not in stop]
                    tweets_core_words = tweets_core_words + ' '.join(core_words)
                    MAGA_count = MAGA_count + tweet['text'].upper().count('MAKE AMERICA GREAT AGAIN'.upper())
                    FAKENEWS_count = FAKENEWS_count + tweet['text'].upper().count('FAKE NEWS'.upper())
            except:
                continue

    tweets_core_words = strip_non_ascii(tweets_core_words)
    tweets_core_words = str(tweets_core_words).translate(None, string.punctuation)
    tweet_count = word_count(tweets_core_words)
    tweet_count_sorted = sorted(tweet_count.items(), key=operator.itemgetter(1), reverse=True)

    for x in tweet_count_sorted:
        if x[1] > 7 and x[0] != 'amp':
            print x

    print 'MAKE AMERICA GREAT AGAIN count: ' + str(MAGA_count)
    print 'FAKE NEWS count: ' + str(FAKENEWS_count)