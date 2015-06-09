#!/usr/bin/python

import sys
from nltk.corpus import wordnet
import nltk
from collections import defaultdict
from nltk.tag.stanford import NERTagger

def main():
    text = []
    with open("en.tok.off.test", 'r') as filedata:
        for line in filedata:
            text.append(line.split())
        woorden = [token_data[3] for token_data in text]

        bigram_list = nltk.ngrams(woorden, 2)
    bigramTagger(bigram_list)
    #entityTagger()

def bigramTagger(l):
    bigrams = []
    tb = []
    for i in l:
        ngram = i[0] + " " + i[1]
        bigrams.append(ngram)

    class3 = NERTagger('stanford-ner/classifiers/english.all.3class.distsim.crf.ser.gz',
                       'stanford-ner/stanford-ner.jar')
    tagged_bigrams = class3.tag(bigrams)
    for l in tagged_bigrams:
        for t in l:
            if len(t[1]) > 3:
                tb.append(t)
    print(tb)



def posTagger(text_data):
    # Take the 4th column, the word
    tokens = [token_data[3] for token_data in text_data]
    tagged_tokens = nltk.pos_tag(tokens)
    for i in range(len(text_data)):
        text_data[i].append(tagged_tokens[i][1])
    output = open("en.tok.off.test.pos", "w")
    for i in text_data:
        data = ("{:4}{:4}{:6}{:20}{:3}".format(i[0], i[1], i[2], i[3], i[4]))
        output.write(data+"\n")
    output.close()

def entityTagger():
    class3 = NERTagger('stanford-ner/classifiers/english.all.3class.distsim.crf.ser.gz',
                       'stanford-ner/stanford-ner.jar')
    output = open("en.tok.off.test.pos.tagged", "w")
    with open("en.tok.off.test.pos", "r") as inp_file:
        for l in inp_file:
            line = l.split()
            print(line[3])
            if line[4] == "NN" or line[4] == "NNP":
                ner_tagged = class3.tag([line[3]])
                print("Nertagged:", ner_tagged)
                for t in ner_tagged[0]:
                    if len(t[1]) < 3:
                        tag = wordNetTagger(t[0])
                        print("Wordnet tag:", tag)
                        data = ("{:4}{:4}{:6}{:20}{:6}{:10}".format(line[0], line[1], line[2], line[3], line[4], tag))
                        output.write(data+"\n")
                    else:
                        data = ("{:4}{:4}{:6}{:20}{:6}{:10}".format(line[0], line[1], line[2], line[3], line[4], t[1]))
                        output.write(data+"\n")
    output.close()

def wordNetTagger(w):
    entities = {
        "country": wordnet.synsets("country", pos='n'),
        "state": wordnet.synsets("state", pos='n'),
        "city": wordnet.synsets("city", pos='n'),
        "town": wordnet.synsets("town", pos='n'),
        "natural_places": wordnet.synsets("natural places", pos='n'),
        "person": wordnet.synsets("person", pos='n'),
        "organisation": wordnet.synsets("organisation", pos='n'),
        "animal": wordnet.synsets("animal", pos='n'),
        "sport": wordnet.synsets("sport", pos='n'),
        "entertainment": wordnet.synsets("entertainment", pos='n'),
        }
    word_synset = wordnet.synsets(w, pos="n")
    for e in list(entities.keys()):
        if len(word_synset) != 0 and len(entities[e]) != 0:
            if hypernymOf(word_synset[0], entities[e][0]):
                return e
    return None

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
