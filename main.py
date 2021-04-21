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
    print(f"Candidate: {candidate}, Language: {lang} \n")
    import time
    with open(fileName, 'a', encoding="utf-8") as file:
        writer = csv.writer(file, delimiter=',', quotechar='"', quoting=csv.QUOTE_MINIMAL)
        writer.writerow(TweetBatch.TweetBatch.columns)
        i = 0
        for tweet in tweets:
            try:
                tweetBatch = TweetBatch.TweetBatch(tweet._json)
                writer.writerow(tweetBatch.__dict__.values())
                i += 1
                if i % 100 == 0:
                    sleepTime = random.randint(2,5)
                    print(f'Stoping {sleepTime} seconds....')
                    time.sleep(60 * sleepTime)
                    print('Reanunding....')
            except Exception as e:
                print(e)
                continue

if __name__ == '__main__':
    extractTweets()
