#!/usr/bin/python
# Date: 5/28/15

import sys
import wikipedia
from nltk.corpus import wordnet
import nltk
from collections import defaultdict
from nltk.tag.stanford import NERTagger
from nltk.wsd import lesk

def main(argv):

    text = []
    with open("en.tok.off.test", 'r') as filedata:
        for line in filedata:
            text.append(line.split())
        words = [token_data[3] for token_data in text]

        bigram_list = nltk.ngrams(words, 2)
    posTagger(text)
    entityTagger()
    tagged_bigrams = ngramTagger(bigram_list)
    tagChecker("en.tok.off.test.pos.et", tagged_bigrams)


def posTagger(text_data):
    """
    Pos tags words.
    :param text_data: raw data from files
    """
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
    """
    Tags nouns in given file, writes them to output file
    """
    class3 = NERTagger('stanford-ner/classifiers/english.all.3class.distsim.crf.ser.gz',
                       'stanford-ner/stanford-ner.jar')
    output = open("en.tok.off.test.pos.et", "w")
    with open("en.tok.off.test.pos", "r") as inp_file:
        for l in inp_file:
            line = l.split()
            # If words is a noun, go tag it!
            if line[4] == "NN" or line[4] == "NNP":
                ner_tagged = class3.tag([line[3]])
                for t in ner_tagged[0]:
                    # No nertag? Check wordnet tagging
                    if len(t[1]) < 3:
                        tag = wordNetTagger(t[0])
                        data = ("{:4}{:4}{:6}{:20}{:6}{:10}".format(line[0], line[1], line[2], line[3], line[4], tag))
                        output.write(data+"\n")
                    else:
                        data = ("{:4}{:4}{:6}{:20}{:6}{:10}".format(line[0], line[1], line[2], line[3], line[4], t[1]))
                        output.write(data+"\n")
            else:
                data = ("{:4}{:4}{:6}{:20}{:6}{:10}".format(line[0], line[1], line[2], line[3], line[4], "-"))
                output.write(data+"\n")
    output.close()


def wordNetTagger(w):
    """
    Tags words using Wordnet Synsets.
    :param w: input a word
    :return: class name or None indicator ("-")
    """
    entities = {
        "COU": wordnet.synsets("country", pos='n'),
        "STATE": wordnet.synsets("state", pos='n'),
        "CITY": wordnet.synsets("city", pos='n'),
        "TOWN": wordnet.synsets("town", pos='n'),
        "NAT": wordnet.synsets("natural_places", pos='n'),
        "PER": wordnet.synsets("person", pos='n'),
        "ORG": wordnet.synsets("organisation", pos='n'),
        "ANI": wordnet.synsets("animal", pos='n'),
        "SPO": wordnet.synsets("sport", pos='n'),
        "ENT": wordnet.synsets("entertainment", pos='n'),
    }
    word_synset = wordnet.synsets(w, pos="n")
    for e in list(entities.keys()):
        # Check word synsets with class synsets.
        if len(word_synset) != 0 and len(entities[e]) != 0:
            if hypernymOf(word_synset[0], entities[e][0]):
                return e
    return "-"


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


def ngramTagger(l):
    """
    This function takes a list of ngrams, creates bigrams and entity tags them.
    :param l: input must be a list of bigrams, formed in tuples
    :return: returns a list with words that are tagged. (For example, "El Salvador" would be [("El", "LOCATION"),
    ("Salvador", "LOCATION")]
    """
    print("tagging ngrams")
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
                tb.append(t)
    for bg in bigrams:
        tag_bg = bgWordNetTagger(bg[0], bg[1])
        if tag_bg == "COUNTRY" or tag_bg == "STATE" or tag_bg == "CITY" or tag_bg == "TOWN":
            tb.append((bg, tag_bg))
    return tb


def tagChecker(fname, tagged_bigrams):
    """
    This function adds enitity tags to ngrams.
    :param fname: input must be a filename
    :param bl: must be a list of words which are tagged (preferably bigrams)
    :return:
    """
    output = open("en.tok.off.test.pos.et.final", "w")
    print("checking Tags")
    with open(fname, "r") as inp_file:
        for line in inp_file:
            l = line.split()
            # Check if word in our tagged ngram list, if so replace tag with new tag.
            for t in tagged_bigrams:
                if t[0] == l[3]:
                    data = ("{:4}{:4}{:6}{:20}{:6}{:10}".format(line[0], line[1], line[2], line[3], line[4], t[1]))
                    output.write(data+"\n")



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

def wiki_lookup(search_pass, tag_pass):

    search = search_pass
    tag = tag_pass

    tagcheck = ["COUNTRY", "STATE", "CITY", "TOWN", "NATURAL_PLACE", "PERSON", "ORGANISATION", "ANIMAL", "SPORT", "ENTERTAINMENT"]



    if len(search.split(" ")) == 1:
        search_syn = str(wordnet.synsets(search, pos="n")[0])
    else:
        search_syn = None


    wiki_results = []
    url_list = []
    result_syns = []
    to_return = []

    if tag != "NATURAL_PLACE" or tag != "ENTERTAINMENT":
        search_results = wikipedia.search((search+" "+tag))
    else:
        search_results = wikipedia.search((search))



    for result in search_results:
        try:
            wiki_results.append([result, wikipedia.summary(result, sentences=2)])
        except wikipedia.exceptions.DisambiguationError as e:
            for result_e in e:
                wiki_results.append([result_e, wikipedia.summary(result, sentences=2)])

    for result in wiki_results:
        result_words = result[0].split(" ")
        if len(result_words) == 1:
            ss = lesk(result[1], result[0], "n")
            try:
                result.append(str(ss))
                result_syns.append(str(ss))
            except AttributeError:
                result.append("-")
                result_syns.append("-")
        else:
            result.append("-")

        page = wikipedia.page(result[0])
        result.append(page.url)
        url_list.append(page.url)

    if search_syn:
        if search_syn in result_syns:
            for result in wiki_results:
                if result[2] == search_syn:
                    to_return = [result[3], "-", "-"]
    elif tag in tagcheck:
        to_return = [url_list[0], "-", "-"]
    else:
        if len(url_list) >= 3:
            to_return = ([url_list[0], url_list[1], url_list[2]])
        elif len(url_list) == 2:
            to_return = ([url_list[0], url_list[1], "-"])
        else:
            to_return = ([url_list[0], "-", "-"])

    return(to_return)


if __name__ == "__main__":
    main(sys.argv)