#!/usr/bin/python

import sys


def main(argv):
    text_data = []
    output = open("en.tok.off.pos.test", "w")
    with open(argv[1], 'r') as fname:
        for line in fname:
            text_data.append(line.split())
    for i in text_data:
        if len(i) == 5:
            i.extend(("-", "-"))
        elif len(i) == 6:
            i.append("-")
        print(i[3])
        data = ("{:4}{:4}{:6}{:20}{:5}{:5}{}".format(i[0], i[1], i[2], i[3], i[4], i[5], i[6]))
        output.write(data+"\n")

main(sys.argv)