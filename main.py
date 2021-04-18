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
    tweetsExtracted = [[
        TweetBatch.TweetBatch(tweet._json)
    ] for tweet in tweets]

    print(f"Candidate: {candidate}, Language: {lang}, Tweets extraidos : {len(tweetsExtracted)}  \n")

    with open(fileName, 'a') as file:
        try:
            writer = csv.writer(file, delimiter=',', quotechar='"', quoting=csv.QUOTE_MINIMAL)
            writer.writerow(TweetBatch.TweetBatch.columns)
            for t in tweetsExtracted:
                writer.writerow(t[0].__dict__.values())
        except Exception as e:
            print(e)


if __name__ == '__main__':
    extractTweets()
