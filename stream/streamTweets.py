import json
import csv
from tweepy import StreamListener, Stream
from utils import configTweepy, getDatesExtractData, getItemsCount, getKeywords, getLanguages
import os
import threading
from itertools import product

if __package__ is None:
    import sys
    from os import path
    sys.path.append( path.dirname( path.dirname( path.abspath(__file__) ) ) )
    # print(sys.path)
    from batch import TweetBatch
    # from utils.utils import configTweepy
else:
    from batch import TweetBatch
    # from utils.utils import configTweepy

path_data_stream = './dataStream'
os.makedirs(path_data_stream, exist_ok=True)
fileName = ''
fileName = os.path.join(path_data_stream, 'stream.csv')

languages = getLanguages()
itemsCount = getItemsCount()
sinceDate = getDatesExtractData()
candidates = {
    'castilloValue': 'Castillo',
    'keikoValue': 'Keiko'
}

class StreamListener(StreamListener):

    def on_status(self,status):
        tweetBatch = TweetBatch.TweetBatch(status._json)
        with open(fileName, 'a', encoding="utf-8") as file:
            try:
                writer = csv.writer(file, delimiter=',', quotechar='"', quoting=csv.QUOTE_MINIMAL)
                if os.stat(fileName).st_size == 0:
                    writer.writerow(TweetBatch.TweetBatch.columns)
                tweetBatchStream = TweetBatch.TweetBatch(status._json)
                writer.writerow(tweetBatchStream.__dict__.values())
            except Exception as e:
                print(e)
            finally:
                print(tweetBatchStream.text)
    
                
    def on_error(self, status_code):
        if status_code == 420:
            return False

# while True:
#         r = api.request('statuses/filter',
#                         {'locations': '-77.2694,-12.4735,-76.6624,-11.6721'})  # Coordenadas para Perú
#         with open("JSONTwitter.csv", "a") as ed:  # "a", si existe el archivo le hace append.
#             for item in r:  # r -> Es el JSON de Twitter #item-> es cada tweet(row)
#                 try:
#                     writer = csv.writer(ed, delimiter=',', quotechar='"', quoting=csv.QUOTE_MINIMAL)
#                     writer.writerow(item)
#                 except Exception as e:
#                     print(e)
#                     item
#                 pprint.pprint(item)

api = configTweepy()
stream_listener = StreamListener()
stream = Stream(auth=api.auth, listener=stream_listener)


# for key, lang in product(candidates.keys(), languages):
#     print(f"Candidate: {key}, Language: {lang},\n")
#     stream.filter(track = getKeywords(candidates[key]), languages = lang, is_async=True)

search = getKeywords('Castillo')
stream.filter(track = search, languages = 'es')