import re
import string
from collections import Counter
from textblob import TextBlob
from src.mysql_connector import MySqlOperator
from collections import defaultdict

class ProcessTweets:
    def __init__(self):
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
        self.punctuation = list(string.punctuation)
        self.stop = list()
        self.tokens = list()
        self.read_stop_words_from_file()

    def tokenize(self, s):
        return self.tokens_re.findall(s)
 
    def pre_process(self, s, lowercase=False):
        tokens = self.tokenize(s)
        if lowercase:
            tokens = [token if self.emoticon_re.search(token) else token.lower() for token in tokens]
        return tokens

    def read_stop_words_from_file(self):
        with open('datas/stop_words.txt', 'r') as f:
            self.stop.append(f.readline().replace('\n', ''))
            while f.readline():
                self.stop.append(f.readline().replace('\n', ''))
        self.stop.append(self.punctuation + ['rt', 'via'])

    def read_datas_to_generate_tokens(self, table):
        sql = MySqlOperator()
        result = sql.select_tweets_from_table(table)

        for i in result:
            for k in i:
                k = k.replace('\n', '')
                self.tokens.append([term for term in self.pre_process(k) if term not in self.stop])

    def count_commom_datas(self):
        count_all = Counter()
        for i in self.tokens:
            count_all.update(i)
        return count_all.most_common(5)

    def calculate_sentiment(self, table):
        twittes_score = list()
        all_tweets = MySqlOperator().select_all_datas_from_table(table)
        sentimets_datas = [0 for i in range(0, 3)]

        for i in all_tweets:
            analysis = TextBlob(str(i))
            polarity = analysis.sentiment.polarity
            twittes_score.append(polarity)

        for j in twittes_score:
            if j <= -0.5:
                sentimets_datas[0] += 1
            elif j > -0.5 and j <= 0.5:
                sentimets_datas[1] += 1
            else:
                sentimets_datas[2] += 1
        return sentimets_datas

    def calculate_frequency(self, table):
        all_tweets = MySqlOperator().select_all_datas_from_table(table)
        com = defaultdict(lambda: defaultdict(int))

        terms_only = [term for term in self.pre_process(all_tweets)
                      if term not in self.stop and not term.startwith(('#', '@'))]

        for i in range(len(terms_only) - 1):
            for j in range(i + 1, len(terms_only)):
                w1, w2 = sorted([terms_only[i], terms_only[j]])
                if w1 != w2:
                    com[w1][w2] += 1
