#!/usr/bin/python3
# File: wikitest.py
# Author: Matthijs Bonnema
# Date: 6/9/15
# Info: Returns urls for wikipedia

import wikipedia
from nltk.corpus import wordnet
import nltk
from nltk.wsd import lesk

from collections import defaultdict
from nltk.tag.stanford import NERTagger


def wiki_lookup(search_pass, tag_pass):

    search = search_pass
    tag = tag_pass

    tagcheck = ["COU", "STATE", "CITY", "TOWN", "NAT", "PER", "ORG", "ANI", "SPO", "ENT"]

    if len(search.split(" ")) == 1:
        search_syn = str(wordnet.synsets(search, pos="n")[0])
    else:
        search_syn = None


    wiki_results = []
    url_list = []
    result_syns = []
    to_return = []
    search_results = wikipedia.search(search)



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

    if search_syn != None:
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
    search = "El Salvador"
    tag = "COU"
    test = wiki_lookup(search, tag)

    print(test)