import time

class TweetBatch:
    columns = [
        'created_at',
        'id_str',
        'text',
        'source',
        'user_id_str',
        'user_name',
        'user_location',
        'user_url',
        'user_protected',
        'user_followers_count',
        'user_friends_count',
        'user_favourites_count',
        'user_lang',
        'geo',
        'coordinates',
        'favorite_count',
        'place',
        'favorited',
        'retweet_count',
        'retweeted',
        'lang',
    ]

    def __init__(self, tweet):        
        self.created_at =  time.strftime('%Y-%m-%d %H:%M:%S', time.strptime(tweet['created_at'],'%a %b %d %H:%M:%S +0000 %Y'))
        self.id_str = tweet['id_str']
        self.text = tweet['text']
        self.source = tweet['source']
        self.user_id_str = tweet['user']['id_str']
        self.user_name = tweet['user']['name']
        self.user_location = tweet['user']['location']
        self.user_url = tweet['user']['url']
        self.user_protected = tweet['user']['protected']
        self.user_followers_count = tweet['user']['followers_count']
        self.user_friends_count = tweet['user']['friends_count']
        self.user_favourites_count = tweet['user']['favourites_count']
        self.user_lang = tweet['user']['lang']
        self.geo = tweet['geo']
        self.coordinates = tweet['coordinates']
        self.favorite_count = tweet['favorite_count']
        self.place = tweet['place']
        self.favorited = tweet['favorited']
        self.retweet_count = tweet['retweet_count']
        self.retweeted = tweet['retweeted']
        self.lang = tweet['lang']

    def toList(self):
        return list(self.__dict__.values())
