#!/usr/bin/python
# Date: 5/28/15

import sys
import wikipedia
from nltk.stem.wordnet import WordNetLemmatizer
from nltk.corpus import wordnet
import nltk
from collections import defaultdict
from nltk.tag.stanford import NERTagger


def main(argv):
    result_word_syn_list = []
    result_synset_list = []
    result_list = wikipedia.search("President")
    print(result_list)
    for result in result_list:
        # print(result, wikipedia.summary(result), "\n")

        try:
            result_word_syn_list.append((result, wikipedia.summary(result, sentences=2)))
        except wikipedia.exceptions.DisambiguationError as e:
            for result_e in e:
                result_word_syn_list.append((result_e, wikipedia.summary(result, sentences=2)))

    # for line in result_word_syn_list:
    #     print(line)


    for i in result_word_syn_list:
        # print(i[0] + "\n" + i[1])
        words = i[0].split(" ")
        for word in words:
            print(word)
            print(i[1])
            ss = lesk(i[1], word, "n")
            print(ss)
            try:
                print(str((ss, ss.definition())) + "\n")
            except AttributeError:
                print(str((word, "No definition")))
            # outputwrite = str((ss, ss.definition())) + "\n"
            # output.write(outputwrite)



    # print(result_synset_list)



def posTagger(text_data):
    # Take the 4th column, the word
    tokens = [token_data[3] for token_data in text_data]
    tagged_tokens = nltk.pos_tag(tokens)
    for i in range(len(text_data)):
        text_data[i].append(tagged_tokens[i][1])
    output = open("en.tok.off.pos", "w")
    for i in text_data:
        data = ("{:4}{:4}{:6}{:20}{:3}".format(i[0], i[1], i[2], i[3], i[4]))
        output.write(data+"\n")
    output.close()


def nertagger(fname):
    class3 = NERTagger('stanford-ner/classifiers/english.all.3class.distsim.crf.ser.gz',
                       'stanford-ner/stanford-ner.jar')
    output = open("en.tok.off.pos.tagged", "w")
    with open(fname, "r") as inp_file:
        for l in inp_file:
            line = l.split()
            if line[4] == "NN" or line[4] == "NNP":
                ner_tagged = class3.tag(line[3])
                print(ner_tagged)
                for t in ner_tagged:
                    if t[1] == u'O':
                        #WordNet tagging
                        tag = wordNetTagger(t[0])
                        data = ("{:4}{:4}{:6}{:20}{:3}{:10}".format(line[0], line[1], line[2], line[3], line[4], tag))
                        output.write(data+"\n")
                    else:
                        data = ("{:4}{:4}{:6}{:20}{:3}{:10}".format(line[0], line[1], line[2], line[3], line[4], t[1]))
                        output.write(data+"\n")
    output.close()

        noun_lemmas = []
        nouns = []
        final_ner_tagged = []
        not_ner_tagged = []
        pos_tags = nltk.pos_tag(words)
        lemmatizer = WordNetLemmatizer()

def wordNetTagger(w):
    lemmatizer = WordNetLemmatizer()
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

    tagged_top_entities = defaultdict(list)
    lemmatizer.lemmatize(w, wordnet.NOUN)
    word_synset = wordnet.synsets(w, pos="n")
    for e in list(entities.keys()):
        if len(word_synset) != 0 and len(entities[e]) != 0:
            if hypernymOf(word_synset[0], entities[e][0]):
                return e
            else:
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