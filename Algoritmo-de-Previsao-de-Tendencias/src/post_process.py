from collections import defaultdict
import numpy as np
import matplotlib.pyplot as plt
from to_process_tweets import ProcessTweets
import matplotlib.pyplot as pyplot

class PostProcessTweets:
    def __init__(self, product):
        self.all_tweets = list()
        self.product = product
        self.pt = ProcessTweets(self.product)

    def sentiment_graphic(self):
        self.all_tweets = self.pt.calculate_sentiment(self.product)

        labels_list = ["Bad Sentiments", "Medium Sentiments", "Good Sentiments"]
        explode_list = [0, 0, 0.1]

        plt.axis('equal')
        plt.pie(self.all_tweets, labels = labels_list, autopct='%1.1f%%',
                    shadow = True, explode = explode_list)

        plt.title('Sentiment Frequency')
        plt.savefig('img/sentiment.png')
        plt.clf()

    def good_words_graphic(self):
        good_datas = list(self.pt.count_good.values())
        plt.bar(list(self.pt.count_good.keys()), good_datas, width=0.25, color='#007FFF')

        plt.savefig('img/good.png')
        plt.clf()

    def bad_words_graphic(self):
        bad_datas = list(self.pt.count_bad.values())
        plt.bar(list(self.pt.count_bad.keys()), bad_datas, width=0.25, color='#FF0000')

        plt.savefig('img/bad.png')
        plt.clf()

x = PostProcessTweets('ipad')
x.sentiment_graphic()
x.good_words_graphic()
x.bad_words_graphic() 