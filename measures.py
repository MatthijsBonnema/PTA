#!/usr/bin/python
from collections import Counter
from nltk.metrics import ConfusionMatrix

def makeList(f):
    tagged = []
    with open(f, 'r') as fname:
        for line in fname:
            if len(line.split()) > 5:
                tagged.append(line.split()[5])
    return tagged

compare = ["en.tok.off.pos.simon", "en.tok.off.pos.lars", "en.tok.off.pos.matthijs"]
#lars = makeList(compare[1])
simon = makeList(compare[0])
#matthijs = makeList(compare[2])

print(simon, len(simon))
print("TEST KLAAR")

ref = 'DET NN VB DET JJ NN NN IN DET NN'.split()
tagged = 'DET VB VB DET NN NN NN IN DET NN'.split()
cm = ConfusionMatrix(ref, tagged)

print(cm)

# deze moeten cou, cit, etc worden
labels = set('DET NN VB IN JJ'.split())

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
print() 

for i in sorted(labels):
    if true_positives[i] == 0:
        fscore = 0
    else:
        precision = true_positives[i] / float(true_positives[i]+false_positives[i])
        recall = true_positives[i] / float(true_positives[i]+false_negatives[i])
        fscore = 2 * (precision * recall) / float(precision + recall)
    print(i, fscore)
