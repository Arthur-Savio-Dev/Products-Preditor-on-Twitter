from initialize_api import InitializeTwitterApi
from post_process import PostProcessTweets
from to_process_tweets import ProcessTweets
from read_twitter import MyListener

if __name__ == '__main__':

    #api = InitializeTwitterApi(i, 200)
    #api.set_access_api_keys()

    """process = ProcessTweets('ipad')
    process.read_datas_to_generate_tokens()
    process.generate_clean_tokens()
    process.count_commom_datas()"""

    post_process_twitter = PostProcessTweets('ipad')
    post_process_twitter.sentiment_graphic()

