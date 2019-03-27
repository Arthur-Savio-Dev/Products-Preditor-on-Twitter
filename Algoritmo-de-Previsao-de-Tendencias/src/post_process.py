from src.mysql_connector import MySqlOperator
from collections import defaultdict

import numpy as np
from src.to_process_tweets import ProcessTweets
import matplotlib.pyplot as pyplot

class PostProcessTweets:
    def __init__(self, table):
        self.all_tweets = list()
        self.table = table

    def generate_graphic(self):
        pt = ProcessTweets()
        self.all_tweets = pt.calculate_sentiment(self.table)

        labels_list = ["Bad Sentiments", "Medium Sentiments", "Good Sentiments"]
        explode_list = [0, 0.1, 0]

        pyplot.axis('equal')
        pyplot.pie(self.all_tweets, labels = labels_list, autopct='%1.1f%%',
                    shadow = True, explode = explode_list)

        pyplot.title('Sentiment Frequency')
        pyplot.show()
