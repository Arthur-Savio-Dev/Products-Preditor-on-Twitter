import tweepy
from tweepy import OAuthHandler
from tweepy import Stream
from read_twitter import MyListener

class InitializeTwitterApi:
    def __init__(self, product, limit):
        self.consumer_key = "ao65rICjuJmrW9iGWlMpVDDRc"
        self.consumer_secret = "ZLgdiYjz5hTtAfFsBeT9MkudbjLs3BmQF8YAU5fPNcOY1SqsGQ"
        self.access_token = "1090611131213905922-e7vY6lrIj4D3CKHb7sBJQrxpK3gjZX"
        self.access_token_secret = "iVVFbRQLCWsHsNVXqDg8c0Mde1HQR4rczXmuReUTExtKo"
        self.auth = None
        self.api = None
        self.limit = limit
        self.product = product

    def set_access_api_keys(self):
        self.auth = OAuthHandler(self.consumer_key, self.consumer_secret)
        self.auth.set_access_token(self.access_token, self.access_token_secret)
        self.api = tweepy.API(self.auth)
        self.receive_informations_to_init_read_api()

    def receive_informations_to_init_read_api(self):
        self.init_read_api(self.product, self.limit)

    def init_read_api(self, term_to_search, number_of_tweets):
        print(" - Please wait, we are working for find your results... -\n\n")
        receive_my_listener = MyListener(term_to_search, number_of_tweets)
        twitter_stream = Stream(self.auth, receive_my_listener)
        twitter_stream.filter(track=[term_to_search], languages=["en"])
        twitter_stream.disconnect()