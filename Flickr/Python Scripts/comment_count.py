'''
Created on 27-Mar-2015

@author: Ritesh
'''
from __future__ import generators
from collections import OrderedDict
import MySQLdb.cursors


#db = MySQLdb.connect("localhost","root","ritesh","flickr_data")
db=MySQLdb.connect(host="localhost",user="root", passwd="ritesh",db="flickr_data",cursorclass = MySQLdb.cursors.SSCursor)
cursor = db.cursor()

authorComment = {}

def iter_row(cursor, size=1):
    while True:
        rows = cursor.fetchmany(size)
        if not rows:
            break
        for row in rows:
            yield row

def countComments():
    query = "select commenter_id, commented_on_id, count from author_comments_new_u"
    cursor.execute(query)
    #res = cursor.fetchall()
    #for row in res:
    lc = 0
    for row in iter_row(cursor, 1):
        lc+=1
        print lc
        if lc==4:
            x = 1
        if authorComment.has_key(row[0]+","+row[1]) == True:
            val = authorComment[row[0]+","+row[1]]
            val += row[2]
            authorComment[row[0]+","+row[1]] = val
        elif authorComment.has_key(row[1]+","+row[0]) == True:
            val = authorComment[row[1]+","+row[0]]
            val += row[2]
            authorComment[row[1]+","+row[0]] = val
        else:
            authorComment[row[0]+","+row[1]] = row[2]

def writeToFile():
    myfile = open("C:/Users/Ritesh/Desktop/LiveJournalDatasets/FlickrDataset/data_stats/commentCount.csv","a")
    #for key in OrderedDict(sorted(authorComment.items(), key=lambda t: t[1])):
    for key in authorComment:
        myfile.write(key+","+str(authorComment[key])+"\n")
        myfile.flush()
    myfile.close()
countComments()
writeToFile()
print "Done"