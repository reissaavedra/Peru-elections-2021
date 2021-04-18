from yaml import load, FullLoader
import tweepy
import os

PATH_YAML_CONFIG = r'./config/config.yml'
consumerKey = 'CONSUMER_KEY'
consumerSecretKey = 'CONSUMER_SECRET_KEY'
accessTokenKey = 'ACCESS_TOKEN_KEY'
accessTokenSecretKey = 'ACCESS_TOKEN_SECRET_KEY'

#Parametros de ejecucion
retryDelay = 180



def loadParametersYml():
    with open(PATH_YAML_CONFIG) as file:
        parameters = load(file, Loader=FullLoader)
        return parameters


def configTweepy():
    paramYml = loadParametersYml()
    auth = tweepy.OAuthHandler(paramYml[consumerKey], paramYml[consumerSecretKey])
    auth.set_access_token(paramYml[accessTokenKey], paramYml[accessTokenSecretKey])
    api = tweepy.API(auth,
                     # parser=tweepy.parsers.JSONParser(),
                     wait_on_rate_limit=True,
                     retry_delay=retryDelay,
                     retry_count=5,
                     retry_errors=set([401, 404, 500, 503]),
                     wait_on_rate_limit_notify=True)
    return api


def extractTweets():
    if configTweepy():
        cursorTweepy = tweepy.Cursor(configTweepy().search,
                                     q=["Pedro Castillo", 'pedro castillo', 'Peru Libre'],
                                     lang=['en','es'],
                                     since="2021-04-11").items(100000000)
        # return
        uploadTweets2Csv(cursorTweepy)
        # return tweets


def uploadTweets2Csv(tweets):
    path = './dataCsv'
    os.makedirs(path, exist_ok=True)

    tweetsPedro = [[
        tweet.author,
        tweet.contributors,
        tweet.coordinates,
        tweet.created_at,
        tweet.favorited,
        tweet.geo,
        tweet.id_str,
        tweet.in_reply_to_screen_name,
        tweet.in_reply_to_user_id,
        tweet.is_quote_status,
        tweet.lang,
        tweet.place,
        tweet.retweet_count,
        tweet.retweeted,
        tweet.retweets,
        tweet.source,
        tweet.source_url,
        tweet.text,
        tweet.truncated,
        tweet.user.listed_count,
        tweet.user.location,
        tweet.user.name,
        tweet.user.screen_name,
        tweet.user.statuses_count,
        tweet.user.time_zone,
        tweet.user.verified,
        tweet.user.follow_request_sent,
        tweet.user.friends_count,
        tweet.user.following,
        tweet.user.created_at] for tweet in tweets]
    print(f"Tweets extraidos : {len(tweetsPedro)} \n")
    return tweetsPedro


if __name__ == '__main__':
    # print(len(extractTweets()['statuses']))
    extractTweets()
