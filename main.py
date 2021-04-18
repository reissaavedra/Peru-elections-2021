from yaml import load, FullLoader
import tweepy
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
    parametersYml = loadParametersYml()
    auth = tweepy.OAuthHandler(parametersYml[consumerKey], parametersYml[consumerSecretKey])
    auth.set_access_token(parametersYml[accessTokenKey], parametersYml[accessTokenSecretKey])
    api = tweepy.API(auth,
                     wait_on_rate_limit=True,
                     retry_delay=60 * 3,
                     retry_count=5,
                     retry_errors=set([401, 404, 500, 503]),
                     wait_on_rate_limit_notify=True)
    return api

def extractTweets():
    allTweets = []
    api = configTweepy()
    screen_name = '@userToSearch'
    new_tweets = api.user_timeline(screen_name=screen_name, count=500)
    allTweets.extend(new_tweets)
    oldest = allTweets[-1].id - 1

    while len(new_tweets) > 0:
        print(f"getting tweets before {oldest}")
        new_tweets = api.user_timeline(screen_name=screen_name, count=200, max_id=oldest)
        allTweets.extend(new_tweets)
        oldest = allTweets[-1].id - 1
        print(f"...{len(allTweets)} tweets downloaded so far")

    outTweets = [[tweet.id_str, tweet.created_at, tweet.text.encode("utf-8")] for tweet in allTweets]
    return outTweets


if __name__ == '__main__':
    print(extractTweets())
