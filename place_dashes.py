#!/usr/bin/python

import sys


def main(argv):
    text_data = []
    output = open(argv[1]+"2", "w")
    with open(argv[1], 'r') as fname:
        for line in fname:
            text_data.append(line.split())
    for i in text_data:
        if len(i) == 5:
            i.extend(("-", "-"))
        elif len(i) == 6:
            i.append("-")
        data = ("{:4}{:4}{:6}{:20}{:5}{:5}{}".format(i[0], i[1], i[2], i[3], i[4], i[5], i[6]))
        output.write(data+"\n")
        output.close()

main(sys.argv)