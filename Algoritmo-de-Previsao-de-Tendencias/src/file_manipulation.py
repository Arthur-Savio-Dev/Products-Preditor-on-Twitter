from nltk.corpus import wordnet
from nltk.stem import PorterStemmer

bad_words = list()
good_words = list()
#corrigit leitura
with open('datas/bad_words.txt', 'r') as f:
    bad_words.append(f.readline().replace('\n', ''))
    while f.readline():
        bad_words.append(f.readline().replace('\n', ''))

with open('datas/good_words.txt', 'r') as f:
    good_words.append(f.readline().replace('\n', ''))
    while f.readline():
        good_words.append(f.readline().replace('\n', ''))

result1 = list()
result2 = list()

for i in bad_words:
    for syn in wordnet.synsets(i):
        for l in syn.lemmas():
            result1.append(l.name())

for i in good_words:
    for syn in wordnet.synsets(i):
        for l in syn.lemmas():
            result2.append(l.name())

ps = PorterStemmer()

for i in bad_words:
    result1.append(ps.stem(i))

for i in good_words:
    result2.append(ps.stem(i))

result1 = set(result1) #bad
result2 = set(result2) #good

with open('datas/synonym_bad_words.txt', 'w') as f:
    for i in result1:
        f.writelines(i + "\n")

with open('datas/synonym_good_words.txt', 'w') as f:
    for i in result2:
        f.writelines(i + '\n ')

