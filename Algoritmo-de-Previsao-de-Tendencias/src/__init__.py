from initialize_api import InitializeTwitterApi
from post_process import PostProcessTweets
from to_process_tweets import ProcessTweets
from read_twitter import MyListener

if __name__ == '__main__':

    #api = InitializeTwitterApi(i, 200)
    #api.set_access_api_keys()

    process = ProcessTweets('ipad')
    process.read_datas_to_generate_tokens()
    process.generate_clean_tokens()
    process.calculate_frequency()

    #post_process_twitter = PostProcessTweets('ipad')
    #post_process_twitter.generate_graphic()

