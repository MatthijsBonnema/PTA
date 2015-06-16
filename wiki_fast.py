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
            if len(l) > 4:
                text.append([l[0], l[1], l[2], l[3], l[4]])

    # Pos & Entity Tagging + finding wikipedia links of normal words
    posTagger(text)
    nouns = getNouns()
    # tagged = gertest(nouns)
    # writeTags(tagged)
    # locationCheck()
    # wikification()

    # Entity tagging and finding wikipedia links of bigrams
    bigrams = makeBigrams(nouns, 2)
    tagged_bigrams = ngramTagger(bigrams)
    tagChecker(tagged_bigrams)


def posTagger(text_data):
    """
    Pos tags words.
    :param text_data: raw data from files
    """
    # Take the 5th column, the word
    tokens = [token_data[4].decode("utf-8") for token_data in text_data]

    # Tag words
    tagged_tokens = nltk.pos_tag(tokens)

    #Append tokens to list
    for i in range(len(text_data)):
        text_data[i].append(unicode(tagged_tokens[i][1]))

    #Write to output file
    output = open("pos.tagged", "w")
    for i in text_data:
        data = "{} {} {} {} {} {}".format(i[0], i[1], i[2], i[3], i[4], i[5])
        output.write(data+"\n")
    output.close()


def getNouns():
    """
    function that makes a list of all the nouns in the development set.
    :return: list of all the nouns
    """
    nouns = []
    with open("wiki.final", "r") as inp_file:
        for l in inp_file:
            line = l.split()
            # If words is a noun, go tag it!
            if line[5] == "NN" or line[5] == "NNP" or line[5] == "NNPS":
                nouns.append(unicode(line[4]))
    return nouns


def entityTaggertest(l):
    """
    function that entity tags a list of nouns
    :param l: list of nouns
    :return: list of tagged nouns, tuples (word, tag)
    """
    tagged = []
    class3 = NERTagger('stanford-ner/classifiers/english.all.3class.distsim.crf.ser.gz',
                       'stanford-ner/stanford-ner.jar')
    ner_tagged = class3.tag(l)
    for l in ner_tagged:
        for t in l:
            # If the word is tagged via NERTagger
            if len(t[1]) > 3:
                tagged.append(t)
            # If the words is not tagged, try to tag it via Word Net
            if len(t[1]) < 3:
                tag = wordNetTagger(t[0])
                # If even Word Net cant tag it, return without tag.
                if tag != "-":
                    tagged.append((t[0], tag))
    return tagged


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


def writeTags(tagged_words):
    """
    this function writes away the entity tags to a given file
    :param tagged_words:
    :return: nothing
    """
    output = open("entities.tagged", "w")
    with open("pos.tagged", "r") as inp_file:
        for line in inp_file:
            l = line.split()
            # Check if word in this line is tagged, if so, add tag to line
            result = inList(l[4], tagged_words)
            if result[0] == "yes":
                data = "{} {} {} {} {} {} {}".format(l[0], l[1], l[2], l[3], l[4], l[5], result[1])
            else:
                data = "{} {} {} {} {} {} {}".format(l[0], l[1], l[2], l[3], l[4], l[5], "-")
            output.write(data+"\n")
    output.close()


def inList(w, l):
    """
    function that check if a word is in the tagged words list. if so, it returns the tag
    :param w: words
    :param l: list of tuples with (word, tag)
    :return: yes or no, followed by the tag or none
    """
    for t in l:
        if t[0] == w:
            return "yes", t[1]
    return "no", None


def locationCheck():
    """
    function that checks if any words are tagged as location. if so, this is converted to city, state, country or town
    :return:
    """
    output = open("loc.checked", "w")
    with open("entities.tagged", "r") as inp_f:
        for line in inp_f:
            l = line.split()
            # If words is tagged location, tag again via locationTagger()
            if l[6] == "LOCATION":
                tag = locationTagger(l[4])
                data = "{} {} {} {} {} {} {}".format(l[0], l[1], l[2], l[3], l[4], l[5], tag)
            # elif len(l) > 7:
            #     data = "{:6}{:6}{:6}{:6}{:20}{:6}{:13}{:90}{:90}{:90}".format(l[0], l[1], l[2], l[3], l[4], l[5],
            #                                                                   l[6], l[7], l[8], l[9])
            else:
                data = "{} {} {} {} {} {} {}".format(l[0], l[1], l[2], l[3], l[4], l[5], l[6])

            output.write(data+"\n")
    output.close()


