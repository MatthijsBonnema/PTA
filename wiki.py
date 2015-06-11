#!/usr/bin/python
# Date: 5/28/15

import wikipedia
from nltk.corpus import wordnet
import nltk
from nltk.tag.stanford import NERTagger
from nltk.wsd import lesk


def main():

    text = []
    with open("en.tok.off.test", 'r') as filedata:
        for line in filedata:
            l = line.split()
            text.append([l[0], l[1], l[2], l[3], l[4]])

    posTagger(text)
    entityTagger()

    # print(wiki_lookup("Barack Obama", "PERSON"))
    # class3 = NERTagger('stanford-ner/classifiers/english.all.3class.distsim.crf.ser.gz',
    #                    'stanford-ner/stanford-ner.jar')
    # print(class3.tag(["Barack Obama"]))
    # print(wordNetTagger("Barack Obama"))

    words = []
    with open("pos.tagged", 'r') as filedata:
        for line in filedata:
            l = line.split()
            if l[5] != ".":
                words.append(l[4])
        bigram_list = nltk.ngrams(words, 2)

    tagged_bigrams = ngramTagger(bigram_list)
    tagChecker(tagged_bigrams)
    locationCheck()
    wikification()


def posTagger(text_data):
    """
    Pos tags words.
    :param text_data: raw data from files
    """
    # Take the 5th column, the word
    tokens = [token_data[4] for token_data in text_data]
    tagged_tokens = nltk.pos_tag(tokens)
    for i in range(len(text_data)):
        text_data[i].append(tagged_tokens[i][1])
    output = open("pos.tagged", "w")
    for i in text_data:
        data = "{:6}{:6}{:6}{:6}{:20}{:6}".format(i[0], i[1], i[2], i[3], i[4], i[5])
        output.write(data+"\n")
    output.close()


def entityTagger():
    """
    Tags nouns in given file, writes them to output file
    :rtype : object
    """
    class3 = NERTagger('stanford-ner/classifiers/english.all.3class.distsim.crf.ser.gz',
                       'stanford-ner/stanford-ner.jar')
    output = open("entity.tagged", "w")
    with open("pos.tagged", "r") as inp_file:
        for l in inp_file:
            line = l.split()
            # If words is a noun, go tag it!
            if line[5] == "NN" or line[5] == "NNP":
                ner_tagged = class3.tag([line[4]])
                for t in ner_tagged[0]:
                    # No nertag? Check wordnet tagging
                    if len(t[1]) < 3:
                        tag = wordNetTagger(t[0])
                        data = ("{:6}{:6}{:6}{:6}{:20}{:6}{:10}".format(line[0], line[1], line[2], line[3], line[4],
                                                                        line[5], tag))
                        output.write(data+"\n")
                    else:
                        data = ("{:6}{:6}{:6}{:6}{:20}{:6}{:10}".format(line[0], line[1], line[2], line[3], line[4],
                                                                        line[5], t[1]))
                        output.write(data+"\n")
            else:
                data = ("{:6}{:6}{:6}{:6}{:20}{:6}{:10}".format(line[0], line[1], line[2], line[3], line[4], line[5],
                                                                "-"))
                output.write(data+"\n")
    output.close()


def wordNetTagger(w):
    """
    Tags words using Wordnet Synsets.
    :param w: input a word
    :return: class name or None indicator ("-")
    """
    entities = {
        "COUNTRY": wordnet.synsets("country", pos='n'),
        "STATE": wordnet.synsets("state", pos='n'),
        "CITY": wordnet.synsets("city", pos='n'),
        "TOWN": wordnet.synsets("town", pos='n'),
        "NATURAL_PLACES": wordnet.synsets("natural_places", pos='n'),
        "PERSON": wordnet.synsets("person", pos='n'),
        "ORGANIZATION": wordnet.synsets("organisation", pos='n'),
        "ANIMAL": wordnet.synsets("animal", pos='n'),
        "SPORT": wordnet.synsets("sport", pos='n'),
        "ENTERTAINMENT": wordnet.synsets("entertainment", pos='n'),
    }
    word_synset = wordnet.synsets(w, pos="n")
    for e in list(entities.keys()):
        # Check word synsets with class synsets.
        if len(word_synset) != 0 and len(entities[e]) != 0:
            if hypernymOf(word_synset[0], entities[e][0]):
                return e
    return "-"


