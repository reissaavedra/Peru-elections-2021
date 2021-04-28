import fastavro
from io import BytesIO

class TweetBatch:
    columns = [
        'created_at',
        'contributors',
        'coordinates',
        'favorited',
        'favorite_count',
        'geo',
        'id_str',
        'in_reply_to_screen_name',
        'in_reply_to_user_id',
        'in_reply_to_status_id',
        'is_quote_status',
        'lang',
        'place',
        'retweet_count',
        'retweet_count',
        'retweeted',
        'source',
        'text',
        'truncated',
        'user',
        'entities',
        'metadata',
    ]

    def __init__(self, tweet):
        self.created_at = tweet['created_at']
        self.contributors = tweet['contributors']
        self.coordinates = tweet['coordinates']
        self.favorited = tweet['favorited']
        self.favorite_count = tweet['favorite_count']
        self.geo = tweet['geo']
        self.id_str = tweet['id_str']
        self.in_reply_to_screen_name = tweet['in_reply_to_screen_name']
        self.in_reply_to_user_id = tweet['in_reply_to_user_id']
        self.in_reply_to_status_id = tweet['in_reply_to_status_id']
        self.is_quote_status = tweet['is_quote_status']
        self.lang = tweet['lang']
        self.place = tweet['place']
        # self.retweeted_status = tweet['retweeted_status']
        self.retweet_count = tweet['retweet_count']
        self.retweeted = tweet['retweeted']
        self.source = tweet['source']
        # self.source_url = tweet['source_url']
        self.text = tweet['text']
        self.truncated = tweet['truncated']
        # self.user = tweet['user']
        # self.entities = tweet['entities']
        # self.metadata = tweet['metadata']

    def toAvro(self, schema):
        buf = BytesIO()
        fastavro.writer(buf, schema, [self.__dict__])
        message = buf.getvalue()
        return message

    def toList(self):
        return list(self.__dict__.values())
