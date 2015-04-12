'''
Created on 20-Mar-2015

@author: Ritesh
'''

import MySQLdb

db = MySQLdb.connect("localhost","root","ritesh","flickr_data")
MySQLdb.escape_string("@")
authorMap = {}
cursor = db.cursor()
myfile = open("C:/Users/Ritesh/Desktop/LiveJournalDatasets/FlickrDataset/data_stats/authorGroupIDCount.txt","a")
authorGrp = {}

def loadAuthorGroupMapping():
    query = "select * from author_groupids"
    cursor.execute(query)
    ag = cursor.fetchall()
    for a in ag:
        if authorGrp.has_key(a[0]) == False:
            authorGrp[a[0]] = a[1]
        else:
            grp = authorGrp[a[0]]
            grp = grp + a[1]
            authorGrp[a[0]] = grp

def generateGroupDistribution():
    query = "select author_id from authors"
    cursor.execute(query)
    allAuthors = cursor.fetchall()
    #print cursor.rowcount
    ac = 0
    for a in allAuthors:
        authorGroup = {}
        ac+=1
        print ac
        query = "select group_id from author_groupids where author_id = " + "'" + a[0] +"'"
        
        #cursor.execute(query)
        #if cursor.rowcount==0:
            #continue
        #print cursor.rowcount
        #groups = cursor.fetchall()
        #for g in groups:
        if a[0] not in authorGrp:
            continue
        g = authorGrp[a[0]]
        g = g[0:-1]
        grp = g.split(",")
        for gp in grp:
            if authorGroup.has_key(gp) == False:
                authorGroup[gp] = 1
            else:
                cnt = authorGroup[gp]
                cnt+=1
                authorGroup[gp] = cnt
        
        for key in authorGroup:
            myfile.write(a[0]+","+key+","+str(authorGroup[key])+"\n")
            myfile.flush()           

def dumpToDatabase():
    lc = 0
    with open("C:/Users/Ritesh/Desktop/LiveJournalDatasets/FlickrDataset/data_stats/authorGroupIDCount.txt","r") as f:
        for line in f:
            lc+=1
            print lc
            l = line.split(",")
            #query = "Insert into author_group_distribution (author_id, group, count) values (" + "'" + l[0] + "'" + "," + "'" + l[1] + "'" + "," + "'" + l[2][0:-1] + "'" + ")"
            #sql = "INSERT INTO author_group_distribution (author_id, group, count) VALUES ('%s', '%s', '%s')" % ('a', 'a', 'a')
            #cursor.execute(sql)
            cursor.execute("""INSERT INTO author_groupid_distribution VALUES (%s,%s,%s)""",(l[0],l[1],l[2][0:-1]))
            db.commit()
        
loadAuthorGroupMapping()
generateGroupDistribution()                
dumpToDatabase()      
                    
                    
                    
                    
                    
                    
                    
                    
                    
                    
                    
                    