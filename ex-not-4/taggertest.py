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

def main():
    words = ["book", "car", "flower", "shower", "tower", "happiness"]

    entities = {
        "act": wordnet.synsets("act", pos='n'),
        "animal": wordnet.synsets("animal", pos='n'),
        "artifact": wordnet.synsets("artifact", pos='n'),
        "attribute": wordnet.synsets("attribute", pos='n'),
        "body": wordnet.synsets("body", pos='n'),
        "cognition": wordnet.synsets("cognition", pos='n'),
        "communication": wordnet.synsets("communication", pos='n'),
        "event": wordnet.synsets("event", pos='n'),
        "feeling": wordnet.synsets("feeling", pos='n'),
        "food": wordnet.synsets("food", pos='n'),
        "group": wordnet.synsets("group", pos='n'),
        "location": wordnet.synsets("location", pos='n'),
        "motive": wordnet.synsets("motive", pos='n'),
        "natural_object": wordnet.synsets("natural object", pos='n'),
        "natural_phenomenon": wordnet.synsets("natural object", pos='n'),
        "person": wordnet.synsets("person", pos='n'),
        "plant": wordnet.synsets("plant", pos='n'),
        "possession": wordnet.synsets("possession", pos='n'),
        "process": wordnet.synsets("process", pos='n'),
        "quantity": wordnet.synsets("quantity", pos='n'),
        "relation": wordnet.synsets("relation", pos='n'),
        "shape": wordnet.synsets("shape", pos='n'),
        "state": wordnet.synsets("state", pos='n'),
        "substance": wordnet.synsets("substance", pos='n'),
        "time": wordnet.synsets("time", pos='n')
    }

    noun_lemmas = []
    lemmatizer = WordNetLemmatizer()
    pos_tags = nltk.pos_tag(words)

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