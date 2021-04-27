import argparse as argp
import datetime
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
FORMAT_DATE = '%Y-%m-%d'


def generateDates():
    import datetime
    today = datetime.date.today()
    sinceDate = datetime.datetime.strptime(getDatesExtractData(), FORMAT_DATE).date()
    differenceBetweenDates = abs((today - sinceDate).days) + 1
    return [(sinceDate + datetime.timedelta(days=i)).strftime(FORMAT_DATE) for i in range(differenceBetweenDates)]


def extractTweets():
    api = configTweepy()
    if api:
        languages = getLanguages()
        itemsCount = getItemsCount()
        rangeDates = generateDates()
        os.makedirs(PATH_DATA_CSV, exist_ok=True)
        v = 0
        for dateToSearch in rangeDates:
            for key, lang in product(candidates.keys(), languages):
                cursorTweepy = Cursor(configTweepy().search,
                                      q=getKeywords(candidates[key]),
                                      lang=lang,
                                      since=f'{dateToSearch}',
                                      until=f'{rangeDates[v + 1]}',
                                      show_user=True).items(itemsCount)
                print(
                    f'Staring download tweets Candidate: {candidates[key]}, dateToSearch: {dateToSearch}, lang: {lang}')
                uploadTweets2Csv(cursorTweepy, candidates[key], lang, dateToSearch)
            v += 1

def extractTweetTest():
    api = configTweepy()
    if api:
        cursorTweepy = Cursor(configTweepy().search,
            q='keiko',
            lang='es',
            since='2021-04-26',
            until='2021-04-27',
            show_user=True).items(10)
        import json
        arrJson = [json.dumps(t._json, indent=2) for t in cursorTweepy]
        with open('test/jsonTweetsTest.json','a') as f:
            json.dump(arrJson, f)

def uploadTweets2Csv(tweets, candidate, lang, dateToSearch):
    fileName = os.path.join(PATH_DATA_CSV, f'{candidate}_{lang}_{dateToSearch}.csv')
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
                if i % 500 == 0:
                    print(f'{i} tweets donwloaded')
                    sleepTime = random.randint(2, 4)
                    time.sleep(60 * sleepTime)
            except Exception as e:
                print(e)
                continue


if __name__ == '__main__':
    # parse command line options
    # params = {
    #     'date': datetime.date.today().strftime('%Y-%m-%d'),
    #     'cand': '',
    #     'format': 'csv',
    #     'outFile': ''
    # }
    #
    # parser = argp.ArgumentParser()
    # parser.add_argument('-d', '--date',
    #                     help='date for extraction', type=str)
    # parser.add_argument('-c', '--cand',
    #                     help='candidate for extraction', type=str)
    # parser.add_argument('-f', '--format',
    #                     help='format output-file', type=str)
    # parser.add_argument('-of', '--outfile',
    #                     help='output-file', type=str)
    # options = parser.parse_args()
    #
    # if options.date is not None:
    #     params['date'] = options.date
    #
    # if options.format is not None:
    #     params['format'] = options.format
    #
    # if options.cand is not None:
    #     params['cand'] = options.cand
    # else:
    #     raise SystemExit('Debe ingresar el nombre del candidato')
    #
    # if options.format is not None:
    #     params['outFile'] = options.outfile
    # else:
    #     params['outFile'] = os.path.join(params['date'], f"{params['cand']}.{params['format']}")
    #
    # #
    extractTweetTest()
