#!/usr/bin/python
# File: w4_ex4.py
# Author: Simon de Wit
# Date: 5/15/15
# Info:

import os
import nltk

path = "group9/"
dirs = ["p34", "p35"]
for directory in dirs:
    for directory2 in os.listdir(path+directory):
        for filename in os.listdir(path+directory+"/"+directory2):
            if filename.endswith(".tok.off"):
                with open(os.path.join(path, directory+"/"+directory2, filename), 'r') as filedata:
                    text_data = [line.split() for line in filedata]
tokens = [token_data[3] for token_data in text_data]
tagged_tokens = nltk.pos_tag(tokens)
for i in range(len(text_data)):
    text_data[i].append(tagged_tokens[i][1])
output = open("en.tok.off.pos", "w")
for i in text_data:
    data = ("{:4}{:4}{:6}{:20}{:3}".format(i[0], i[1], i[2], i[3], i[4]))
    output.write(data+"\n")
output.close()
