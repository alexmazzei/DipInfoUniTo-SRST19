from __future__ import print_function
import io
import os
import numpy
from sets import Set
from collections import OrderedDict
from conllu import parse, parse_tree
# encoding=utf8  
import sys  
reload(sys)  
sys.setdefaultencoding('utf8')

from polyglot.mapping import Embedding #there are other embeddings to test, for instance glove



featuresFile = sys.argv[1]  #File UD used only to create the "feature
                            #set". The features values will be
                            #numeric: 0/1 or real
encodeFile   = sys.argv[2]  #File UD that will be encoded into a
                            #numeric CSV file representing the feature
                            #values

globalInteger = 1;          #global index



#NOTE: exploreTree is a recursive function that explore top-down the tree and prints to the console




def exploreTree(tn):
    global globalInteger
    if(tn.children):
        #print globalInteger , "---------" , globalInteger#DEBUG
        d = {"depRel" :  tn.data.get("deprel") , "uPoS" :  tn.data.get("upostag"), "xPoS" :  tn.data.get("xpostag") , "lemma" :  tn.data.get("lemma"), "groupId" : globalInteger, "originalPosition" : tn.data.get("feats").get("original_id") , "form" : tn.data.get("form"), "feats" : tn.data.get("feats"), "isHead" : True}
        l=[d]
        for c in tn.children:
            dc = {"depRel" :  c.data.get("deprel") , "uPoS" :  c.data.get("upostag") ,"xPoS" :  c.data.get("xpostag") , "lemma" :  c.data.get("lemma"), "groupId" : globalInteger, "originalPosition" : c.data.get("feats").get("original_id") , "form" : c.data.get("form"), "feats" : c.data.get("feats"), "isHead" : False}
            l.append(dc)
        newL = sorted (l,key = lambda x : x['originalPosition'])
        i = 1
        for el in newL:
            el["newPosition"]=i
            i += 1
        out = ""#groupId,lemma,uPoS,xPos,dep,isHead,newPosition
        for node in newL:
            #out = out+"lemma="+node.get('lemma')
            out = out + str (node.get('groupId')) + ','
            #Embeddings
            embLemma = emb.get(str(node.get('lemma')))
            #embLemma = emb.get(str(node.get('form')))#In SRST18 lemma and forma are inverted!!!
            #print("uPos="+node.get("uPoS"))
            if ((node.get("uPoS") not in closedUPoS) and (embLemma is not None)):
                #print("Sono qui!!"+node.get("uPoS"))
                for n in embLemma:
                    out = out + str(n) +","
            else:
                out = out + "0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,"#TODO
            #ClosedLemma
            if( lemma2HVRlemma.has_key(node.get('lemma'))):
                out = out +lemma2HVRlemma.get(node.get('lemma'))  + ","
            else:
                out = out + lemma2HVRlemma.get('UNK')+ ","
            if(uPoS2HVRuPoS.has_key(node.get('uPoS'))):
                out = out + uPoS2HVRuPoS.get(node.get('uPoS'))  + ","
            else:
                out = out + uPoS2HVRuPoS.get('UNK')  + ","
            if(xPoS2HVRxPoS.has_key(node.get('xPoS')) ):#NO for PT!!!
                out = out + xPoS2HVRxPoS.get(node.get('xPoS'))  + ","
            else:
                out = out + xPoS2HVRxPoS.get('UNK')  + ","
            if (node.get("feats") is not None):
                for key in mfeat2HVR:
                    #print("k="+key)
                    #print("f+k="+str(node.get("feats").get(key)))
                    if (((node.get("feats").get(key)) is not None) and (mfeat2HVR[key].get(node.get("feats").get(key)) is not None)):
                        out = out + mfeat2HVR[key][node.get("feats").get(key)]  + ","
                    else:
                        out = out + mfeat2HVR[key][u'NaV']  + ","
            else:
                for key in mfeat2HVR:
                    out = out + mfeat2HVR[key][u'NaV']  + ","
            if(dep2HVRdep.has_key(node.get('depRel'))):
                out = out + dep2HVRdep.get(node.get('depRel'))  + ","
            else:
                out = out + dep2HVRdep.get('UNK')  + ","
            if node.get('isHead'):
                out = out + "1,"
            else:
                out = out + "0,"
            out = out + str( node.get('newPosition')) + "\n"
        print(out,end="")
        globalInteger = globalInteger + 1
        
        for c in tn.children:            
            exploreTree(c)
            


