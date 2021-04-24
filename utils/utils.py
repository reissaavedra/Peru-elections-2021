from yaml import load, FullLoader
from tweepy import OAuthHandler, API, Cursor, StreamListener, Stream

PATH_YAML_CREDENTIALS = r'config/credentialsTwitterConf.yml'
PATH_YAML_KEYWORDS = r'config/keyWordsConf.yml'
PATH_YAML_EXTRACT_DATA = r'config/extractDataConf.yml'

consumerKey = 'CONSUMER_KEY'
consumerSecretKey = 'CONSUMER_SECRET_KEY'
accessTokenKey = 'ACCESS_TOKEN_KEY'
accessTokenSecretKey = 'ACCESS_TOKEN_SECRET_KEY'

retryDelay = 'RETRY_DELAY'
retryCount = 'RETRY_COUNT'
retryErrors = 'RETRY_ERRORS'
waitOnRateLimitNotify = 'WAIT_ON_RATE_LIMIT_NOTIFY'
sinceDate = 'SINCE_DATE'
itemsCount = 'ITEMS_COUNT'
lang = 'LANG'

def loadParametersYml(path):
    with open(path) as file:
        parameters = load(file, Loader=FullLoader)
        return parameters

def configTweepy():
    paramCredentials = loadParametersYml(PATH_YAML_CREDENTIALS)
    paramExtractData = loadParametersYml(PATH_YAML_EXTRACT_DATA)
    auth = OAuthHandler(paramCredentials[consumerKey], paramCredentials[consumerSecretKey])
    auth.set_access_token(paramCredentials[accessTokenKey], paramCredentials[accessTokenSecretKey])
    api = API(auth,
              wait_on_rate_limit=True,
              retry_delay=paramExtractData[retryDelay],
              retry_count=paramExtractData[retryCount],
              retry_errors=set(paramExtractData[retryErrors]),
              wait_on_rate_limit_notify=paramExtractData[waitOnRateLimitNotify])
    return api

def getDatesExtractData():
    paramExtractData = loadParametersYml(PATH_YAML_EXTRACT_DATA)
    return paramExtractData[sinceDate]

def getKeywords(candidate):
    return loadParametersYml(PATH_YAML_KEYWORDS)[candidate]

def getItemsCount():
    return loadParametersYml(PATH_YAML_EXTRACT_DATA)[itemsCount]

def getLanguages():
    return loadParametersYml(PATH_YAML_EXTRACT_DATA)[lang]

