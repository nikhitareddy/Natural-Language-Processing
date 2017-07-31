import os
import string
import pickle
import sys
import re
import math
from _collections import defaultdict
dp=[]
dn=[]
tp=[]
tn=[]
dptext=[]
dntext=[]
tptext=[]
tntext=[]
p=sys.argv[1]
p1=sys.argv[2]
p2=sys.argv[1]
script_dir = os.path.dirname(__file__) #<-- absolute dir the script is in
f1 = open(p1, "r")
f = open(p, "r")
f2 = open(p2, "r")

r=[]
q=[]

for i in range(1280):
    r.append(f.readline().split())
    q.append(f1.readline().split())
w=(f2.readlines())


s=""
cat=[]
for i in range(1280):
    if r[i][0]==q[i][0]:
        s=q[i][1]+q[i][2]
        cat.append(s)
for i in range(1280):
    w[i]=w[i].replace(q[i][0],'')
    w[i]=w[i].replace('\n','')
def splitwords(lis,label):
    tplist=[]
    tnlist=[]
    dplist=[]
    dnlist=[]
    dpcount=0
    tpcount=0
    dncount=0
    tncount=0
    master=[]
    
    if label=="dp":
        for i in range(len(lis)):
            w=lis[i].split()
            for j in range(len(w)):
                dplist.append(w[j])
                dpcount+=1
        return dplist,dpcount
    if label=="dn":
        for i in range(len(lis)):
            w=lis[i].split()
            for j in range(len(w)):
                dnlist.append(w[j])
                dncount+=1
        return dnlist,dncount
    if label=="tn":
        for i in range(len(lis)):
            w=lis[i].split()
            for j in range(len(w)):
                tnlist.append(w[j])
                tncount+=1
        return tnlist,tncount
    if label=="tp":
        for i in range(len(lis)):
            w=lis[i].split()
            for j in range(len(w)):
                tplist.append(w[j])
                tpcount+=1
        return tplist,tpcount
for i in range(1280):
    if q[i][1]=="truthful":
        if q[i][2]=="positive":
            tp.append(q[i][0])
            tptext.append(w[i])
            tru,tcount=splitwords(tptext,"tp")
        else:
            tn.append(q[i][0])
            tntext.append(w[i])
            trun,tncount=splitwords(tntext,"tn")
    elif q[i][1]=="deceptive":
        if q[i][2]=="positive":
            dp.append(q[i][0])
            dptext.append(w[i])
            dec,dcount=splitwords(dptext,"dp")
        else:
            dn.append(q[i][0])
            dntext.append(w[i])
            decn,dncount=splitwords(dntext,"dn")

def count(l):
    dic={}
    #count=1
    for i in range(len(l)):
        word=l[i].split()
        #print word
        for k in range(len(word)):
            if word[k] in dic:
               # print dic[word[k]]
                dic[word[k]]=dic[word[k]]+1
            else:
                dic[word[k]]=1
    return dic

	#return wordDict

def allwords(d):
    allword=[]
    for key in d:
        if key not in allword:
            allword.append(key)
    return allword
def simplify(wordDict):
	#f=open(filepath, 'r')
	text={}
	for key in wordDict.keys():
		t=key.lower()
		t=t.translate(string.maketrans("",""), string.punctuation)
		text[t]=wordDict[key]
	return text
                
	         
def removehighandlow(wordDict):
	wordCount=0
	totalOccur=0
	for key in wordDict.keys():
		wordCount=wordCount+1
		totalOccur=totalOccur+wordDict[key]
	averageOccur=totalOccur/wordCount	
	#print totalOccur/wordOccunt
	for key in wordDict.keys():
		#if wordDict[key]>=100*averageOccur or wordDict[key]*100<=averageOccur or wordDict[key]==1:
		if wordDict[key]>=100 or wordDict[key]*100<=averageOccur:
			#print key," ",wordDict[key]
			del wordDict[key]
	return wordDict	
def removestopwords(wordDict):
	stopwords=['i','a','about','an','are','as','at','be','by','com','de','en','for','from','how','in',
	'is','it','la','of','on','or','that','the','this','to','was','what','when','where','who','will','with',
	'and','the','www'] 
	for key in wordDict.keys():
		if key in stopwords:
			del wordDict[key]
	return wordDict	
def removedigits(wordDict):
	pattern = re.compile('\d')
	for key in wordDict.keys():
		if key.isdigit() or bool(pattern.search(key))==True:
			del wordDict[key]
	return wordDict
def removeshortlongwords(wordDict):
	for key in wordDict.keys():
		if len(key)<=4 or len(key)>=15:
			del wordDict[key]
	return wordDict
def getprob(li):
    ratend=1.0
    ratent=1.0
    ratepd=1.0
    ratept=1.0
    dict_nd=count(decn)
    dict_nt=count(trun)
    dict_pt=count(tru)
    dict_pd=count(dec)
    xyz=count(li)
    di=allwords(xyz)
    v=len(di)
    #print v
    prelen_nd=dncount
    prelen_nt=tncount
    prelen_pd=dcount
    prelen_pt=tcount
    dic={}
    
    for key in range(len(di)):
        #print di[key]
        if di[key] not in dict_pt:
              
                dic.setdefault(di[key], []).append((float(1)/float(prelen_pt+v)))
                
        else:
                dic.setdefault(di[key], []).append((float(int(dict_pt[di[key]])+1)/float(prelen_pt+v)))
        if di[key] not in dict_pd:
              
                dic.setdefault(di[key], []).append((float(1)/float(prelen_pd+v)))
               
        else:
               dic.setdefault(di[key], []).append((float(int(dict_pd[di[key]])+1)/float(prelen_pd+v)))
        
        
                
       
        if di[key] not in dict_nt:
               
                dic.setdefault(di[key], []).append((float(1)/float(prelen_nt+v)))
                
        else:
                dic.setdefault(di[key], []).append((float(int(dict_nt[di[key]])+1)/float(prelen_nt+v)))
                
        if di[key] not in dict_nd:
                
                dic.setdefault(di[key], []).append((float(1)/float(prelen_nd+v)))
                
        else:
               
                dic.setdefault(di[key], []).append((float(int(dict_nd[di[key]])+1)/float(prelen_nd+v)))
        
        
    writefile(dic)
    
total=len(tptext)+len(tntext)+len(dptext)+len(dntext)
pri_tp=float(len(tptext))/float(total)
pri_dp=float(len(dptext))/float(total)
pri_tn=float(len(tntext))/float(total)

pri_dn=float(len(dntext))/float(total)

def writefile(dic):
    fModel=open('nbmodel.txt', 'w')
    fModel.write(str(pri_tp)+" "+str(pri_dp)+" "+str(pri_tn)+" "+str(pri_dn)+"\n")
    for key in dic:
        fModel.write(key+" "+str(dic[key][0])+" "+str(dic[key][1])+" "+str(dic[key][2])+" "+str(dic[key][3])+"\n")
    fModel.close()

wordDict=count(w)
wordDict=simplify(wordDict)
wordDict=removestopwords(wordDict)
wordDict=removedigits(wordDict)
wordDict=removeshortlongwords(wordDict)
wordDict=removehighandlow(wordDict)
r=[]
for k in wordDict:
    r.append(k)
getprob(r)    

       
