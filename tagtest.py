#!/usr/bin/python3
# File: tagtest.py
# Author: Matthijs Bonnema
# Date: 6/9/15
# Info: 

import sys
from nltk.corpus import wordnet


def main():
    word = wordnet.synsets("San_Francisco", pos="n")[0]

    city = wordnet.synsets("City", pos="n")[0]
    state = wordnet.synsets("State", pos="n")[0]
    country = wordnet.synsets("Country", pos="n")[1]

    print("City", word.path_similarity(city))
    print("State", word.path_similarity(state))
    print("Country", word.path_similarity(country))


if __name__ == "__main__":
    main()