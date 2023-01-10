import tweepy
import pandas as pd 
import json
from datetime import datetime
import s3fs 

# The first part of this funcion is an standard code to connect to Twitter API after successfully 
# authenticate.
# The second part is the code to create an API object, in this case, to look for the tweets of an User.

def run_twitter_etl():
    
    access_key = "" 
    access_secret = "" 
    consumer_key = ""
    consumer_secret = ""

    
    # Twitter authentication
    auth = tweepy.OAuthHandler(access_key, access_secret)   
    auth.set_access_token(consumer_key, consumer_secret) 

    # # # Creating an API object 
    api = tweepy.API(auth)
    tweets = api.user_timeline(screen_name='@user', 
                            # 200 is the maximum allowed count anyway
                            count=200,
                            include_rts = False,
                            # Note that is necessary to keep full_text otherwise, 
                            # only the first 140 words would be extracted.
                            tweet_mode = 'extended'
                            )
    # Now we sneak into the tweets object and append the tweets with some useful attributes about the tweets.
    list = []
    for tweet in tweets:
        text = tweet._json["full_text"]

        refined_tweet = {"user": tweet.user.screen_name,
                        'text' : text,
                        'favorite_count' : tweet.favorite_count,
                        'retweet_count' : tweet.retweet_count,
                        'created_at' : tweet.created_at}
        
        list.append(refined_tweet)
    # We create a dataframe with the list of tweets and then we save it as a csv file, this last part using pandas.
    df = pd.DataFrame(list)
    df.to_csv('refined_tweets.csv')