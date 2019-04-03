import re
import string
from textblob import TextBlob
from mysql_connector import MySqlOperator
from nltk.corpus import stopwords
from post_process import PostProcessTweets

class ProcessTweets:
    def __init__(self, product):
        self.emoticons_str = r"""
            (?:
                [:=;] # Eyes
                [oO\-]? # Nose (optional)
                [D\)\]\(\]/\\OpP] # Mouth
            )"""
        self.regex_str = [
            self.emoticons_str,
            r'<[^>]+>', # HTML tags
            r'(?:@[\w_]+)', # @-mentions
            r"(?:\#+[\w_]+[\w\'_\-]*[\w_]+)", # hash-tags
            r'http[s]?://(?:[a-z]|[0-9]|[$-_@.&amp;+]|[!*\(\),]|(?:%[0-9a-f][0-9a-f]))+', # URLs
            r'(?:(?:\d+,?)+(?:\.?\d+)?)', # numbers
            r"(?:[a-z][a-z'\-_]+[a-z])", # words with - and '
            r'(?:[\w_]+)', # other words
            r'(?:\S)' # anything else
        ]
        self.tokens_re = re.compile(r'('+'|'.join(self.regex_str)+')', re.VERBOSE | re.IGNORECASE)
        self.emoticon_re = re.compile(r'^'+self.emoticons_str+'$', re.VERBOSE | re.IGNORECASE)
        self.stop = list()
        self.tokens = list()
        self.product = product
        self.terms_only = list()
        self.terms_hash = list()
        self.bad_words = list()
        self.good_words = list()
        self.count_bad = dict()
        self.count_good = dict()
        self.good_words = list()
        self.bad_words = list()
        self.all_tweets = list()
        self.sentiment_datas = [0 for i in range(0, 3)]
        self.initialize_process()

    def initialize_process(self):
        self.calculate_sentiment()
        self.generate_stop_words()
        self.read_datas_to_generate_tokens()
        self.generate_clean_tokens()
        self.read_bad_and_good_words()
        self.count_commom_datas()

        ppt = PostProcessTweets(self.count_good, self.count_bad, self.sentiment_datas)
        ppt.generate_all_graphics()

    def tokenize(self, s):
        return self.tokens_re.findall(s)

    def pre_process(self, s, lowercase=False):
        tokens = self.tokenize(s)
        if lowercase:
            tokens = [token if self.emoticon_re.search(token) else token.lower() for token in tokens]
        return tokens

    def generate_stop_words(self):
        self.stop = stopwords.words('english') + list(string.punctuation) + ['rt', 'RT', 'via', 'I', '...', '…', '’']

    def read_datas_to_generate_tokens(self):
        sql = MySqlOperator(self.product)
        result = sql.select_tweets_from_table()

        for i in result:
            string = ''.join(map(str, i))
            token = self.pre_process(string)
            for term in token:
                self.tokens.append(term)

    def generate_clean_tokens(self):
        self.terms_hash = [term for term in self.tokens if term.startswith('#')]
        self.terms_only = [term for term in self.tokens if term not in self.stop and not term.startswith(('#', '@'))]

    def count_commom_datas(self):
        gw = set(self.good_words)
        bw = set(self.bad_words)

        for i in self.terms_only:
            if i in gw:
                if self.count_good.get(i) is None:
                    self.count_good[i] = 1
                else:
                    self.count_good[i] += 1
            if i in bw:
                if self.count_bad.get(i) is None:
                    self.count_bad[i] = 1
                else:
                    self.count_bad[i] += 1

    def calculate_sentiment(self):
        twittes_score = list()
        self.all_tweets = MySqlOperator(self.product).select_all_datas_from_table()

        for i in self.all_tweets:
            analysis = TextBlob(str(i))
            polarity = analysis.sentiment.polarity
            twittes_score.append(polarity)

        for j in twittes_score:
            if j < 0:
                self.sentiment_datas[0] += 1
            elif j == 0:
                self.sentiment_datas[1] += 1
            else:
                self.sentiment_datas[2] += 1

    def read_bad_and_good_words(self):
        with open('../datas/synonym_good_words.txt', 'r') as f:
            self.good_words.append(f.readline().replace('\n', ''))
            while f.readline():
                self.good_words.append(f.readline().replace('\n', ''))

        with open('../datas/synonym_bad_words.txt', 'r') as f:
            self.bad_words.append(f.readline().replace('\n', ''))
            while f.readline():
                self.bad_words.append(f.readline().replace('\n', ''))
