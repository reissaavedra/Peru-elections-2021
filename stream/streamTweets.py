import json
import csv
import pprint
from tweepy import StreamListener

class StreamListener(StreamListener):
    def on_status(self, status):
        print(status.text)

    def on_error(self, status_code):
        if status_code == 420:
            return False


# while True:
#         r = api.request('statuses/filter',
#                         {'locations': '-77.2694,-12.4735,-76.6624,-11.6721'})  # Coordenadas para Perú
#         with open("JSONTwitter.csv", "a") as ed:  # "a", si existe el archivo le hace append.
#             for item in r:  # r -> Es el JSON de Twitter #item-> es cada tweet(row)
#
#                 try:
#                     writer = csv.writer(ed, delimiter=',', quotechar='"', quoting=csv.QUOTE_MINIMAL)
#                     writer.writerow(item)
#                 except Exception as e:
#                     print(e)
#                     item
#
#                 pprint.pprint(item)

stream_listener = StreamListener()
stream = tweepy.Stream(auth=api.auth, listener=stream_listener)
stream.filter(track=["trump", "clinton", "hillary clinton", "donald trump"])