# >>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>            
# read the entire feature file to extract features and convert to binary string
# >>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>


# #embeddings !!!LANGUAGE DEPENDENT!!!
emb = Embedding.load("/home/ubuntu/polyglot_data/embeddings2/it/embeddings_pkl.tar.bz2")
#emb = Embedding.load("/Users/mazzei/polyglot_data/embeddings2/en/embeddings_pkl.tar.bz2")
#emb = Embedding.load("/Users/mazzei/polyglot_data/embeddings2/fr/embeddings_pkl.tar.bz2")
#emb = Embedding.load("/Users/mazzei/polyglot_data/embeddings2/es/embeddings_pkl.tar.bz2")
#emb = Embedding.load("/Users/mazzei/polyglot_data/embeddings2/pt/embeddings_pkl.tar.bz2")


# list of the closed PoS tags in Google PoS set
closedUPoS = ['ADP','AUX','CCONJ','DET','PART','PRON','SCONJ','PUNCT'] 


lemmaSet =  Set([u'UNK'])
upostagList = [u'UNK']
xpostagList = [u'UNK']
deprelList = [u'UNK']
mfeatsDict = {}


file1 = open(featuresFile)
stringTree =""
for line in file1:
    if(line != '\n'):        
        stringTree += line
    else:
        #print(stringTree)#DEBUG
        flatTree = parse(stringTree)
        for node in flatTree[0]:
            if ((node.get("upostag") in closedUPoS) and (node.get("lemma") not in lemmaSet)):
                lemmaSet.add(node.get("lemma"))
                #print("closedLemma="+(node.get("lemma")))
            if (node.get("upostag") not in upostagList):
                upostagList.append(node.get("upostag"))
            if (node.get("xpostag") not  in xpostagList):
                xpostagList.append(node.get("xpostag"))
            if (node.get("feats") is not None):
                for i, (key, value) in enumerate(node.get("feats").iteritems()):
                    #print(key+value)                    
                    if (key != "lin" and key != "original_id"): ##2019 
                        if (key not in mfeatsDict):
                            mfeatsDict[key] =[u'NaV']
                            mfeatsDict[key].append(value)
                        else:
                            if (value not in mfeatsDict[key]):
                                mfeatsDict[key].append(value)
            if (node.get("deprel") not in deprelList):
                deprelList.append(node.get("deprel"))
        stringTree = ""
lemmaList = list(lemmaSet)


lemma2HVRlemma = {} #NOTE: HVR is used only for closed PoS categories.
for lemma,i in zip (lemmaList,range(len(lemmaList))):
    lemma2HVRlemma[lemma] = ",".join(map(str, numpy.eye(len(lemmaList), dtype=int)[i]))
#print("lemma2HVRlemma="+str(lemma2HVRlemma))
uPoS2HVRuPoS = {}
for uPoS,i in zip (upostagList,range(len(upostagList)) ):
    uPoS2HVRuPoS[uPoS] = ",".join(map(str, numpy.eye(len(upostagList), dtype=int)[i]))
xPoS2HVRxPoS = {}
for xPoS,i in zip (xpostagList,range(len(xpostagList)) ):
    xPoS2HVRxPoS[xPoS] = ",".join(map(str, numpy.eye(len(xpostagList), dtype=int)[i]))        
dep2HVRdep = {}
for dep,i in zip (deprelList,range(len(deprelList)) ):
    dep2HVRdep[dep] = ",".join(map(str, numpy.eye(len(deprelList), dtype=int)[i]))
mfeat2HVR = {}
for key in mfeatsDict:
    mfeat2HVR[key] ={}
    for value,i in zip (mfeatsDict[key],range(len(mfeatsDict[key]))):
        mfeat2HVR[key][value] = ",".join(map(str, numpy.eye(len(mfeatsDict[key]), dtype=int)[i]))
        #print(key+"-"+value+"="+mfeat2HVR[key][value])


#NOTE: this is the main alghorithm        
#read the conll file and process the tree one-by-one to convert in 0-1
file = open(encodeFile)
stringTree =""
for line in file:
    if(line != '\n'):        
        stringTree += line
    else:
        #print(stringTree)#DEBUG
        exploreTree(parse_tree(stringTree)[0])
        stringTree = ""



