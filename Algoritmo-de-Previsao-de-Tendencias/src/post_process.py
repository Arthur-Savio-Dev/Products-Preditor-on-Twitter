from mysql_connector import MySqlOperator
from collections import defaultdict

import numpy as np
from to_process_tweets import ProcessTweets
import matplotlib.pyplot as pyplot

class PostProcessTweets:
    def __init__(self, product):
        self.all_tweets = list()
        self.product = product

    def sentiment_graphic(self):
        pt = ProcessTweets(self.product)
        self.all_tweets = pt.calculate_sentiment(self.product)

        labels_list = ["Bad Sentiments", "Medium Sentiments", "Good Sentiments"]
        explode_list = [0, 0, 0.1]

        pyplot.axis('equal')
        pyplot.pie(self.all_tweets, labels = labels_list, autopct='%1.1f%%',
                    shadow = True, explode = explode_list)

        pyplot.title('Sentiment Frequency')
        pyplot.show()

    # Implementar gráfico para palavras mais comuns, localização, controle do termo de pesquisa, melhorar o gráfico do sentimentos
    # exibir gŕafico com os melhores produtos relacionados