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

compare = ["en.tok.off.pos.simon2", "en.tok.off.pos.lars2", "en.tok.off.pos.matthijs2"]
simon = makeList(compare[0])
lars = makeList(compare[1])
matthijs = makeList(compare[2])

cm_list = [ConfusionMatrix(simon, lars), ConfusionMatrix(simon, matthijs), ConfusionMatrix(lars, matthijs)]

# deze moeten cou, cit, etc worden
labels = set('COU CIT ENT PER ANI NAT ORG'.split())

n = 0
for cm in cm_list:
    print(compare[n] + "\n")
    n += 1
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
