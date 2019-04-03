import matplotlib.pyplot as plt

class PostProcessTweets:
    def __init__(self, count_good, count_bad, sentiment_datas):
        self.sentiment_datas = sentiment_datas
        self.count_good = count_good
        self.count_bad = count_bad

    def generate_all_graphics(self):
        self.sentiment_graphic()
        self.good_words_graphic()
        self.bad_words_graphic()

    def sentiment_graphic(self):
        labels_list = ["Bad Sentiments", "Medium Sentiments", "Good Sentiments"]
        explode_list = [0, 0, 0.1]

        plt.axis('equal')
        plt.pie(self.sentiment_datas, labels = labels_list, autopct='%1.1f%%',
                shadow = True, explode = explode_list)

        plt.title('Sentiment Frequency')
        plt.savefig('../img/sentiment.png')
        plt.clf()

    def good_words_graphic(self):
        plt.barh(list(self.count_good.keys()), list(self.count_good.values()),  color='#007FFF')
        plt.savefig('../img/good.png')
        plt.clf()

    def bad_words_graphic(self):
        plt.barh(list(self.count_bad.keys()), list(self.count_bad.values()), color='#FF0000')
        plt.savefig('../img/bad.png')
        plt.clf()
