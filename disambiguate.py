#!/usr/bin/python

from nltk.corpus import wordnet
from nltk.wsd import lesk
import os
from collections import Counter


def main():
    path = "group9/"
    dirs = ["p34", "p35"]
    number_of_ss = 0
    synsets = []

    for directory in dirs:
        for directory2 in os.listdir(path+directory):
            for filename in os.listdir(path+directory+"/"+directory2):
                if filename.endswith(".tok.off.pos.ent"):
                    with open(os.path.join(path, directory+"/"+directory2, filename), 'r') as fname:
                        output = open(os.path.join(path, directory+"/"+directory2, "output_disambiguation.txt"), 'w')

                        ambiguous_words = []
                        ambiguous_lines = []
                        text_words = []


                        for line in fname:
                            split_line = line.split()
                            text_words.append(split_line)
                            l = line.split()
                            if l[4] == "NN" or l[4] == "NNP":
                                if len(wordnet.synsets(l[3], "n")) > 1:
                                    number_of_ss += len(wordnet.synsets(l[3], "n"))
                                    synsets.append(len(wordnet.synsets(l[3], "n")))
                                    ambiguous_words.append((l[2], l[3]))
                        for word in ambiguous_words:
                            start = int(str(word[0][0]) + "001")
                            end = start + 999
                            lines = []
                            for l in text_words:
                                if start <= int(l[2]) <= end:
                                    lines.append(l[3])
                            ambiguous_lines.append(lines)
                        for i in range(len(ambiguous_words)):
                            ss = lesk(ambiguous_lines[i], ambiguous_words[i][1], "n")
                            outputwrite = str((ss, ss.definition())) + "\n"
                            output.write(outputwrite)
    c = Counter(synsets)

    print(sorted(c.items(), key=lambda pair: pair[0], reverse=True))
    print(number_of_ss)

main()