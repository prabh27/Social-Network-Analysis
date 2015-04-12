'''
Created on 11-Apr-2015

@author: Ritesh
'''

import MySQLdb
import math
import numpy
import scipy
import gensim


db = MySQLdb.connect("localhost","root","ritesh","flickr_data")

allTags = {}
cursor = db.cursor()
sentences = []
#cursor = []

def fillTags():
    query = "select * from author_photos_tags"
    cursor.execute(query)
    res = cursor.fetchall()
    for row in res:
        if allTags.has_key(row[0])==False:
            val = row[2][1:-1]
            l = val.split(",")
            for i in range(len(l)):
                l[i] = l[i].strip()
            sentences.append(l)
            allTags[row[0]] = l
        else:
            k = allTags[row[0]]
            val = row[2][1:-1]
            l = val.split(",")
            for i in range(len(l)):
                l[i] = l[i].strip()
            sentences.append(l)
            for i in range(len(l)):
                if l[i].strip() not in k:
                    k.append(l[i].strip())
    print "Total Sentences", len(sentences)

def findJaccardSim():
    myfile = open("C:/Users/Ritesh/Desktop/LiveJournalDatasets/FlickrDataset/data_stats/tagJaccardSim.txt", "w")
    lc = 1
    with open("C:/Users/Ritesh/Desktop/LiveJournalDatasets/FlickrDataset/data_stats/authorEdges.csv", "r") as f:
        for line in f:
            line = line[0:-1]
            print lc
            lc+=1
            l = line.split(" ")
            if allTags.has_key(l[0])==False or allTags.has_key(l[1])==False:
                continue
            
            s1 = set(allTags[l[0]])
            s2 = set(allTags[l[1]])
            
            sim = float(len(s1.intersection(s2)))/len(s1.union(s2))
            myfile.write(l[0]+" "+l[1]+" "+str(sim)+"\n")
            myfile.flush()

def findCosineSimilarity():
    print "Cosine"
    model = gensim.models.Word2Vec(sentences, workers=4, min_count=1)
    print "Training Done"
    
    myfile = open("C:/Users/Ritesh/Desktop/LiveJournalDatasets/FlickrDataset/data_stats/tagCosine.txt", "w")
    lc = 1
    with open("C:/Users/Ritesh/Desktop/LiveJournalDatasets/FlickrDataset/data_stats/authorEdges.csv", "r") as f:
        for line in f:
            line = line[0:-1]
            print lc
            lc+=1
            l = line.split(" ")
            if allTags.has_key(l[0])==False or allTags.has_key(l[1])==False:
                continue
            val = 0.0
            try:
                val = model.n_similarity(allTags[l[0]], allTags[l[1]])
            except:
                pass
            
            myfile.write(l[0]+" "+l[1]+" "+str(val)+"\n")
            myfile.flush()
    


fillTags()
findCosineSimilarity()
#findJaccardSim()       
            

