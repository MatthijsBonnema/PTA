#!/usr/bin/python
# File: w4_ex4.py
# Author: Simon de Wit
# Date: 5/15/15
# Info:

import os

path = "group9/"
dirs = ["p34", "p35"]
for directory in dirs:
    for directory2 in os.listdir(path+directory):
        for filename in os.listdir(path+directory+directory2):
            print(filename)
            with open(os.path.join(path, directory, filename), 'r') as filedata:
                string = "".join(filedata.read().split())
                print(string)
