import random

from tweepy import Cursor, StreamListener, Stream
from utils.utils import configTweepy, getDatesExtractData, getItemsCount, getKeywords, getLanguages
from batch import TweetBatch
import os
from itertools import product
import csv

candidates = {
    'castilloValue': 'Castillo',
    'keikoValue': 'Keiko'
}

PATH_DATA_CSV = './dataCsv'


def extractTweets():
    api = configTweepy()
    if api:
        languages = getLanguages()
        itemsCount = getItemsCount()
        sinceDate = getDatesExtractData()
        os.makedirs(PATH_DATA_CSV, exist_ok=True)

        for key, lang in product(candidates.keys(), languages):
            cursorTweepy = Cursor(configTweepy().search,
                                  q=getKeywords(candidates[key]),
                                  lang=lang,
                                  since=sinceDate).items(itemsCount)
            uploadTweets2Csv(cursorTweepy, candidates[key], lang)


def uploadTweets2Csv(tweets, candidate, lang):
    fileName = os.path.join(PATH_DATA_CSV, f'{candidate}_{lang}.csv')
    import time
    with open(fileName, 'a') as file:
        try:
            writer = csv.writer(file, delimiter=',', quotechar='"', quoting=csv.QUOTE_MINIMAL)
            writer.writerow(TweetBatch.TweetBatch.columns)
            i = 0
            for tweet in tweets:
                tweetBatch = TweetBatch.TweetBatch(tweet._json)
                writer.writerow(tweetBatch.__dict__.values())
                i += 1
                if i % 100 == 0:
                    time.sleep(60 * random.randint(4, 10))
        except Exception as e:
            print(e)
        finally:
            print(f"Candidate: {candidate}, Language: {lang}, Tweets extraidos : {i}  \n")


if __name__ == '__main__':
    extractTweets()
