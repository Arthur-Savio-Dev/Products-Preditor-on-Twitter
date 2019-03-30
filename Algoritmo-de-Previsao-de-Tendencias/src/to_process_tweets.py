import re
import string
import operator
from collections import Counter
from textblob import TextBlob
from mysql_connector import MySqlOperator
from collections import defaultdict
from nltk.corpus import wordnet

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
        self.punctuation = list(string.punctuation)
        self.stop = list()
        self.tokens = list()
        self.product = product
        self.terms_only = list()
        self.terms_hash = list()
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

        for i in self.punctuation:
            self.stop.append(i)
        self.stop.append('…')
        self.stop.append('RT')
        self.stop.append('I')

    def read_datas_to_generate_tokens(self):
        sql = MySqlOperator()
        result = sql.select_tweets_from_table(self.product)

        for i in result:
            string = ''.join(map(str, i))
            token = self.pre_process(string)
            for term in token:
                self.tokens.append(term)

    def deep_cleaning(self):
        pass

    def count_commom_datas(self):
        self.terms_hash = [term for term in self.tokens if term.startswith('#')]
        self.terms_only = [term for term in self.tokens if term not in self.stop and not term.startswith(('#', '@'))]

        for term in self.terms_only:
            if term.lower() == self.product.lower():
                self.terms_only.remove(term)

        count_all = Counter()
        count_all.update(self.terms_only)
        return count_all.most_common(5)

    """def calculate_sentiment(self, table):
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
"""
    #incrementar essas listas
    """def calculate_sentiment(self):
        positive_vocab = [
            'good', 'nice', 'great', 'awesome', 'outstanding',
            'fantastic', 'terrific', ':)', ':-)', 'like', 'love',
        ]
        negative_vocab = [
            'bad', 'terrible', 'crap', 'useless', 'hate', ':(', ':-(',
        ]

        p_t = {}
        p_t_com = defaultdict(lambda : defaultdict(int))
        pmi = defaultdict(lambda : defaultdict(int))

        for term, n in 

        for t1 in"""

    def calculate_frequency(self):
        com = defaultdict(lambda: defaultdict(int))
        com_max = list()

        # Build co-occurrence matrix
        for i in range(len(self.terms_only) - 1):
            for j in range(i + 1, len(self.terms_only)):
                w1, w2 = sorted([self.terms_only[i], self.terms_only[j]])
                if w1 != w2:
                    com[w1][w2] += 1

        # For each term, look for the most common co-occurrent terms
        for t1 in com:
            t1_max_terms = sorted(com[t1].items(), key=operator.itemgetter(1), reverse=True)[:5]
            for t2, t2_count in t1_max_terms:
                com_max.append(((t1, t2), t2_count))
        terms_max = sorted(com_max, key=operator.itemgetter(1), reverse=True)
        print(terms_max[:5])