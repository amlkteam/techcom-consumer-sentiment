# -*- coding: utf-8 -*-
"""
Created on Thu Feb 27 17:18:05 2020

@author: amy
"""
import csv
import tweepy

#private auth info
CONSUMER_KEY = 'asnczCvhDQ01WjWyMtLWNfpbV'
CONSUMER_SECRET = 'HV6CoccQL3Us53g6ZQQCptflv8V4NHMvReh2goPhSjdcWPyZZt'
ACCESS_TOKEN = '54511184-onbbTjSAtut8MFzh39Yhd6W9ok1LOTFPFMmvPewVw'
ACCESS_SECRET  = 'D7OEueBl05LzVv0Tu93iHABiIwhiOVsaLPI46LSD77DV1'

# Setup tweepy to authenticate with Twitter credentials:

auth = tweepy.OAuthHandler(CONSUMER_KEY, CONSUMER_SECRET)
auth.set_access_token(ACCESS_TOKEN, ACCESS_SECRET)

# Create the api to connect to twitter with credentials
api = tweepy.API(auth, wait_on_rate_limit=True, wait_on_rate_limit_notify=True, compression=True)

#rate limits check
#api.rate_limit_status()

#now use Twitter search API with keywords in ['Apple','Google','Amazon','Facebook','Microsoft']

#trying out "Apple" only in this proof-of-concept
#can use "#AppleInc" to narrow down results as "Apple" returns too many irrelvant tweets

##execution note: there's no french tweet result with #AppleInc, but there is results with 'Apple'
#we want to exclude retweets in our corpus
results = api.search("Apple",count=100, lang = "en", exclude = "retweets") #trying out "en" first in this demo


#store the results in a dict
tweets_info_results = []
for tweet in results:
    print(tweet._json["text"])
    tweets_info = dict()
    
    #we mainly need about 5 attributes of the tweets: tweet_id, user_info, creation_time, text, and lang
    #we want to remove quoted tweets in our corpus
    if not tweet._json['is_quote_status']:
        tweets_info['created_at'] = tweet._json["created_at"]
        tweets_info['tweet_id'] = tweet._json["id"]
        tweets_info['text'] = tweet._json["text"]
        tweets_info['lang'] = tweet._json["lang"] 
        #user_info is a dict that includes user_id, user name, user description etc
        #could be useful for annotating user's relation with the tech company he tweeted
        tweets_info['user_info'] = tweet._json["user"] 
    if len(tweets_info) > 0: 
        tweets_info_results.append(tweets_info)


print(len(tweets_info_results)) #returns 100 results in this demo. 

#export results to a csv file
with open('twitter_apple_scrap_string.csv', 'a', newline='', encoding='utf-8') as csvfile:
    fieldnames = [ 'tweet_id','created_at','lang','text','user_info']
    writer = csv.DictWriter(csvfile, fieldnames=fieldnames)

    #only write header for the first time, comment it out from second time onwards
    #writer.writeheader() 
    for tweets_info in tweets_info_results:
        writer.writerow(tweets_info)
    
    
    