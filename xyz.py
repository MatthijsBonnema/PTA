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
    ngramTagger(bigram_list)
    #entityTagger()


def ngramTagger(l):
    """
    This function takes a list of ngrams, creates bigrams and entity tags them.
    :param l: input must be a list of bigrams, formed in tuples
    :return: returns a list with words that are tagged. (For example, "El Salvador" would be [("El", "LOCATION"),
    ("Salvador", "LOCATION")]
    """
    bigrams_ner = []
    bigrams_wn = []
    bigrams = []
    tb = []
    for i in l:
        ngram_ner = i[0] + " " + i[1]
        ngram_wn = i[0] + "_" + i[1]
        bigrams_ner.append(ngram_ner)
        bigrams_wn.append(ngram_wn)
        bigrams.append((ngram_ner, ngram_wn))

    class3 = NERTagger('stanford-ner/classifiers/english.all.3class.distsim.crf.ser.gz',
                       'stanford-ner/stanford-ner.jar')
    tagged_bigrams = class3.tag(bigrams_ner)
    for l in tagged_bigrams:
        for t in l:
            if len(t[1]) > 3:
                if t[1] != "LOCATION":
                    tb.append(t)
    for bg in bigrams:
        tag_bg = bgWordNetTagger(bg[0], bg[1])
        if tag_bg == "COUNTRY" or tag_bg == "STATE" or tag_bg == "CITY" or tag_bg == "TOWN":
            words = bg[0].split()
            tb.extend([(words[0], tag_bg), (words[1], tag_bg)])
    print(tb)


def bgWordNetTagger(ner_word, wn_word):
    class3 = NERTagger('stanford-ner/classifiers/english.all.3class.distsim.crf.ser.gz',
                       'stanford-ner/stanford-ner.jar')
    tag_bigram = class3.tag([ner_word])
    if tag_bigram[0][0][1] == "LOCATION":
        if len(wordnet.synsets(wn_word, pos="n")) > 0:
            word = wordnet.synsets(wn_word, pos="n")[0]

            city = wordnet.synsets("City", pos="n")[0]
            state = wordnet.synsets("State", pos="n")[0]
            country = wordnet.synsets("Country", pos="n")[1]
            town = wordnet.synsets("Town", pos='n')[0]

            results = [("CITY", word.path_similarity(city)),
                       ("STATE", word.path_similarity(state)),
                       ("COUNTRY", word.path_similarity(country)),
                       ("TOWN", word.path_similarity(town))]

            sorted_scores = sorted(results, key=lambda tup: tup[1], reverse=True)

            return sorted_scores[0][0]
        else:
            return "-"
    return "-"


def tagChecker(fname, bl):
    """
    This function adds enitity tags to ngrams.
    :param fname: input must be a filename
    :param bl: must be a list of words which are tagged (preferably bigrams)
    :return:
    """
    with open(fname, "r") as inp_file:
        for line in inp_file:
            l = line.split()
            for t in bl:
                if t[0] == l[3]:
                    l[5] = t[1]


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
        "natural_places": wordnet.synsets("natural_places", pos='n'),
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
    return "-"


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
