'''
Created on 31-Mar-2015

@author: Ritesh
'''

import MySQLdb
import math

db = MySQLdb.connect("localhost","root","ritesh","flickr_data")
MySQLdb.escape_string("@")
authorMap = {}
cursor = db.cursor()
uniqueGrps = {}
authorToGroupCount = {}
authorToGroup = {}
groups = {}
myfile = open("C:/Users/Ritesh/Desktop/LiveJournalDatasets/FlickrDataset/data_stats/commentGrpahGroupContributionKLD.txt","a")
myfile1 = open("C:/Users/Ritesh/Desktop/LiveJournalDatasets/FlickrDataset/data_stats/commentGraphGroupPopularityKLD.txt","a")

def readGroupInfo():
    query = "select distinct(group_id) from author_groupid_distribution"
    cursor.execute(query)
    res = cursor.fetchall()
    for r in res:
        if groups.has_key(r[0])==False:
            groups[r[0]] = 0


def loadMaps():
    query = "select * from author_groupid_distribution"
    cursor.execute(query)
    res = cursor.fetchall()
    for r in res:
        if authorToGroupCount.has_key(r[0])==False:
            l = []
            l.append(r[1]+"|"+r[2])
            authorToGroupCount[r[0]] = l
            
            k = []
            k.append(r[1])
            authorToGroup[r[0]] = k
        else:
            l = authorToGroupCount[r[0]]
            l.append(r[1]+"|"+r[2])
            authorToGroupCount[r[0]] = l
            
            k = authorToGroup[r[0]]
            k.append(r[1])
            authorToGroup[r[0]] = k
    
        val = groups[r[1]]
        val+=int(r[2])
        groups[r[1]] = val

  
def generateKLDForGroupPopularity():
    with open("C:/Users/Ritesh/Desktop/LiveJournalDatasets/FlickrDataset/data_stats/commentGraph.txt","r") as f:
        lc = 0
        for line in f:
            lc+=1
            print lc
            line = line[0:-1]
            l = line.split(" ")
            auth1 = l[0]
            auth2 = l[1]
            gc1 = []
            gc2 = []
            if authorToGroupCount.has_key(auth1)==False or authorToGroupCount.has_key(auth2)==False:
                gc1.append(0.0)
                gc2.append(0.0)
                myfile1.write(auth1+" "+auth2+" "+"0.0"+"\n")
                myfile1.flush()
                continue
            
            g1 = authorToGroupCount[auth1]
            g2 = authorToGroupCount[auth2]
            
            l1 = authorToGroup[auth1]
            l2 = authorToGroup[auth2]
            i = 0
            kld = 0.0
            
            totalPostAuth1 = 0
            totalPostAuth2 = 0
            
            for i in range(len(g1)):
                x = g1[i].split("|")
                totalPostAuth1 += int(x[1])
            
            for i in range(len(g2)):
                x = g2[i].split("|")
                totalPostAuth2 += int(x[1])
            
            for i in range(len(l1)):
                for j in range(len(l2)):
                    if l1[i]==l2[j]:
                        x = g1[i].split("|")                        
                        v1 = int(x[1])/float(totalPostAuth1)
                        
                        y = g2[j].split("|")
                        v2 = int(y[1])/float(totalPostAuth2)
                        
                        if math.ceil(v1)!=0 and math.ceil(v2)!=0:
                            kld += (v1 * math.log(v1/v2, 2)) + (v2*math.log(v2/v1, 2))
                
            #if kld>0:
                #print str(auth1+","+auth2)
            myfile1.write(auth1+" "+auth2+" "+str(kld)+"\n")
            myfile1.flush()
        
def generateKLDForGroupContribution():
    with open("C:/Users/Ritesh/Desktop/LiveJournalDatasets/FlickrDataset/data_stats/commentGraph.txt","r") as f:
        lc = 0
        for line in f:
            lc+=1
            print lc
            line = line[0:-1]
            l = line.split(" ")
            auth1 = l[0]
            auth2 = l[1]
            gc1 = []
            gc2 = []
            if authorToGroupCount.has_key(auth1)==False or authorToGroupCount.has_key(auth2)==False:
                gc1.append(0.0)
                gc2.append(0.0)
                myfile.write(auth1+" "+auth2+" "+"0.0"+"\n")
                myfile.flush()
                continue
            
            g1 = authorToGroupCount[auth1]
            g2 = authorToGroupCount[auth2]
            
            l1 = authorToGroup[auth1]
            l2 = authorToGroup[auth2]
            i = 0
            kld = 0.0
            
            for i in range(len(l1)):
                for j in range(len(l2)):
                    if l1[i]==l2[j]:
                        x = g1[i].split("|")
                        v1 = int(x[1])/float(groups[l1[i]])
                        
                        y = g2[j].split("|")
                        v2 = int(y[1])/float(groups[l2[j]])
                        
                        if math.ceil(v1)!=0 and math.ceil(v2)!=0:
                            kld += (v1 * math.log(v1/v2, 2)) + (v2*math.log(v2/v1, 2))
                
            #if kld>0:
                #print str(auth1+","+auth2)
            myfile.write(auth1+" "+auth2+" "+str(kld)+"\n")
            myfile.flush()
            
readGroupInfo()
loadMaps()
generateKLDForGroupContribution()
generateKLDForGroupPopularity()