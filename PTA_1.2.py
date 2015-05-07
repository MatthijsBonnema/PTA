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
    noun_synsets_relative = []
    noun_synsets_illness = []
    noun_synsets_science = []
    lemmatizer = WordNetLemmatizer()
    pos_tags = nltk.pos_tag(text)

    for word in pos_tags:
        if word[1] == "NN" or word[1] == "NNP":
            # print(word)
            noun_lemmas.append(lemmatizer.lemmatize(word[0], wordnet.NOUN))
            # get the synsets for the noun 'honey'
            word_synset = wordnet.synsets(word[0], pos="n")
            if len(word_synset) != 0 and len(relative) != 0 and len(science) != 0 and len(illness) != 0:
                if hypernymOf(word_synset[0], relative[0]):
                    noun_synsets_relative.append(word_synset)
                if hypernymOf(word_synset[0], illness[0]):
                    noun_synsets_illness.append(word_synset)
                if hypernymOf(word_synset[0], science[0]):
                    noun_synsets_science.append(word_synset)

    # Exercise 1.1
    print("EXERCISE 1.1\n")
    print("Relative: ", len(noun_synsets_relative))
    print("Illness: ", len(noun_synsets_illness))
    print("Science: ", len(noun_synsets_science))

    # Exercise 1.2
    print("\nEXERCISE 1.3\n")
    for word in pos_tags:
        if word[1] == "NN" or word[1] == "NNP":
            noun_lemmas.append(lemmatizer.lemmatize(word[0], wordnet.NOUN))
            for

    # Exercise 1.3
    print("\nEXERCISE 1.3\n")
    compare_words = [("car", "automobile"), ("coast", "shore"), ("food", "fruit"), ("journey", "car"),
                     ("monk", "slave"), ("moon", "string")]
    similarity_words = []
    for words in compare_words:
        w1synsets = wordnet.synsets(words[0], pos="n")
        w2synsets = wordnet.synsets(words[1], pos="n")
        similarity_words.append((words[0], words[1], getMaxSim(w1synsets, w2synsets)))
    similarity_words.sort(key=lambda tup: tup[2], reverse=True)
    for item in similarity_words:
        print("{:15}{:5}{:15}{:15}".format(item[0], "<>", item[1], item[2]))


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


def getMaxSim(synsets1, synsets2):
    maxSim = None
    for s1 in synsets1:
        for s2 in synsets2:
            sim = s1.lch_similarity(s2)
            if maxSim is None or maxSim < sim:
                maxSim = sim
    return maxSim

if __name__ == "__main__":
    main()