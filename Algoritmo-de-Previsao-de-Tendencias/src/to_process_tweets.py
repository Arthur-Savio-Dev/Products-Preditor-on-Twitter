import re
import string
import operator
from collections import Counter
from textblob import TextBlob
from mysql_connector import MySqlOperator
from collections import defaultdict
from nltk.corpus import wordnet, stopwords

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
        self.count_bad = Counter()
        self.count_good = Counter()
        self.good_words = list()
        self.bad_words = list()
        self.generate_stop_words()
        self.read_bad_and_good_words()

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
        sql = MySqlOperator()
        result = sql.select_tweets_from_table(self.product)

        for i in result:
            string = ''.join(map(str, i))
            token = self.pre_process(string)
            for term in token:
                self.tokens.append(term)

    def generate_clean_tokens(self):
        self.terms_hash = [term for term in self.tokens if term.startswith('#')]
        self.terms_only = [term for term in self.tokens if term not in self.stop and not term.startswith(('#', '@'))]

    def count_commom_datas(self):
        for i in self.terms_only:
            if i in self.good_words:
                self.count_good.update(self.good_words)
            if i in self.bad_words:
                self.count_bad.update(self.bad_words)

    def calculate_sentiment(self, table):
        twittes_score = list()
        all_tweets = MySqlOperator().select_all_datas_from_table(table)
        sentimets_datas = [0 for i in range(0, 3)]

        for i in all_tweets:
            analysis = TextBlob(str(i))
            polarity = analysis.sentiment.polarity
            twittes_score.append(polarity)

        for j in twittes_score:
            if j < 0:
                sentimets_datas[0] += 1
            elif j == 0:
                sentimets_datas[1] += 1
            else:
                sentimets_datas[2] += 1
        return sentimets_datas

    def read_bad_and_good_words(self):
        with open('datas/synonym_good_words.txt', 'r') as f:
            self.good_words.append(f.readline().replace('\n', ''))
            while f.readline():
                self.good_words.append(f.readline().replace('\n', ''))

        with open('datas/synonym_bad_words.txt', 'r') as f:
            self.bad_words.append(f.readline().replace('\n', ''))
            while f.readline():
                self.bad_words.append(f.readline().replace('\n', ''))

