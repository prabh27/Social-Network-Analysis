'''
Created on 10-Apr-2015

@author: Ritesh
'''

authorNum = {}

f1 = open("C:/Users/Ritesh/Desktop/LiveJournalDatasets/FlickrDataset/data_stats/groupKLD.txt","r")
g1 = open("C:/Users/Ritesh/Desktop/LiveJournalDatasets/FlickrDataset/data_stats/groupPopularityKLD.txt","r")
h1 = open("C:/Users/Ritesh/Desktop/LiveJournalDatasets/FlickrDataset/data_stats/groupKLD.txt","r")

nf = open("C:/Users/Ritesh/Desktop/LiveJournalDatasets/FlickrDataset/data_stats/groupNewKLD.txt","w")

def createMap():
    with open("C:/Users/Ritesh/Desktop/LiveJournalDatasets/FlickrDataset/csvs_and_sql/authorNumbers.txt","r") as f:
        for line in f:
            line = line[0:-1]
            l = line.split("-")
            if authorNum.has_key(l[0])==False:
                authorNum[l[0]] = l[1]

def readFiles():
    lc = 1
    for line in f1:
        print lc
        lc+=1
        x = g1.readline()
        x = x[0:-1]
        line = line[0:-1]
        x1 = x.split(" ")
        l = line.split(" ")
        w = float(x1[2])+ float(l[2])
        nf.write(authorNum[l[0]]+ " " + authorNum[l[1]] + " " + str(w)+"\n")
        nf.flush()
        
createMap()
readFiles()
        