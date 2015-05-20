#!/usr/bin/python3
# File: w4_ex4.2_mat.py
# Author: Matthijs Bonnema
# Date: 5/13/15
# Info: 

import sys


def main():
    input = file('en.tok.off.pos', 'r')

    data = []

    for line in input.readlines():
        data.append(line.split())

    for dataline in data:
        print(dataline)

if __name__ == "__main__":
    main()