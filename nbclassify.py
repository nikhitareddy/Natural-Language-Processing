import os
import string
import sys
import re
from collections import OrderedDict
def getModel():
	fi=open('nbmodel.txt','r')
	q=fi.readline()
	q=q.split()
	pri_tp=q[0]
	pri_dp=q[1]
	pri_tn=q[2]
	pri_dn=q[3]
	dicList={}
	for line in fi:
		com=line.split(' ')
		dicList[com[0]]=[]
		dicList[com[0]].append(com[1])
		dicList[com[0]].append(com[2])
		dicList[com[0]].append(com[3])
		dicList[com[0]].append(com[4].replace("\n",""))
		
	return dicList,	pri_tp, pri_dp, pri_tn, pri_dn 	
def simplify(f):
	text=''
	for line in f:
		text=text+line
	text=text.lower()
	text=text.translate(string.maketrans("",""), string.punctuation)
	return text	

def count(text):
	wordDict={}
	words=text.split()
	for j in range(0, len(words)):
		if words[j] in wordDict.keys():
			wordDict[words[j]]=wordDict[words[j]]+1
		else:
			wordDict[words[j]]=1
	return wordDict
def removehighandlow(wordDict):
	wordCount=0
	totalOccur=0
	for key in wordDict.keys():
		wordCount=wordCount+1
		totalOccur=totalOccur+wordDict[key]
	averageOccur=totalOccur/wordCount	
	for key in wordDict.keys():
		#if wordDict[key]>=100*averageOccur or wordDict[key]*100<=averageOccur or wordDict[key]==1:
		if wordDict[key]>=100 or wordDict[key]*100<=averageOccur:
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
def getalpha(fil):
   # print fil,'filfiflfil'
    f=fil.split()
    #print f,'ffff'
    al=''
    al=f[0]
    return al
def getreview(fil):
    fil=fil.replace(getalpha(fil),'')
    return fil
    
def getClass(path):
    dictLists={}
    for i in (path):
            #print i
            alpha=getalpha(i)
            #print alpha
            filepath=getreview(i)
            text=simplify(filepath)	
            wordDict=count(text)
            wordDict=removestopwords(wordDict)
            wordDict=removedigits(wordDict)
            wordDict=removeshortlongwords(wordDict)
            wordDict=removehighandlow(wordDict)
            dictLists[alpha]=wordDict	
    return dictLists

def writefile(res):
        fileout=open('nboutput.txt','w')
        for i in range(len(res)):
                fileout.write(res[i])
                fileout.write('\n')
def getResult(dic_list,  dictLists, pri_nd, pri_nt, pri_pd, pri_pt):
    result=[]
    d={}
    #i=0
    for filepath in dictLists.keys():
            wordDict=dictLists[filepath]
            ratend=1.0
            ratent=1.0
            ratepd=1.0
            ratept=1.0
           # i=0
            for key in wordDict.keys():
                if key in dic_list.keys():
                        ratend=ratend*float(dic_list[key][3])
                        ratent=ratent*float(dic_list[key][2])
                        ratepd=ratepd*float(dic_list[key][1])
                        ratept=ratept*float(dic_list[key][0] )

            ratend=float(pri_nd)*float(ratend)	
            ratent=float(pri_nt)*float(ratent)
            ratepd=float(pri_pd)*float(ratepd)
            ratept=float(pri_pt)*float(ratept)	
            maxrate=max(ratend, ratent, ratepd, ratept)
            if maxrate==ratend:
                    result.append(filepath+" deceptive negative ")
                    
            elif maxrate==ratent:
                    result.append(filepath+" truthful negative ")
                   
            elif maxrate==ratepd:
                    result.append(filepath+" deceptive positive ")
                   
            elif maxrate==ratept:
                    result.append(filepath+" truthful positive ")

    writefile(result)

dict_list, pri_tp, pri_dp, pri_tn, pri_dn=getModel()

path=sys.argv[1]

dictLists=getClass(path)

result=[]
result=getResult( dict_list, dictLists, pri_tp, pri_dp, pri_tn, pri_dn)
