from __future__ import division
from _collections import defaultdict
import sys

postags = defaultdict(int)
transition = defaultdict(int)
emission = defaultdict(int)
possible_tags = dict()
tagstates = set()

def getfile(transition, emission, tagstates, postags, possible_tags):
    output=open('hmmmodel.txt', 'w')
    total = len(tagstates)
    output.write(str(total)+"\n")
    for c1 in postags:
        output.write("POSTAGS" + " " + c1 + " " + str(postags[c1]) + "\n")
    for c2 in transition:
        output.write("TRANSITION" + " " + c2 + " " + str(transition[c2])+"\n")        
    for c3 in emission:
        output.write("EMISSION" + " " + c3 + " " + str(emission[c3]) + "\n")
    for c4 in possible_tags:
        word = "WORD " + c4 + " "
        for t in possible_tags[c4]:
            word += str(t) + ";"
        word += "\n" 
        output.write(word)
    output.close()

f=open("ip.txt","r")

for line in f.readlines():
    first_tag = "START"
    postags[first_tag] += 1

    sentence = line.strip().split(" ")
    for wordtag in sentence:
        apostag = wordtag[len(wordtag)-2:]
        word = wordtag[:len(wordtag)-3]
        #print word
        
        postags[apostag] += 1
        if apostag+" "+word in emission:
            emission[apostag+" "+word] += 1
        else:
            emission[apostag+" "+word] = 1
        if first_tag+" "+apostag in transition:
            transition[first_tag+" "+apostag] += 1
        else:
            transition[first_tag+" "+apostag] = 1
        first_tag = apostag
        tagstates.add(apostag)
        if word not in possible_tags:
            possible_tags[word] = set()            
        possible_tags[word].add(apostag)            
    transition[first_tag+" "+"END"] += 1

getfile(transition, emission, tagstates, postags, possible_tags)
        

    

