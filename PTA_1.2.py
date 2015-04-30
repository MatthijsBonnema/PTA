#!/usr/bin/python
# File: PTA_1.2.py
# Author: Matthijs Bonnema
# Date: 4/30/15
# Info: 

import sys
from nltk.stem.wordnet import WordNetLemmatizer
from nltk.corpus import wordnet
import nltk

def main():
    file = open("ada_lovelace.txt", 'r')
    file = file.read()
    file = file.decode('utf-8')
    text = nltk.word_tokenize(file)

    # print(file)

    nouns = []
    lemmatizer = WordNetLemmatizer()


    pos_tags = nltk.pos_tag(text)
    # print(pos_tags)

    for word in pos_tags:
        if word[1] == "NN" or word[1] == "NNP":
            print(word)
            nouns.append(lemmatizer.lemmatize(word[0], wordnet.VERB))


    print(nouns)


if __name__ == "__main__":
    main()