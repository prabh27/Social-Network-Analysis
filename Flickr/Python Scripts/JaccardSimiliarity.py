'''
Created on 28-Mar-2015

@author: Ritesh
'''
from time import time

import MySQLdb.cursors
from __builtin__ import list
from math import ceil

db=MySQLdb.connect(host="localhost",user="root", passwd="ritesh",db="flickr_data",cursorclass = MySQLdb.cursors.SSCursor)
cursor = db.cursor()

authors = []
authorsGroups = {}

myfile = open("C:/Users/Ritesh/Desktop/LiveJournalDatasets/FlickrDataset/data_stats/groupJaccardSimilarity.csv","a")

t = time()

def iter_row(cursor, size=1000):
    while True:
        rows = cursor.fetchmany(size)
        if not rows:
            break
        for row in rows:
            yield row

def fillAuthors():
    query = "select * from authors"
    cursor.execute(query)
    lc = 0
    for row in iter_row(cursor, 1000):
        lc+=1
        print lc
        authors.append(row[0])

def fillAuthorAndGroups():
    query = "select * from author_group_distribution"
    cursor.execute(query)
    lc = 0
    for row in iter_row(cursor, 1000):
        lc+=1
        print lc
        if authorsGroups.has_key(row[0]) == False:
            list1 = []
            if row[1] != '':
                list1.append(row[1])
            authorsGroups[row[0]] = list1
        else:
            list1 = authorsGroups[row[0]]
            if row[1] != '':
                list1.append(row[1])
            authorsGroups[row[0]] = list1

def calculateGroupJaccardSimilarity():
    for i in range(0,len(authors)):
        for j in range(i+1, len(authors)):
            if authorsGroups.has_key(authors[i]) == True and authorsGroups.has_key(authors[j]) == True:
                a = set(authorsGroups[authors[i]])
                b = set(authorsGroups[authors[j]])
                uni = a.union(b)
                inter = a.intersection(b)
                jaccardSim = 1
                if len(uni)==0 and len(inter)==0:
                    jaccardSim = 1
                elif len(uni)==0 or len(inter)==0:
                    jaccardSim = 0
                else:
                    jaccardSim = float(len(inter))/len(uni)
                if ceil(jaccardSim)==0:
                    continue
                myfile.write(authors[i]+","+authors[j]+","+str(ceil(jaccardSim * 1000) / 1000.0)+"\n")
                myfile.flush()
        

fillAuthors()
fillAuthorAndGroups()
calculateGroupJaccardSimilarity()

s = time()

print "Done with time ",
print (s-t)/1000 