def ngramTagger(l):
    """
    This function takes a list of ngrams, creates bigrams and entity tags them.
    :param l: input must be a list of bigrams, formed in tuples
    :return: returns a list with words that are tagged. (For example, "El Salvador" would be [("El", "LOCATION"),
    ("Salvador", "LOCATION")]
    """
    print("checking ngrams")
    bigrams = []
    tagged_bigrams = []
    for i in l:
        ngram_ner = i[0] + " " + i[1]
        ngram_wn = i[0] + "_" + i[1]
        bigrams.append((ngram_ner, ngram_wn))

    class3 = NERTagger('stanford-ner/classifiers/english.all.3class.distsim.crf.ser.gz',
                       'stanford-ner/stanford-ner.jar')

    ner_bigrams = []
    for bg in bigrams:
        bg_tagged = bgWordNetTagger(bg[0], bg[1], class3)
        if bg_tagged[1] != "-":
            ner_bigrams.append(bg_tagged)

    for t in ner_bigrams:
        links = wiki_lookup(t[0], t[1])
        words = t[0].split(" ")
        tagged_bigrams.extend([(words[0], t[1], links), (words[1], t[1], links)])
    return tagged_bigrams


def bgWordNetTagger(ner_word, wn_word, tagger):
    tag_bigram = tagger.tag([ner_word])
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

            return (ner_word, sorted_scores[0][0])
    elif tag_bigram[0][0][1] == "PERSON" or tag_bigram[0][0][1] == "ORGANIZATION":
        return (ner_word, tag_bigram[0][0][1])
    return (ner_word, "-")


def extraWordNetTagger(w):
    if len(wordnet.synsets(w, pos="n")) > 0:
        word = wordnet.synsets(w, pos="n")[0]

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
    return "-"


def locationCheck():
    output = open("location.checked", "w")
    with open("tag.checked", "r") as inp_f:
        for line in inp_f:
            l = line.split()
            if l[6] == "LOCATION":
                tag = extraWordNetTagger(l[4])
                data = "{:6}{:6}{:6}{:6}{:20}{:6}{:10}".format(l[0], l[1], l[2], l[3], l[4], l[5], tag)
            elif len(l) > 7:
                data = "{:6}{:6}{:6}{:6}{:20}{:6}{:10}{:90}{:90}{:90}".format(l[0], l[1], l[2], l[3], l[4], l[5],
                                                                          l[6], l[7], l[8], l[9])
            else:
                data = "{:6}{:6}{:6}{:6}{:20}{:6}{:10}".format(l[0], l[1], l[2], l[3], l[4], l[5], l[6])

            output.write(data+"\n")


def tagChecker(tagged_bigrams):
    """
    This function adds entity tags to ngrams.
    :param fname: input must be a filename
    :param bl: must be a list of words which are tagged (preferably bigrams)
    :return:
    """
    output = open("tag.checked", "w")
    print("checking Tags")
    with open("entity.tagged", "r") as inp_file:
        for line in inp_file:
            l = line.split()
            # Check if word in our tagged ngram list, if so replace tag with new tag.
            condition = bigramCheck(l[4], tagged_bigrams)
            if condition[0] == "yes":
                data = "{:6}{:6}{:6}{:6}{:20}{:6}{:10}{:90}{:90}{:90}".format(l[0], l[1], l[2], l[3], l[4], l[5],
                                                                              condition[1],
                                                                                tagged_bigrams[condition[2]][2][0],
                                                                                tagged_bigrams[condition[2]][2][1],
                                                                                tagged_bigrams[condition[2]][2][2])
            elif condition[0] == "no":
                data = "{:6}{:6}{:6}{:6}{:20}{:6}{:10}".format(l[0], l[1], l[2], l[3], l[4], l[5], l[6])
            output.write(data+"\n")


