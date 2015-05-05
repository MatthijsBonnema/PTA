#!/usr/bin/python
from nltk.tag.stanford import NERTagger
import nltk


def main():
    file = open("ada_lovelace.txt", 'r')
    file = file.read()
    file = file.decode('utf-8')
    text = nltk.word_tokenize(file)
    test = NERTagger('/usr/share/stanford-ner/classifiers/english.all.3class.distsim.crf.ser.gz',
                   '/usr/share/stanford-ner/stanford-ner.jar')
    print(test.tag(text))



main()