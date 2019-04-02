import json
from tweepy.streaming import StreamListener
from mysql_connector import MySqlOperator

class MyListener(StreamListener):
    def __init__(self, term_to_search, limit):
        super().__init__()
        self.counter = 0
        self.limit = limit
        self.term_to_search = term_to_search
        self.mysql_operator = MySqlOperator()
        self.mysql_operator.check_existing_table(term_to_search)

    def on_data(self, data):
        try:
            datas = {"user":"", "text":"", "location":""}
            all_data = json.loads(data)
            datas['user'] = all_data["user"]["screen_name"]
            datas['text'] = all_data["text"]
            datas['location'] = all_data["user"]["location"]

            self.mysql_operator.insert_table(self.term_to_search, datas['user'], datas['text'], datas['location'])
            self.counter += 1

            print(self.counter)
            if self.counter < self.limit:
                return True
            else:
                self.mysql_operator.commit_table()
                self.mysql_operator.close_database_connection()
                return False
        except BaseException as e:
            print("Error on_data: %s" % str(e))

    def on_error(self, status):
        print(status)
        return True
