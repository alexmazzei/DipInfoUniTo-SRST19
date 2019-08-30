from __future__ import print_function
import io
import os
import numpy
from collections import OrderedDict
from conllu import parse, parse_tree
# encoding=utf8  
import sys  
reload(sys)  
sys.setdefaultencoding('utf8')


#testfile = "test-listnet-test-it.txt"#"test-02.conll"#
#HVRPredFile = "it-test-HVR-PoSDeP.txt.pred"
#HVRPredFile = "ud-it-test-UXMDEP-H1V.txt.pred"
#HVRPredFile = "ud-it-test-WEUXMDEP-H1V.txt.pred"
#HVRPredFile = "ud-it-test-WELUXMDEP-H1V.txt.gold"
#HVRPredFile = "ud-it-test-WELUXMDEP-H1V-25.txt.pred"
#HVRPredFile = "ud-it-test-WELUXMDEP-H1V-35.txt.pred"

#testfile = "it-results-srst18.morpho.conll"
#HVRPredFile = "ud-it-SRST-WELUXMDEP-tr-H1V.txt.pred"#35
testfile = sys.argv[1]#"en-results-srst18.morpho.conll"
HVRPredFile = sys.argv[2]#"ud-en-SRST-WELUXMDEP-tr-H1V.txt.pred"#35


fileHVRPredFile = open(HVRPredFile)

def augmentTree(tn):
    #tn.children.sort(key = lambda x : x.data["id"])
    if(tn.children):
        i = 0
        while ((i < len(tn.children)) and (tn.children[i].data.get("id") < tn.data.get("id")) ):
            tn.children[i].data["predictedIslandPosition"] = int(fileHVRPredFile.readline())
            i+=1
        tn.data["predictedIslandPositionH"] = int(fileHVRPredFile.readline())
        while (i < len(tn.children)):
            tn.children[i].data["predictedIslandPosition"] = int(fileHVRPredFile.readline())
            i+=1
        for c in tn.children:
            augmentTree(c)
    else:
        tn.data["predictedIslandPositionH"] = 1#int(fileHVRPredFile.readline())
        
def visitNewPositionTree(tn):
    global realPosition;
    tn.children.sort(key = lambda x : x.data["predictedIslandPosition"])
    if(not(tn.children)):
        #print(tn.data.get("form") +"-"+ str(tn.data.get("predictedIslandPosition"))+"-"+str(realPosition)+"-"+str(tn.data.get("id")))
        print(tn.data.get("form"),end=" ")
        realPosition += 1 
    else:
        i = 0
        while ((i < len(tn.children)) and (tn.children[i].data.get("predictedIslandPosition") < tn.data.get("predictedIslandPositionH"))):
            visitNewPositionTree(tn.children[i])
            i+=1
        #print(tn.data.get("form")+"-"+ str(tn.data.get("predictedIslandPositionH"))+"-"+str(realPosition)+"-"+str(tn.data.get("id")))
        print(tn.data.get("form"),end=" ")
        realPosition += 1 
        while (i < len(tn.children)):
            #print("Sono qui!!!")
            visitNewPositionTree(tn.children[i])
            i+=1

        
#read the conll file and process the tree one-by-one
file = open(testfile)
sentenceNumber = 1
stringTree =""
for line in file:
    if(line != '\n'):        
        #print line#DEBUG
        stringTree += line
    else:
        #print(stringTree)#DEBUG
        tree = parse_tree(stringTree)[0]
        #print(tree)
        realPosition = 1;
        augmentTree(tree)
        print("# sent_id ="+str(sentenceNumber)+"\n# text =",end=" ")
        visitNewPositionTree(tree)
        print("\n")
        stringTree = ""
        sentenceNumber = sentenceNumber + 1



#(evaluation) Alessandro-Mazzeis-MacBook-Pro:bin mazzei$ python eval_Py2.py /Users/mazzei/lavori/Software/SharedTaskNLG18/ud2ln/ud2ln/result/ /Users/mazzei/lavori/Software/SharedTaskNLG18/ud2ln/ud2ln/gold/


#python hard_attention.py   --dynet-gpus=1 --input=100 --hidden=100 --feat-input=20 --epochs=100 --layers=2 --optimization=ADADELTA /home/mazzei/software/morprho/morphological-reinflection/data/test1/train/french_train.txt.sigmorphon_format.txt /home/mazzei/software/morprho/morphological-reinflection/data/test1/dev/french_dev.txt.sigmorphon_format.txt /home/mazzei/software/morprho/morphological-reinflection/data/test1/test/french_test.txt.sigmorphon_format.txt /home/mazzei/software/morprho/morphological-reinflection/data/test1/results/results.txt /home/mazzei/software/morprho/sigmorphon2016/ > msg.txt 2> err.txt &



#/home/mazzei/software/morprho/morphological-reinflection/data/test-inst


#python hard_attention.py   --dynet-gpus=1 --input=100 --hidden=100 --feat-input=20 --epochs=100 --layers=2 --optimization=ADADELTA /home/mazzei/software/morprho/morphological-reinflection/data/test-inst/train/german-train.txt /home/mazzei/software/morprho/morphological-reinflection/data/test-inst/dev/german-dev.txt /home/mazzei/software/morprho/morphological-reinflection/data/test-inst/test/german-test.txt /home/mazzei/software/morprho/morphological-reinflection/data/test-inst/results/german-results.txt /home/mazzei/software/morprho/sigmorphon2016/ > msg.txt 2> err.txt &
