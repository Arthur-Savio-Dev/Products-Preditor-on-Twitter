from src.initialize_api import InitializeTwitterApi
from src.post_process import PostProcessTweets


if __name__ == '__main__':
    api = InitializeTwitterApi()
    api.set_access_api_keys()

    post_process_twitter = PostProcessTweets('ipad')
    post_process_twitter.generate_graphic()