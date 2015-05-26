#!/usr/bin/python

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
            if l[4] == "NN" or l[4] == "NNP":
                if len(wordnet.synsets(l[3], "n")) > 1:
                    ambigious_words.append((l[2], l[3]))
    for word in ambigious_words:
        start = int(str(word[0][0]) + "001")
        end = start + 999
        with open(argv[1], 'r') as fname:
            lines = []
            for line in fname:
                l = line.split()
                if start <= int(l[2]) <= end:
                    lines.append(l[3])
                    print(l[3])
            ambigious_lines.append(lines)
    for i in range(len(ambigious_lines)):
        print(ambigious_words[i], ambigious_lines[i])
        print(i)








main(sys.argv)