def locationTagger(w):
    """
    function that tags words which are tagged with LOCATION, via wordnet similarity.
    :param w: word
    :return:
    """
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


def ngramTagger(l):
    """
    this function creates bigrams, tags them via Stanford NER or Word Net, and searches links for wiki pages.
    :param l: input must be a list of bigrams, formed in tuples
    :return: returns a list with words that are tagged and linked to wikipedia.
    """
    print("checking ngrams")
    nerts = []

    # First, create words which are suited as input for NERTagger.
    for i in l:
        ngram_ner = i[0] + " " + i[1]
        nerts.append(ngram_ner)

    # Input the list of suitable bigrams in the NERTagger, and form the output to a wanted format with nerToBG()
    class3 = NERTagger('stanford-ner/classifiers/english.all.3class.distsim.crf.ser.gz',
                       'stanford-ner/stanford-ner.jar')
    ner_result = class3.tag(nerts)
    bigramsAndTags = nerToBG(ner_result)

    for t in bigramsAndTags:
        # If tagged as location, get rid of location via the same technique as locationTagger(), but then for bigrams,
        # using getRidOfLocation()
        if t[1] == "LOCATION" or t[2] == "LOCATION":
            wn_bg = t[0].split()[0] + "_" + t[0].split()[1]
            wAndTag = getRidOfLocation(wn_bg)
            t[1] = wAndTag[1]
            t[2] = wAndTag[1]

    final_list = []
    a = 0
    for j in range(len(bigramsAndTags)):
        # If the 2 words of the bigram are tagged the same, append them to final_list.
        if bigramsAndTags[a][1] == bigramsAndTags[a][2]:
            final_list.extend([(bigramsAndTags[a][0], bigramsAndTags[a][1])])
        # If word 1 isn't tagged and word 2 is, check if word 1 is tagged in the development set.
        # If this tag is the same as the tag of word 2, append to final_list.
        elif checkBGTag(bigramsAndTags[a][0].split()[0]) == bigramsAndTags[a][2]:
            final_list.extend([(bigramsAndTags[a][0], bigramsAndTags[a][2])])
        # If word 2 isn't tagged and word 1 is, check if word 2 is tagged in the single word tagged development set.
        # If this tag is the same as the tag of word 1, append to final_list.
        elif checkBGTag(bigramsAndTags[a][0].split()[1]) == bigramsAndTags[a][1]:
            final_list.extend([(bigramsAndTags[a][0], bigramsAndTags[a][1])])
        a += 1

    taglink_bigrams = []
    for bgs in final_list[:]:
        # If bigrams are still not tagged, remove them from the list.
        if len(bgs[1]) < 4:
            final_list.remove(bgs)
        else:
            # If they are tagged, look up wikipedia links.
            links = wiki_lookup(bgs[0], bgs[1])
            words = bgs[0].split(" ")
            taglink_bigrams.extend([(words[0], bgs[1], links), (words[1], bgs[1], links)])

    return taglink_bigrams


def makeBigrams(l, n):
    """
    simple function that return bigrams, but can also make other n grams if wanted
    :param l: list of words
    :param n: n for n grams (2 for bigrams)
    :return: list with tuples with 2 words, which are the bigrams.
    """
    bgs = nltk.ngrams(l, n)
    return bgs


def nounsAndTags():
    """
    function that gets the nouns + entity tag from a wanted file.
    :return:
    """
    nNt = []
    with open("wiki.final", "r") as inp_file:
        for l in inp_file:
            line = l.split()
            # If words is a noun, go tag it!
            if (line[5] == "NN" or line[5] == "NNP") and line[6] != "-":
                nNt.append((unicode(line[4]), unicode(line[6])))
    return nNt


def checkBGTag(word):
    """
    function that checks if a word is in the list created by the nounsAndTags() function.
    :param word: word
    :return: tag of that word, or - if no tag is found
    """
    nAndT = nounsAndTags()
    for t in nAndT:
        if t[0] == word:
            return t[1]
    return "-"


