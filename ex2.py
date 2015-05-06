#!/usr/bin/python
from nltk.tag.stanford import NERTagger
import nltk


def main():
    file = open("ada_lovelace.txt", 'r')
    file = file.read()
    file = file.decode('utf-8')
    text = nltk.word_tokenize(file)

    # Location, Person, Organization
    class3 = NERTagger('stanford-ner/classifiers/english.all.3class.distsim.crf.ser.gz',
                   'stanford-ner/stanford-ner.jar')
    class3_nowiki = NERTagger('stanford-ner/classifiers/english.nowiki.3class.distsim.crf.ser.gz',
                   'stanford-ner/stanford-ner.jar')

    # Location, Person, Organization, Misc
    class4 = NERTagger('stanford-ner/classifiers/english.conll.4class.distsim.crf.ser.gz',
               'stanford-ner/stanford-ner.jar')

    # Time, Location, Organization, Person, Money, Percent, Date
    class7 = NERTagger('stanford-ner/classifiers/english.muc.7class.distsim.crf.ser.gz',
               'stanford-ner/stanford-ner.jar')


    words = []

    pos_tags = nltk.pos_tag(text)
    for tag in pos_tags:
        if tag[1] == 'NNP':
            words.append(tag[0])
    print(class3.tag(words))



    # print(class3.tag(text))



main()