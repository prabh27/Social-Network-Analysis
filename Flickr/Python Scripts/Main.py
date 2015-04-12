'''
Created on 19-Mar-2015

@author: Ritesh
'''
import MySQLdb

db = MySQLdb.connect("localhost","root","ritesh","flickr_data")
authorMap = {}
cursor = db.cursor()
myfile = open("C:/Users/Ritesh/Desktop/LiveJournalDatasets/FlickrDataset/authorEdges.txt","a")
photoMap = {}

def imageAuthor():
    query = "Select * from author_photos_tags_u"
    cursor.execute(query)
    results = cursor.fetchall()
    print cursor.rowcount
    for row in results:
        photoMap[row[1]] = row[0]

def authorEdges():
    lc = 0
    with open("C:/Users/Ritesh/Desktop/LiveJournalDatasets/FlickrDataset/flickrEdges/flickrEdges.txt", 'r') as f:
        for line in f:
            #print line
            lc+=1
            print lc
            id1, id2 = map(str, line.split())
            if photoMap.has_key(id1) and photoMap.has_key(id2) and photoMap[id1]!=photoMap[id2]:
                auth1 = photoMap[id1]
                auth2 = photoMap[id2]
                if authorMap.has_key(auth1+","+auth2) or authorMap.has_key(auth2+","+auth1):
                    x = 1
                else:
                    authorMap[auth1+","+auth2] = 1
                    myfile.write(auth1 + " " + auth2 + "\n")
                    myfile.flush()

def createAuthorEdges():
    lc = 0
    with open("C:/Users/Ritesh/Desktop/LiveJournalDatasets/FlickrDataset/flickrEdges/flickrEdges.txt", 'r') as f:
        for line in f:
            #print line
            lc+=1
            print lc
            id1, id2 = map(str, line.split())
            auth1 = ""
            auth2 = ""
            query1 = "Select author_id from author_photos_tags_u where photo_id = " + id1
            query2 = "Select author_id from author_photos_tags_u where photo_id = " + id2
            cursor.execute(query1)
            if cursor.rowcount == 0:
                continue
            #results = cursor.fetchall()
            #if results.size()
            #for row in results:
                #auth1 = row[0]
            auth1 = cursor.fetchone()[0]
            cursor.execute(query2)
            if cursor.rowcount==0:
                continue
            auth2 = cursor.fetchone()[0]
            #results = cursor.fetchall()
            #for row in results:
                #auth2 = row[0]
            #print auth1, auth2
            if auth1 != auth2:
                if authorMap.has_key(auth1+","+auth2) or authorMap.has_key(auth2+","+auth1):
                    x = 1
                else:
                    authorMap[auth1+","+auth2] = 1
                    myfile.write(auth1 + " " + auth2 + "\n")
                    myfile.flush()

imageAuthor()
authorEdges()
#createAuthorEdges()
db.close()
myfile.close()