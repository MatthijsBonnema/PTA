#!/usr/bin/python3
# File: test.py
# Author: Matthijs Bonnema
# Date: 4/16/15
# Info:

import sys
import nltk
from collections import Counter

def main():
    br_tw = nltk.corpus.brown.tagged_words(categories='mystery')
    br_ts = nltk.corpus.brown.tagged_sents(categories='mystery')
    words = nltk.corpus.brown.words(categories='mystery')
    sents = nltk.corpus.brown.raw(categories='mystery')


    # Opdracht A en B en C:
    #
    # tags = []
    # for tag in br_tw:
    #     tags.append(tag[1])
    #
    # tags2 = []
    #
    # for e in tags:
    #     if e not in tags2:
    #         tags2.append(e)
    # print(tags2[99])
    # print(len(tags2))


    # Opdracht D en E
    # l = []
    #
    # br_tw_freq = nltk.FreqDist(br_tw)
    # for b,f in br_tw_freq.items():
    #     tag = (b,f)
    #     l.append(tag)
    #     l.sort(key=lambda tup: tup[1])
    # print(l[-9:])

    # # Opdracht F en G:
    # #
    # l = []
    #
    # freq = nltk.FreqDist(br_tw)
    # for b in br_tw:
    #     # b = nltk.str2tuple(str(b))
    #     if b[1] == (u'JJ'):
    #         l.append(b[0])
    # c = Counter(l)
    # print(c.most_common(10))

    # Opdracht H en I
    #
    # l = []
    #
    # freq = nltk.FreqDist(br_tw)
    # for b in br_tw:
    #     # b = nltk.str2tuple(str(b))
    #     if b[0] == (u'so'):
    #         print(b[0])
    #         l.append(b[1])
    # print(l)
    # c = Counter(l)
    # print(c.most_common())
    #
    # Opdracht J en K
    #
    # print(nltk.pos_tag(text))
    # tokens = []
    # sents = nltk.sent_tokenize(sents)
    #
    # for sent in sents:
    #     tokens += nltk.word_tokenize(sent)
    # text = nltk.Text(tokens)
    # for lines in tokens:
    #     print(lines.concordance(" u'so/ql'"))
    # l = []

    # bigrams = nltk.bigrams(words)
    # fdist = nltk.FreqDist(bigrams)
    # for b,f in fdist.items():
    #     tag = (b,f)
    #     l.append(tag)
    # l.sort(key=lambda tup: tup[1], reverse=True)
    # print(l)
    #
    # words = []
    #
    # Opdracht 3
    #
    # t = nltk.FreqDist(words)
    # print(t.tabulate(10))
    # file = open("holmes.txt", 'r')
    # file = file.read()
    # file = file.decode('utf-8')
    # text = nltk.word_tokenize(file)



if __name__ == "__main__":
    main()
