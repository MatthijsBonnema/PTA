#!/usr/bin/python
# File: tagtest.py
# Author: Matthijs Bonnema
# Date: 6/9/15
# Info: 

import sys
from nltk.corpus import wordnet


def main():
    w = "New_York"
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

    words = w.split("_")
    return [(words[0], sorted_scores[0][0]), (words[1], sorted_scores[0][0])]

def test():
    word = wordnet.synsets("San_Francisco", pos="n")[0]

    city = wordnet.synsets("City", pos="n")[0]
    state = wordnet.synsets("State", pos="n")[0]
    country = wordnet.synsets("Country", pos="n")[1]

    print("City", word.path_similarity(city))
    print("State", word.path_similarity(state))
    print("Country", word.path_similarity(country))


if __name__ == "__main__":
    main()