def nerToBG(l):
    """
    function that converts the output of the nertagger to a list with lists,
    which are formed like this: [bigram, tag_word_1, tag_word_2]
    :param l: output of NERTagger
    :return: list bigrams plus tags
    """
    bg = []
    while len(l[0]) > 1:
        bigram = l[0][0][0] + " " + l[0][1][0]
        bg.append([bigram, l[0][0][1], l[0][1][1]])
        l[0].pop(0)
        l[0].pop(0)
    return bg


def getRidOfLocation(wn_word):
    """
    function that tags bigrams which are tagged with LOCATION, via wordnet similarity.
    :param wn_word: bigrams, with _ instead of space
    :return: word + tag
    """
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
        word = wn_word.split("_")[0] + " " + wn_word.split("_")[1]
        return word, sorted_scores[0][0]
    else:
        word = wn_word.split("_")[0] + " " + wn_word.split("_")[1]
        return word, "-"


def tagChecker(tagged_bigrams):
    """
    function that adds the tagged words from bigrams and the wikipedia links to a given file.
    :param tagged_bigrams: list of bigrams, formed: [bigram, tag, links]
    :return:
    """
    output = open("hopelijk.echt.de.laatste", "w")
    print("checking Tags")
    with open("wiki.final", "r") as inp_file:
        for line in inp_file:
            l = line.split()
            # Check if word in our tagged ngram list, if so replace tag with new tag.
            condition = bigramCheck(unicode(l[4]), tagged_bigrams)
            if condition[0] == "yes":
                # Add tag + links to line
                data = "{} {} {} {} {} {} {} {} {} {}".format(l[0], l[1], l[2], l[3], l[4], l[5], condition[1],
                                                              tagged_bigrams[condition[2]][2][0],
                                                              tagged_bigrams[condition[2]][2][1],
                                                              tagged_bigrams[condition[2]][2][2])
            elif condition[0] == "no":
                # Leave line like it is
                data = "{} {} {} {} {} {} {} {} {} {}".format(l[0], l[1], l[2], l[3], l[4], l[5], l[6], l[7], l[8], l[9])
            output.write(data+"\n")
    output.close()


def bigramCheck(w, l):
    """
    Checks if a word is in a list
    :param w: word
    :param l: list of tagged words from bigrams
    :return: yes or no + the tag and if yes the index of the tag in the list
    """
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
    """
    function that searches wikipedia pages by words.
    :return:
    """
    output = open("wiki.final", "w")
    with open("loc.checked", "r") as inp_f:
        for line in inp_f:
            l = line.split()
            if len(l) <= 7:
                # If file is tagged, than look up wikipedia links
                if l[6] != "-":
                    links = wiki_lookup(l[4], l[6])
                    data = "{} {} {} {} {} {} {} {} {} {}".format(l[0], l[1], l[2], l[3], l[4], l[5],
                                                                  l[6], links[0], links[1], links[2])
                else:
                    data = "{} {} {} {} {} {} {} {} {} {}".format(l[0], l[1], l[2], l[3], l[4], l[5], l[6],
                                                                  "-", "-", "-")
            else:
                data = "{} {} {} {} {} {} {} {} {} {}".format(l[0], l[1], l[2], l[3], l[4], l[5], l[6], l[7],
                                                              l[8], l[9])
            output.write(data+"\n")
    output.close()


def wiki_lookup(search_pass, tag_pass):
    search = search_pass
    tag = tag_pass
    search_lower = search.lower()

    tagcheck = ["COUNTRY", "STATE", "CITY", "TOWN", "NATURAL_PLACE", "PERSON", "ANIMAL", "SPORT"]
    if search_lower != "president":
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

        if tag != "NATURAL_PLACE" and tag != "ANIMAL" and tag != "ENTERTAINMENT" and tag != "COUNTRY" and \
                        tag != "STATE" and tag != "ORGANIZATION":
            search = search+" "+tag
            search_results = wikipedia.search(search)
        else:
            search_results = wikipedia.search(search)

        if len(search_results) != 0:

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
        else:
            to_return = ["-", "-", "-"]
    else:
        to_return = ["-", "-", "-"]

    return to_return


if __name__ == "__main__":
    main()