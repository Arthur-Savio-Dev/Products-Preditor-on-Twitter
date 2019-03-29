from initialize_api import InitializeTwitterApi
from post_process import PostProcessTweets
from to_process_tweets import ProcessTweets

if __name__ == '__main__':
    #api = InitializeTwitterApi()
    #api.set_access_api_keys()

    process = ProcessTweets()
    process.read_datas_to_generate_tokens('ipad')
    print(process.count_commom_datas())

    #post_process_twitter = PostProcessTweets('ipad')
    #post_process_twitter.generate_graphic()

