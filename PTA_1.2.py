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
    noun_synsets_relative =[]
    noun_synsets_illness =[]
    noun_synsets_science =[]
    lemmatizer = WordNetLemmatizer()
    pos_tags = nltk.pos_tag(text)

    for word in pos_tags:
        if word[1] == "NN" or word[1] == "NNP":
            # print(word)
            noun_lemmas.append(lemmatizer.lemmatize(word[0], wordnet.VERB))
            # get the synsets for the noun 'honey'
            word_synset = wordnet.synsets(word[0], pos="n")
            if len(word_synset) != 0 and len(relative) != 0 and len(science) != 0 and len(illness) != 0:
                if hypernymOf(word_synset[0], relative[0]):
                    noun_synsets_relative.append(word_synset)
                if hypernymOf(word_synset[0], illness[0]):
                    noun_synsets_illness.append(word_synset)
                if hypernymOf(word_synset[0], science[0]):
                    noun_synsets_science.append(word_synset)
    # # print(noun_lemmas)
    #
    # print(noun_synsets_relative)
    # print(noun_synsets_illness)
    # print(noun_synsets_science)

    print("Relative: ", len(noun_synsets_relative))
    print("Illness: ", len(noun_synsets_illness))
    print("Science: ", len(noun_synsets_science))


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

if __name__ == "__main__":
    main()