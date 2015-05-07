#!/usr/bin/python
from nltk.tag.stanford import NERTagger
import nltk
from nltk.corpus import wordnet


def main():
    file = open("ada_lovelace.txt", 'r')
    file = file.read()
    file = file.decode('utf-8')
    text = nltk.word_tokenize(file)

    # Location, Person, Organization
    class3 = NERTagger('stanford-ner/classifiers/english.all.3class.distsim.crf.ser.gz',
                   'stanford-ner/stanford-ner.jar')
    class3_nowiki = NERTagger('stanford-ner/classifiers/english.nowiki.3class.distsim.crf.ser.gz',
                   'stanford-ner/stanford-ner.jar')

    # Location, Person, Organization, Misc
    class4 = NERTagger('stanford-ner/classifiers/english.conll.4class.distsim.crf.ser.gz',
               'stanford-ner/stanford-ner.jar')

    # Time, Location, Organization, Person, Money, Percent, Date
    class7 = NERTagger('stanford-ner/classifiers/english.muc.7class.distsim.crf.ser.gz',
               'stanford-ner/stanford-ner.jar')

    #print(class3.tag(text))

    nnp_words = []
    nn_words = []
    not_tagged = []

    pos_tags = nltk.pos_tag(text)
    for tag in pos_tags:
        if tag[1] == 'NNP':
            nnp_words.append(tag[0])
        elif tag[1] == 'NN':
            nn_words.append(tag[0])

    print("NERTagged words:")
    ner_tagged = class3.tag(nnp_words)
    tagged = []
    for t in ner_tagged[0]:
        if t[1] == u'O':
            not_tagged.append(t)
        else:
            tagged.append(t)
    print(tagged)
    print("WordNet Tagged Words:")
    print(WNtagger(nn_words))
    print("Not Tagged Words:")
    print(not_tagged)


def WNtagger(l):
    tagged_words = []
    person = wordnet.synsets("person", pos='n')
    organization = wordnet.synsets("organization", pos='n')
    location = wordnet.synsets("location", pos='n')
    for w in l:
        word_synset = wordnet.synsets(w, pos="n")
        if len(word_synset) != 0 and len(person) != 0 and len(organization) != 0 and len(location) != 0:
                if hypernymOf(word_synset[0], person[0]):
                    tagged_words.append((w, "PERSON"))
                elif hypernymOf(word_synset[0], organization[0]):
                    tagged_words.append((w, "ORGANIZATION"))
                elif hypernymOf(word_synset[0], location[0]):
                    tagged_words.append((w, "LOCATION"))
    return tagged_words


def hypernymOf(synset1, synset2):
    """ Returns True if synset2 is a hypernym of
    synset1, or if they are the same synset.
    Returns False otherwise. """

    if synset1 == synset2:
        return True
    for hypernym in synset1.hypernyms():
        if synset2 == hypernym:
            return True
        if hypernymOf(hypernym, synset2):
            return True


if __name__ == "__main__":
    main()