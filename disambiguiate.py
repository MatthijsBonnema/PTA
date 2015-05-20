__author__ = 'simon'

from nltk.corpus import wordnet
from nltk.wsd import lesk
from nltk import word_tokenize
import sys


def main(argv):
    ambigious_words = []
    ambigious_lines = []
    with open(argv[1], 'r') as fname:
        for line in fname:
            l = line.split()
            if l[5] == "NN" or l[5] == "NNP":
                if len(wordnet.synsets(l[5], "n")) > 1:
                    ambigious_words.append((l[2], l[3]))

        for word in ambigious_words:
            start = int(str(word[0][0]) + "001")
            end = start + 999
            for line in fname:
                l = line.split()
                if start <= l[2] <= end:
                    ambigious_lines.append(line)

    print(ambigious_lines, ambigious_words)







main(sys.argv)