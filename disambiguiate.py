__author__ = 'simon'

from nltk.corpus import wordnet
from nltk.wsd import lesk
from nltk import word_tokenize
import sys


def main(argv):
    with open(argv[1], 'r') as fname:
        for line in fname:
            l = line.split()
            if l[5]


main(sys.argv)