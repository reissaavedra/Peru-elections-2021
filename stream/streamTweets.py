
import json
import csv
import pprint
from tweepy import StreamListener, Stream
import pprint
from utils import configTweepy
import os

# print(__package__)

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
fileName = os.path.join(path_data_stream, 'stream.csv')

class StreamListener(StreamListener):
    def on_status(self, status):
        # print(status)
        # print(status.__dict__.values())
        # tweetBatch = TweetBatch.TweetBatch(status._json)
        # print(tweetBatch.__dict__.values())
        with open(fileName, 'w') as file:
            try:
                writer = csv.writer(file, delimiter=',', quotechar='"', quoting=csv.QUOTE_MINIMAL)
                # writer.writerow(TweetBatch.TweetBatch.columns)
                tweetBatchStream = TweetBatch.TweetBatch(status._json)
                writer.writerow(tweetBatchStream.__dict__.values())
            except Exception as e:
                print('error')
    
                
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
stream.filter(track=["trump", "clinton", "hillary clinton", "donald trump"])



