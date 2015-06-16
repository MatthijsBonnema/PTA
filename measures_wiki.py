#!/usr/bin/python
from collections import Counter
from nltk.metrics import ConfusionMatrix


devset = []
with open("development.set.underscore", 'r') as testfile:
    for line in testfile:
        devset.append(line.split())
ourset = []
with open("development.set.our", 'r') as ourfile:
    for line in ourfile:
        ourset.append(line.split())

total = 0
true_pos = 0

for i in range(len(devset)):
    if devset[i][7] != "-" and ourset[i][7] != "-":
        total += 1
        if devset[i][7] == ourset[i][7] or devset[i][7] == ourset[i][8] or devset[i][7] == ourset[i][9]:
            true_pos += 1
        else:
            if len(devset[i][7]) > 4 and len(ourset[i][7]) > 4:
                if ourset[i][7][4] == "s" and not devset[i][7][4] == "s":
                    if devset[i][7][6:] == ourset[i][7][7:]:
                        true_pos += 1
                elif devset[i][7][4] == "s" and not ourset[i][7][4] == "s":
                    if devset[i][7][7:] == ourset[i][7][6:]:
                        true_pos += 1
                if ourset[i][8] != "-":
                    if devset[i][7][4] == "s" and not ourset[i][8][4] == "s":
                        if devset[i][7][7:] == ourset[i][8][6:]:
                            true_pos += 1
                    elif ourset[i][8][4] == "s" and not devset[i][7][4] == "s":
                        if devset[i][7][6:] == ourset[i][8][7:]:
                            true_pos += 1
                if ourset[i][9] != "-":
                    if devset[i][7][4] == "s" and not ourset[i][9][4] == "s":
                        if devset[i][7][7:] == ourset[i][9][6:]:
                            true_pos += 1
                    elif ourset[i][9][4] == "s" and not devset[i][7][4] == "s":
                        if devset[i][7][6:] == ourset[i][9][7:]:
                            true_pos += 1
    elif devset[i][7] == "-" and ourset[i][7] == "-":
        # If both are dash, also good.
        pass

perc = (true_pos/float(total)) * 100
print("Total: {:6} \t Good: {:6} \t Percentage Accurate: {} % ".format(total, true_pos, round(perc, 2)))

# cm = ConfusionMatrix(golden_set, our_set)
#
# # deze moeten cou, cit, etc worden
# labels = set('COUNTRY STATE ENTERTAINMENT PERSON ANIMAL NATURAL_PLACES ORGANIZATION'.split())
#
# print(cm)
# true_positives = Counter()
# false_negatives = Counter()
# false_positives = Counter()
#
# # hier wordt geteld wat de aantal keren hits van de classes in de confusion matrix zijn
# for i in labels:
#     for j in labels:
#         if i == j:
#             print(i, j)
#             true_positives[i] += cm[i, j]
#         else:
#             false_negatives[i] += cm[i, j]
#             false_positives[j] += cm[i, j]
#
# print("TP:", sum(true_positives.values()), true_positives)
# print("FN:", sum(false_negatives.values()), false_negatives)
# print("FP:", sum(false_positives.values()), false_positives)
# print("\n")
#
# for i in sorted(labels):
#     if true_positives[i] == 0:
#         fscore = 0
#     else:
#         precision = true_positives[i] / float(true_positives[i]+false_positives[i])
#         recall = true_positives[i] / float(true_positives[i]+false_negatives[i])
#         fscore = 2 * (precision * recall) / float(precision + recall)
#     print(i, fscore)
# print("\n")
