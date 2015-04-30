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
    relative = wordnet.synsets("relative", pos='n')
    science = wordnet.synsets("science", pos='n')
    illness = wordnet.synsets("illness", pos='n')

    noun_lemmas = []
    noun_synsets =[]
    lemmatizer = WordNetLemmatizer()
    pos_tags = nltk.pos_tag(text)

    for word in pos_tags:
        if word[1] == "NN" or word[1] == "NNP":
            print(word)
            noun_lemmas.append(lemmatizer.lemmatize(word[0], wordnet.VERB))
            # get the synsets for the noun 'honey'
            word_synset = wordnet.synsets(word[0], pos="n")
            if hypernymOf(word_synset[0], relative[0]):
                noun_synsets.append(word_synset)



def hypernymOf(synset1, synset2):
    """ Returns True if synset2 is a hypernym of
    synset1, or if they are the same synset.
    Returns False otherwise. """

    if synset1 == synset2:
        return True
    for hypernym in synset1.hypernyms():
        if synset2 == hypernym:
            return True
        if hypernymOf(hypernym, synset2):
            return True

    print(noun_lemmas)
    print(noun_synsets)




if __name__ == "__main__":
    main()