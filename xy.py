#!/usr/bin/python


import sys
from nltk.stem.wordnet import WordNetLemmatizer
from nltk.corpus import wordnet
import nltk

def main():
	file = open("ada_lovelace.txt", 'r')
	file = file.read()
	file = file.decode('utf-8')
	
	text = nltk.word_tokenize(file)
	
	mydict = {
	"act": wordnet.synsets("act", pos='n'),
	"animal": wordnet.synsets("animal", pos='n'),
	"artifact": wordnet.synsets("artifact", pos='n'),
	"attribute": wordnet.synsets("attribute", pos='n'),
	"body": wordnet.synsets("body", pos='n'),
	"cognition": wordnet.synsets("cognition", pos='n'),
	"communication": wordnet.synsets("communication", pos='n'),
	"event": wordnet.synsets("event", pos='n'),
	"feeling": wordnet.synsets("feeling", pos='n'),
	"food": wordnet.synsets("food", pos='n'),
	"group": wordnet.synsets("group", pos='n'),
	"location": wordnet.synsets("location", pos='n'),
	"motive": wordnet.synsets("motive", pos='n'),
	"natural object": wordnet.synsets("natural object", pos='n'),
	"person": wordnet.synsets("person", pos='n'),
	"plant": wordnet.synsets("plant", pos='n'),
	"possession": wordnet.synsets("possession", pos='n'),
	"process": wordnet.synsets("process", pos='n'),
	"quantity": wordnet.synsets("quantity", pos='n'),
	"relation": wordnet.synsets("relation", pos='n'),
	"shape": wordnet.synsets("shape", pos='n'),
	"state": wordnet.synsets("state", pos='n'),
	"substance": wordnet.synsets("substance", pos='n'),
	"time": wordnet.synsets("time", pos='n')
	}
	
	act = wordnet.synsets("act", pos='n')
	action = wordnet.synsets("action", pos='n')
	artifact = wordnet.synsets("artifact", pos='n')
	activity = wordnet.synsets("activity", pos='n')
	animal = wordnet.synsets("animal", pos='n')
	fauna = wordnet.synsets("fauna", pos='n')
	
	noun_lemmas = []
	
	noun_synsets_act =[]
	noun_synsets_animal =[]
	noun_synsets_artifact =[]
	noun_synsets_activity =[]
	noun_synsets_action =[]
	noun_synsets_fauna =[]
	
	#mydict = {0: ["act","action","activity"], 1: ["animal","fauna"], 2: ["artifact"]}
	
	mylist = ["act","action","activity","animal","fauna","artifact"]

	
	lemmatizer = WordNetLemmatizer()
	pos_tags = nltk.pos_tag(text)
	
	for word in pos_tags:
		if word[1] == "NN" or word[1] == "NNP":
			noun_lemmas.append(lemmatizer.lemmatize(word[0], wordnet.VERB))
			word_synset = wordnet.synsets(word[0], pos="n")
			if len(word_synset) != 0  and len(act) !=0 and len(action) !=0 and len(activity) !=0 and len(animal) !=0 and len(fauna) !=0 and len(artifact) !=0:
				if hypernymOf(word_synset[0], act[0]):
					noun_synsets_act.append(word_synset)
				if hypernymOf(word_synset[0], action[0]):
					noun_synsets_action.append(word_synset)
				if hypernymOf(word_synset[0], activity[0]):
					if word_synset not in noun_synsets_activity:
						noun_synsets_activity.append(word_synset)
				if hypernymOf(word_synset[0], animal[0]):
					noun_synsets_animal.append(word_synset)
				if hypernymOf(word_synset[0], fauna[0]):
					noun_synsets_fauna.append(word_synset)
				if hypernymOf(word_synset[0], artifact[0]):
					if word_synset not in noun_synsets_artifact:
						noun_synsets_artifact.append(word_synset)
		
				

	# Exercise 1.2
	print("\nEXERCISE 1.2\n")
	print("Act: ", len(noun_synsets_act))
	print("Action: ", len(noun_synsets_action))
	print("Artifact: ", len(noun_synsets_artifact))
	print("Activity: ", len(noun_synsets_activity))
	print("Animal: ", len(noun_synsets_animal))
	print("fauna: ", len(noun_synsets_fauna))
	
	
		
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
