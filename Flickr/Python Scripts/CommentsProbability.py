'''
Created on 10-Apr-2015

@author: Ritesh
'''
from _ctypes import COMError

totalComm = {}
commentsAsPairs = {}
commentPairProb = {}

def cleanCommentCountFile():
    cmt = open("C:/Users/Ritesh/Desktop/LiveJournalDatasets/FlickrDataset/data_stats/commentCountClean.csv","w")
    lc = 1
    with open("C:/Users/Ritesh/Desktop/LiveJournalDatasets/FlickrDataset/data_stats/commentCount.csv","r") as f:
        for line in f:
            line = line[0:-1]
            print lc
            lc+=1
            l = line.split(",")
            if l[0]!=l[1]:
                cmt.write(l[0] + "," + l[1] + "," + l[2] + "\n")
                cmt.flush()
        

def findTotalComments():
    with open("C:/Users/Ritesh/Desktop/LiveJournalDatasets/FlickrDataset/data_stats/commentCountClean.csv","r") as f:
        lc = 1
        for line in f:
            line = line[0:-1]
            print lc
            lc+=1
            l = line.split(",")
            if totalComm.has_key(l[0])==False:
                totalComm[l[0]] = int(l[2])
            else:
                val = totalComm[l[0]]
                val+=int(l[2])
                totalComm[l[0]] = val

            if commentsAsPairs.has_key(l[0]+" "+l[1])==False:
                commentsAsPairs[l[0]+" "+l[1]] = int(l[2])
            else:
                val = commentsAsPairs[l[0]+" "+l[1]]
                val+=int(l[2])
                commentsAsPairs[l[0]+" "+l[1]] = val


def findCommProb():
    count = 0
    with open("C:/Users/Ritesh/Desktop/LiveJournalDatasets/FlickrDataset/csvs_and_sql/authorEdges.csv","r") as f:
        lc = 1
        myfile = open("C:/Users/Ritesh/Desktop/LiveJournalDatasets/FlickrDataset/data_stats/commentProbability.txt","w")
        for line in f:
            line = line[0:-1]
            print lc
            lc+=1
            pr = 0.0
            l = line.split(" ")
            if commentsAsPairs.has_key(l[0]+" "+l[1])==True:
                val = commentsAsPairs[l[0]+" "+l[1]]
                pr += float(val)/totalComm[l[0]]
            if commentsAsPairs.has_key(l[1]+" "+l[0])==True:
                val = commentsAsPairs[l[1]+" "+l[0]]
                pr += float(val)/totalComm[l[1]]
            
            if pr!=0.0:
                count+=1
            myfile.write(line+" "+str(pr)+"\n")
            myfile.flush()
    print "count: ", count
    

def findCommProbAndMakeGraph():
    count = 0
    with open("C:/Users/Ritesh/Desktop/LiveJournalDatasets/FlickrDataset/data_stats/commentCountClean.csv","r") as f:
        lc = 1
        
        for line in f:
            line = line[0:-1]
            print lc
            lc+=1
            pr = 0.0
            l = line.split(",")
            if commentsAsPairs.has_key(l[0]+" "+l[1])==True:
                val = commentsAsPairs[l[0]+" "+l[1]]
                pr += float(val)/totalComm[l[0]]
            if commentsAsPairs.has_key(l[1]+" "+l[0])==True:
                val = commentsAsPairs[l[1]+" "+l[0]]
                pr += float(val)/totalComm[l[1]]
            
            if pr!=0.0:
                count+=1
            
            if commentPairProb.has_key(l[0]+" "+l[1])==True or commentPairProb.has_key(l[1]+" "+l[0])==True:
                if commentPairProb.has_key(l[0]+" "+l[1])==True:
                    val = commentPairProb[l[0]+" "+l[1]]
                    val+=pr
                    commentPairProb[l[0]+" "+l[1]] = val
                elif commentPairProb.has_key(l[1]+" "+l[0])==True:
                    val = commentPairProb[l[1]+" "+l[0]]
                    val+=pr
                    commentPairProb[l[1]+" "+l[0]] = val
            else:
                commentPairProb[l[0]+" "+l[1]] = pr
                
    print "count: ", count
    
def writeToFile():
    myfile = open("C:/Users/Ritesh/Desktop/LiveJournalDatasets/FlickrDataset/data_stats/commentGraph.txt","w")
    myfile1 = open("C:/Users/Ritesh/Desktop/LiveJournalDatasets/FlickrDataset/data_stats/commentGraphAndProbability.txt","w")
    for key in commentPairProb:
        myfile.write(key+"\n")
        myfile.flush()
        myfile1.write(key+" "+str(commentPairProb[key])+"\n")
        myfile1.flush()
        
#cleanCommentCountFile()    
findTotalComments()
findCommProbAndMakeGraph()
writeToFile()
findCommProb()

print "Total Authors: ", len(totalComm)
                