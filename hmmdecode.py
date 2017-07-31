from __future__ import division
from _collections import defaultdict
import sys
    
states = set()
transition = defaultdict(int)       
emission = defaultdict(int)
start = defaultdict(int) 
postags = defaultdict(int)   
possible_tags = dict()
c=0
total = 0

#def calcprob(st1,st2,num,di,
pun={'.',',','!','?','(',')',':',';','=','-','+','"','\'','*','$','[',']','{','}'}

def gettags(states,word_prob,viterbi_backpointer,sentence,possible_tags):
    #print "hi"
    word_tags = [] 
    postag = ""   
    max_prob = -1
    cur_states = states
    leng=len(sentence)-1
    if sentence[leng] in possible_tags:
        cur_states = possible_tags[sentence[leng]]
       # print sentence[leng],"cur ****states",sentence
        for tag in cur_states:
            
            if max_prob <= word_prob[leng][tag]:
                max_prob = word_prob[leng][tag]
                postag = tag
               # print postag,"****IF****",max_prob
    else:
        for tag in cur_states:
           # print tag,"****ELSE****"
            if max_prob <= word_prob[leng][tag]:
                max_prob = word_prob[leng][tag]
                postag = tag
                #print postag,"****ELSE****"
    
    word_tags.append(sentence[leng]+"/"+postag)
   # print word_tags
                   
    for ij in range(leng-1, -1, -1):
        if postag in viterbi_backpointer[ij+1]:
            postag = viterbi_backpointer[ij+1][postag]
           # print postag,"foooor####if"
        else:
            for i in states:
                if i in viterbi_backpointer[ij+1]:
                    postag = viterbi_backpointer[ij+1][i]
                    #print postag,"foooor####"
                    break;
        word_tags.append(sentence[ij]+"/"+postag)
    # print c
    return word_tags

def calculate_prob(val1,val2,val3):
    prob=val1*val2*val3
    return prob
    
def viterbi_algo(sentence, start, total,states, postags, transition, emission, possible_tags):
    word_prob = [defaultdict(int)]
    #c=0
    viterbi_backpointer = [defaultdict(int)]
    cur_states = states
    if sentence[0] not in possible_tags:
        #  c+=1
        for i in states:
            if i in states and start[i] > 0:
                word_prob[0][i] = calculate_prob(start[i],total,1)
                      
    else:
        cur_states = possible_tags[sentence[0]]
        for i in cur_states:
            if i in states and start[i] > 0:
                if (i+" "+sentence[0].strip()) in emission:
                    word_prob[0][i] = calculate_prob(start[i],total,emission[i+" "+sentence[0]])
        

    if "START" in states:
        states.remove("START") 
    
    for wo in range(1, len(sentence)):
        word_prob.append(defaultdict(int))
        viterbi_backpointer.append(defaultdict(int))
        cur_states = states
        if sentence[wo] in possible_tags:
            cur_states = possible_tags[sentence[wo]]
            
            for tag1 in cur_states:
                max_prob = -1
                
                for tag2 in states:
                    if((tag2 in word_prob[wo-1]) and word_prob[wo-1][tag2] > 0):
                       if((tag1+" "+sentence[wo]) in emission):
                            probvalv = calculate_prob(word_prob[wo-1][tag2],transition[tag2+" "+tag1],emission[tag1+" "+sentence[wo]])
                            if max_prob <= probvalv :
                                max_prob = probvalv
                                viterbi_backpointer[wo][tag1] = tag2
                word_prob[wo][tag1] = max_prob
                
        else:
            
            for tag1 in states:
                max_prob = -1
                for tag2 in states:
                    if((tag2 in word_prob[wo-1]) and word_prob[wo-1][tag2] > 0):
                        probvalv = calculate_prob(word_prob[wo-1][tag2],transition[tag2+" "+tag1],1)
                        if max_prob <= probvalv :
                            max_prob = probvalv
                       # max_prob = max(max_prob,probvalv)
                            viterbi_backpointer[wo][tag1] = tag2
                word_prob[wo][tag1] = max_prob
    return gettags(states,word_prob,viterbi_backpointer,sentence,possible_tags)
                
                
def calctransition(val,tag1,num):
    va=(int(val) + 1)
    de=(int(tag1) + num)
    return float(va/de)

def calculateemission(count,val):
    c=int(count)
    v=int(val)
    return float(c/v)
    
f=open("hmmmodel.txt","r")
nums=int(f.readline())
#r=open("1.txt","w")
for line in f.readlines():
   # if line.startswith("T"):
    temp = line.rstrip("\n").split(" ")
    if temp[0]=="POSTAGS":
        postags[temp[1]] = int(temp[2])
        states.add(temp[1])
    elif temp[0]=="TRANSITION":
        key=temp[1]+" "+temp[2]
        transition[key] = calctransition(temp[3],postags[temp[1]],nums)
        if temp[1]=="START":
            start[str(temp[2])] += int(temp[3])
            total += int(temp[3])
    
    elif temp[0]=="EMISSION":
        key=temp[1]+" "+temp[2]
        emission[key] = calculateemission(temp[3],postags[temp[1]])    
        
    elif temp[0]=="WORD":
        word = temp[1].strip()
        if word not in possible_tags:
            possible_tags[word] = set()
        tags = temp[2].strip().rstrip(";").strip()
        tags = tags.split(";")
        for tag in tags:
            possible_tags[word].add(tag.strip())

            
          #  r.write(str(possible_tags[word])+"***"+str(tag)+">>>>"+str(word)+"\n")

output = open("hmmoutput.txt", 'w')
f=open("ip1.txt","r")
for line in f.readlines():
    sentence = line.rstrip("\n").split(" ")
    
    POSTags = viterbi_algo(sentence, start,total,states, postags, transition, emission, possible_tags)
    for i in range(len(POSTags)-1, -1, -1):
        output.write(str(POSTags[i])+" ")
    output.write("\n")
        
          

