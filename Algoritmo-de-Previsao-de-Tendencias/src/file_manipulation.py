from nltk.corpus import wordnet

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

for i in bad_words:
    for syn in wordnet.synsets(i):
        for l in syn.lemmas():
            result1.append(l.name())

print(set(result1))