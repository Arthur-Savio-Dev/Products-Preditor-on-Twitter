from initialize_api import InitializeTwitterApi
from post_process import PostProcessTweets
from to_process_tweets import ProcessTweets
from read_twitter import MyListener

if __name__ == '__main__':
    api = InitializeTwitterApi('Donald Trump', 1000)
    api.set_access_api_keys()