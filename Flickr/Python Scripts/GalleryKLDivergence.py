'''
Created on 02-Apr-2015

@author: Ritesh
'''

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
authorToGalleryCount = {}
authorToGallery = {}
galleries = {}
myfile = open("C:/Users/Ritesh/Desktop/LiveJournalDatasets/FlickrDataset/data_stats/commentGraphgalleryContributionKLD.txt","a")
myfile1 = open("C:/Users/Ritesh/Desktop/LiveJournalDatasets/FlickrDataset/data_stats/commentGraphgalleryPopularityKLD.txt","a")

def readGalleryInfo():
    query = "select gallery from author_gallery_distribution"
    cursor.execute(query)
    res = cursor.fetchall()
    for r in res:
        if galleries.has_key(r[0])==False:
            if r[0] == "cactus":
                x = 1
            galleries[r[0]] = 0


def loadMaps():
    query = "select * from author_gallery_distribution"
    cursor.execute(query)
    res = cursor.fetchall()
    for r in res:
        if authorToGalleryCount.has_key(r[0])==False:
            l = []
            l.append(r[1]+"|;*:|"+r[2])
            authorToGalleryCount[r[0]] = l
            
            k = []
            k.append(r[1])
            authorToGallery[r[0]] = k
        else:
            l = authorToGalleryCount[r[0]]
            l.append(r[1]+"|;*:|"+r[2])
            authorToGalleryCount[r[0]] = l
            
            k = authorToGallery[r[0]]
            k.append(r[1])
            authorToGallery[r[0]] = k
    
        val = galleries[r[1]]
        val+=int(r[2])
        galleries[r[1]] = val

  
def generateKLDForGalleryPopularity():
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
            if authorToGalleryCount.has_key(auth1)==False or authorToGalleryCount.has_key(auth2)==False:
                gc1.append(0.0)
                gc2.append(0.0)
                myfile1.write(auth1+" "+auth2+" "+"0.0"+"\n")
                myfile1.flush()
                continue
            
            g1 = authorToGalleryCount[auth1]
            g2 = authorToGalleryCount[auth2]
            
            l1 = authorToGallery[auth1]
            l2 = authorToGallery[auth2]
            i = 0
            kld = 0.0
            
            totalPostAuth1 = 0
            totalPostAuth2 = 0
            
            for i in range(len(g1)):
                x = g1[i].split("|;*:|")
                totalPostAuth1 += int(x[1])
            
            for i in range(len(g2)):
                x = g2[i].split("|;*:|")
                totalPostAuth2 += int(x[1])
            
            for i in range(len(l1)):
                for j in range(len(l2)):
                    if l1[i]==l2[j]:
                        x = g1[i].split("|;*:|")                        
                        v1 = int(x[1])/float(totalPostAuth1)
                        
                        y = g2[j].split("|;*:|")
                        v2 = int(y[1])/float(totalPostAuth2)
                        
                        if math.ceil(v1)!=0 and math.ceil(v2)!=0:
                            kld += (v1 * math.log(v1/v2, 2)) + (v2*math.log(v2/v1, 2))
                
            #if kld>0:
                #print str(auth1+","+auth2)
            myfile1.write(auth1+" "+auth2+" "+str(kld)+"\n")
            myfile1.flush()
        
def generateKLDForGalleryContribution():
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
            if authorToGalleryCount.has_key(auth1)==False or authorToGalleryCount.has_key(auth2)==False:
                gc1.append(0.0)
                gc2.append(0.0)
                myfile.write(auth1+" "+auth2+" "+"0.0"+"\n")
                myfile.flush()
                continue
            
            g1 = authorToGalleryCount[auth1]
            g2 = authorToGalleryCount[auth2]
            
            l1 = authorToGallery[auth1]
            l2 = authorToGallery[auth2]
            i = 0
            kld = 0.0
            
            for i in range(len(l1)):
                for j in range(len(l2)):
                    if l1[i]==l2[j]:
                        x = g1[i].split("|;*:|")
                        v1 = int(x[1])/float(galleries[l1[i]])
                        
                        y = g2[j].split("|;*:|")
                        v2 = int(y[1])/float(galleries[l2[j]])
                        
                        if math.ceil(v1)!=0 and math.ceil(v2)!=0:
                            kld += (v1 * math.log(v1/v2, 2)) + (v2*math.log(v2/v1, 2))
                
            #if kld>0:
                #print str(auth1+","+auth2)
            myfile.write(auth1+" "+auth2+" "+str(kld)+"\n")
            myfile.flush()
            
readGalleryInfo()
loadMaps()
generateKLDForGalleryContribution()
generateKLDForGalleryPopularity()