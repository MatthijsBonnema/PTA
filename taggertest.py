#!/usr/bin/python
# File: PTA_1.2.py
# Author: Matthijs Bonnema
# Date: 4/30/15
# Info: 

import sys
from nltk.stem.wordnet import WordNetLemmatizer
from nltk.corpus import wordnet
import nltk
from collections import defaultdict
from nltk.tag.stanford import NERTagger


def main():
    words = ["book", "car", "flower", "shower", "tower", "happiness"]

    noun_lemmas = []
    nouns = []
    final_ner_tagged = []
    not_ner_tagged = []
    pos_tags = nltk.pos_tag(words)
    lemmatizer = WordNetLemmatizer()

    class3 = NERTagger('stanford-ner/classifiers/english.all.3class.distsim.crf.ser.gz',
                       'stanford-ner/stanford-ner.jar')

    # STANFORD NERTAGGING HAPPENS HERE
    for tag in pos_tags:
        if tag[1] == 'NNP':
            nouns.append(tag[0])
        elif tag[1] == 'NN':
            nouns.append(tag[0])

    ner_tagged = class3.tag(nouns)
    for t in ner_tagged[0]:
        if t[1] == u'O':
            not_ner_tagged.append(t[0])
        else:
            final_ner_tagged.append(t)
    print(final_ner_tagged)

    entities = {
        "COUNTRY": wordnet.synsets("country", pos='n'),
        "STATE": wordnet.synsets("state", pos='n'),
        "CITY": wordnet.synsets("city", pos='n'),
        "TOWN": wordnet.synsets("town", pos='n'),
        "NAT": wordnet.synsets("natural places", pos='n'),
        "PER": wordnet.synsets("person", pos='n'),
        "ORG": wordnet.synsets("organisation", pos='n'),
        "ANI": wordnet.synsets("animal", pos='n'),
        "SPO": wordnet.synsets("sport", pos='n'),
        "ENT": wordnet.synsets("entertainment", pos='n'),
    }

    print(pos_tags)

    tagged_top_entities = defaultdict(list)
    for word in pos_tags:
        if word[1] == "NN" or word[1] == "NNP":
            noun_lemmas.append(lemmatizer.lemmatize(word[0], wordnet.NOUN))
            word_synset = wordnet.synsets(word[0], pos="n")
            for e in list(entities.keys()):
                if len(word_synset) != 0 and len(entities[e]) != 0:
                    if hypernymOf(word_synset[0], entities[e][0]):
                        tagged_top_entities[word[0]].append(e)
    for w in tagged_top_entities:
        print("{:15}{:15}".format(w, tagged_top_entities[w]))


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