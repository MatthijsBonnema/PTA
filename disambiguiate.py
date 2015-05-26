#!/usr/bin/python

from nltk.corpus import wordnet
from nltk.wsd import lesk
from nltk import word_tokenize
import sys
import os


def main(argv):
    path = "group9/"
    dirs = ["p34", "p35"]
    ambigious_words = []
    ambigious_lines = []
    text_words = []
    for directory in dirs:
        for directory2 in os.listdir(path+directory):
            for filename in os.listdir(path+directory+"/"+directory2):
                if filename.endswith(".tok.off.pos.ent"):
                    with open(os.path.join(path, directory+"/"+directory2, filename), 'r') as fname:
                        output = open("output_disambiguation.txt", "w")
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
                            output.write((ss, ss.definition()))

main(sys.argv)