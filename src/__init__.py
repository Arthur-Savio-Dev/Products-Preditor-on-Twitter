from initialize_api import InitializeTwitterApi
from to_process_tweets import ProcessTweets

def main(product, limit):
    api = InitializeTwitterApi(product, limit)
    api.set_access_api_keys()
    pt = ProcessTweets(product)
    pt.initialize_process()

if __name__ == '__main__':

    main('Avenger', 100)