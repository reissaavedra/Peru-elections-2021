from yaml import load, FullLoader
import tweepy
import os

PATH_YAML_CONFIG = r'./config/config.yml'
consumerKey='CONSUMER_KEY'
consumerSecretKey= 'CONSUMER_SECRET_KEY'
accessTokenKey='ACCESS_TOKEN_KEY'
accessTokenSecretKey='ACCESS_TOKEN_SECRET_KEY'

def loadParametersYml():
    with open(PATH_YAML_CONFIG) as file:
        parameters = load(file, Loader=FullLoader)
        return parameters

def configTweepy():
    paramYml = loadParametersYml()
    auth = tweepy.OAuthHandler(paramYml[consumerKey], paramYml[consumerSecretKey])
    auth.set_access_token(paramYml[accessTokenKey], paramYml[accessTokenSecretKey])
    api = tweepy.API(auth,
                     parser=tweepy.parsers.JSONParser(),
                     wait_on_rate_limit=True,
                     retry_delay=60 * 3,
                     retry_count=5,
                     retry_errors=set([401, 404, 500, 503]),
                     wait_on_rate_limit_notify=True)
    return api if api.verify_credentials() else False

def extractTweets():
    # allTweets = []
    # screen_name = '@userToSearch'
    # new_tweets = api.user_timeline(screen_name=screen_name, count=500)
    # allTweets.extend(new_tweets)
    # oldest = allTweets[-1].id - 1
    #
    # while len(new_tweets) > 0:
    #     print(f"getting tweets before {oldest}")
    #     new_tweets = api.user_timeline(screen_name=screen_name, count=200, max_id=oldest)
    #     allTweets.extend(new_tweets)
    #     oldest = allTweets[-1].id - 1
    #     print(f"...{len(allTweets)} tweets downloaded so far")
    #
    # outTweets = [[tweet.id_str, tweet.created_at, tweet.text.encode("utf-8")] for tweet in allTweets]
    # return outTweets
    new_search = ["Pedro Castillo", 'pedro castillo', 'Peru Libre']
    date_since = "2021-04-11"
    api = configTweepy()
    if api:
        tweets = api.search(q=new_search,
                            lang='en',
                            since=date_since)
        # return [[
        #     # tweet.author,
        #     tweet.contributors,
        #     tweet.coordinates,
        #     tweet.created_at,
        #     tweet.favorited,
        #     tweet.geo,
        #     tweet.id_str,
        #     tweet.in_reply_to_screen_name,
        #     tweet.in_reply_to_user_id,
        #     tweet.is_quote_status,
        #     tweet.lang,
        #     tweet.place,
        #     tweet.retweet_count,
        #     tweet.retweeted,
        #     tweet.retweets,
        #     tweet.source,
        #     tweet.source_url,
        #     tweet.text,
        #     tweet.truncated,
        #     tweet.user.listed_count,
        #     tweet.user.location,
        #     tweet.user.name,
        #     tweet.user.screen_name,
        #     tweet.user.statuses_count,
        #     tweet.user.time_zone,
        #     tweet.user.verified,
        #     tweet.user.follow_request_sent,
        #     tweet.user.friends_count,
        #     tweet.user.following,
        #     tweet.user.created_at] for tweet in tweets]
        uploadTweets2Csv(tweets)
        # return tweets


def uploadTweets2Csv(tweets):
    path = './dataCsv'
    os.makedirs(path, exist_ok=True)
    print(f"Tweets extraidos : {len(tweets['statuses'])} \n")
    for t in tweets['statuses']:
        print(f"{t['text']} \n")

if __name__ == '__main__':
    # print(len(extractTweets()['statuses']))
    extractTweets()