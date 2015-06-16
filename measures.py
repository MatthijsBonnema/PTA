#!/usr/bin/python
from collections import Counter
from nltk.metrics import ConfusionMatrix


def makeList(f):
    tagged = []
    with open(f, 'r') as fname:
        for line in fname:
            tagged.append(line.split()[7][5:])
    return tagged

golden_set = makeList("development.set.underscore")
our_set = makeList("development.set.our")
print(len(golden_set), len(our_set))

cm = ConfusionMatrix(golden_set, our_set)

# deze moeten cou, cit, etc worden
labels = set('COUNTRY STATE ENTERTAINMENT PERSON ANIMAL NATURAL_PLACES ORGANIZATION'.split())

print(cm)
true_positives = Counter()
false_negatives = Counter()
false_positives = Counter()

# hier wordt geteld wat de aantal keren hits van de classes in de confusion matrix zijn
for i in labels:
    for j in labels:
        if i == j:
            print(i, j)
            true_positives[i] += cm[i, j]
        else:
            false_negatives[i] += cm[i, j]
            false_positives[j] += cm[i, j]

print("TP:", sum(true_positives.values()), true_positives)
print("FN:", sum(false_negatives.values()), false_negatives)
print("FP:", sum(false_positives.values()), false_positives)
print("\n")

for i in sorted(labels):
    if true_positives[i] == 0:
        fscore = 0
    else:
        precision = true_positives[i] / float(true_positives[i]+false_positives[i])
        recall = true_positives[i] / float(true_positives[i]+false_negatives[i])
        fscore = 2 * (precision * recall) / float(precision + recall)
    print(i, fscore)
print("\n")
