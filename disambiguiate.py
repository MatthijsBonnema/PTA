#!/usr/bin/python

from nltk.corpus import wordnet
from nltk.wsd import lesk
from nltk import word_tokenize
import sys


def main(argv):
    ambigious_words = []
    ambigious_lines = []
    text_words = []
    with open(argv[1], 'r') as fname:
        for line in fname:
            split_line = line.split()
            text_words.append(split_line)
            l = line.split()
            if l[4] == "NN" or l[4] == "NNP":
                if len(wordnet.synsets(l[3], "n")) > 1:
                    ambigious_words.append((l[2], l[3]))
    for word in ambigious_words:
        start = int(str(word[0][0]) + "001")
        end = start + 999
        lines = []
        for l in text_words:
            if start <= int(l[2]) <= end:
                lines.append(l[3])
        ambigious_lines.append(lines)
    for i in range(len(ambigious_lines)):
        ss = lesk(ambigious_lines[i], ambigious_words[i][1], "n")
        print(ss, ss.definition())








main(sys.argv)