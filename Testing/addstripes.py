#!/usr/bin/python


def replace(w):
    if w == "ORG":
        w = "ORGANIZATION"
        return w
    elif w == "COU":
        w = "COUNTRY"
        return w
    elif w == "CIT":
        w = "CITY"
        return w
    elif w == "PER":
        w = "PERSON"
        return w
    elif w == "ANI":
        w = "ANIMAL"
        return w
    elif w == "SPO":
        w = "SPORT"
        return w
    elif w == "ENT":
        w = "ENTERTAINMENT"
        return w
    elif w == "NAT":
        w = "NATURAL_PLACES"
        return w
    else:
        return w


def replace2(w):
    if w == "None":
        return "-"
    else:
        return w

output = open("test.set.dashes", "w")
with open("test.set", 'r') as fname:
    for line in fname:
        l = line.split()
        if len(l) > 5:
            if len(l) == 6:
                data = "{1}{0}{2}{0}{3}{0}{4}{0}{5}{0}{6}{0}{7}{0}{8}".format(" ", l[0], l[1], l[2], l[3], l[4], l[5], "-", "-")
            elif len(l) == 7:
                l[6] = replace2(l[6])
                l[6] = replace(l[6])
                data = "{1}{0}{2}{0}{3}{0}{4}{0}{5}{0}{6}{0}{7}{0}{8}".format(" ", l[0], l[1], l[2], l[3], l[4], l[5], l[6], "-")
            else:
                l[6] = replace2(l[6])
                l[6] = replace(l[6])
                data = "{1}{0}{2}{0}{3}{0}{4}{0}{5}{0}{6}{0}{7}{0}{8}".format(" ", l[0], l[1], l[2], l[3], l[4], l[5], l[6], l[7])
        output.write(data+"\n")
output.close()