def bigramCheck(w, l):
    for t in l:
        if t[0] == w:
            return ("yes", t[1], l.index(t))
    return ("no", None)


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


def wikification():
    output = open("wiki.final", "w")
    with open("location.checked", "r") as inp_f:
        for line in inp_f:
            l = line.split()
            if len(l) <= 7:
                if l[6] != "-":
                    links = wiki_lookup(l[4], l[6])
                    data = "{:6}{:6}{:6}{:6}{:20}{:6}{:10}{:90}{:90}{:90}".format(l[0], l[1], l[2], l[3], l[4], l[5],
                                                                                  l[6], links[0], links[1], links[2])
                    output.write(data+"\n")
                else:
                    data = "{:6}{:6}{:6}{:6}{:20}{:6}{:10}{:90}{:90}{:90}".format(l[0], l[1], l[2], l[3], l[4], l[5],
                                                                                  l[6], "-", "-", "-")
                    output.write(data+"\n")
            else:
                data = "{:6}{:6}{:6}{:6}{:20}{:6}{:10}{:90}{:90}{:90}".format(l[0], l[1], l[2], l[3], l[4], l[5], l[6],
                                                                              l[7], l[8], l[9])
                output.write(data+"\n")


def wiki_lookup(search_pass, tag_pass):
    search = search_pass
    tag = tag_pass

    tagcheck = ["COUNTRY", "STATE", "CITY", "TOWN", "NATURAL_PLACE", "PERSON", "ORGANISATION", "ANIMAL", "SPORT"]

    if len(search.split(" ")) == 1:
        try:
            search_syn = wordnet.synsets(search, pos="n")[0]
            search_syn = str(search_syn)
        except IndexError:
            search_syn = None
    else:
        search_clean = search.split(" ")
        search_clean = "_".join(search_clean)
        syn = wordnet.synsets(search_clean, pos="n")
        if len(syn) == 0:
            search_syn = None
        else:
            search_syn = str(wordnet.synsets(search_clean, pos="n")[0])

    wiki_results = []
    url_list = []
    result_syns = []
    to_return = []

    if tag != "NATURAL_PLACE" and tag != "ANIMAL" and tag != "ENTERTAINMENT" and tag != "COUNTRY":
        search = search+" "+tag
        search_results = wikipedia.search(search)
    else:
        search_results = wikipedia.search(search)

    for result in search_results:
        try:
            wiki_results.append([result, wikipedia.summary(result, sentences=2)])
        except wikipedia.exceptions.DisambiguationError as e:
            for result_e in e:
                wiki_results.append([result_e, wikipedia.summary(result, sentences=2)])
        except wikipedia.exceptions.PageError:
            pass

    for result in wiki_results:
        result_words = result[0].split(" ")
        if len(result_words) >= 1:
            result_clean = "_".join(result_words)
            ss = lesk(result[1], result_clean, "n")
            try:
                if ss == None:
                    result.append("-")
                    # result_syns.append("-")
                else:
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

    if search_syn != None:
        if search_syn in result_syns:
            for result in wiki_results:
                if result[2] == search_syn:
                    to_return = [result[3], "-", "-"]
        else:
            to_return = [url_list[0], "-", "-"]
    elif tag in tagcheck:
        to_return = [url_list[0], "-", "-"]
    else:
        if len(url_list) >= 3:
            to_return = [url_list[0], url_list[1], url_list[2]]
        elif len(url_list) == 2:
            to_return = [url_list[0], url_list[1], "-"]
        else:
            to_return = [url_list[0], "-", "-"]

    return to_return


if __name__ == "__main__":
    main()