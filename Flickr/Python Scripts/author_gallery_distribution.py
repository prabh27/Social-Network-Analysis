'''
Created on 20-Mar-2015

@author: Ritesh
'''
'''
Created on 20-Mar-2015

@author: Ritesh
'''

import MySQLdb

db = MySQLdb.connect("localhost","root","ritesh","flickr_data")
MySQLdb.escape_string("@")
authorMap = {}
cursor = db.cursor()
myfile = open("C:/Users/Ritesh/Desktop/LiveJournalDatasets/FlickrDataset/authorGalleryCount.txt","a")
authorGal = {}

def loadAuthorGalleryMapping():
    query = "select * from author_galleries"
    cursor.execute(query)
    ag = cursor.fetchall()
    for a in ag:
        if authorGal.has_key(a[0]) == False:
            authorGal[a[0]] = a[1]
        else:
            gal = authorGal[a[0]]
            gal = gal + a[1]
            authorGal[a[0]] = gal

def generateGalleryDistribution():
    query = "select author_id from authors"
    cursor.execute(query)
    allAuthors = cursor.fetchall()
    #print cursor.rowcount
    ac = 0
    for a in allAuthors:
        authorGallery = {}
        ac+=1
        print ac
        query = "select groups from author_groups_new where author_id = " + "'" + a[0] +"'"
        
        #cursor.execute(query)
        #if cursor.rowcount==0:
            #continue
        #print cursor.rowcount
        #groups = cursor.fetchall()
        #for g in groups:
        if a[0] not in authorGal:
            continue
        g = authorGal[a[0]]
        grp = g.split(",")
        for gp in grp:
            if authorGallery.has_key(gp) == False:
                authorGallery[gp] = 1
            else:
                cnt = authorGallery[gp]
                cnt+=1
                authorGallery[gp] = cnt
        
        for key in authorGallery:
            myfile.write(a[0]+","+key+","+str(authorGallery[key])+"\n")
            myfile.flush()           

def dumpToDatabase():
    lc = 0
    with open("C:/Users/Ritesh/Desktop/LiveJournalDatasets/FlickrDataset/authorGalleryCount.txt","r") as f:
        for line in f:
            lc+=1
            print lc
            l = line.split(",")
            #query = "Insert into author_group_distribution (author_id, group, count) values (" + "'" + l[0] + "'" + "," + "'" + l[1] + "'" + "," + "'" + l[2][0:-1] + "'" + ")"
            #sql = "INSERT INTO author_group_distribution (author_id, group, count) VALUES ('%s', '%s', '%s')" % ('a', 'a', 'a')
            #cursor.execute(sql)
            cursor.execute("""INSERT INTO author_gallery_distribution VALUES (%s,%s,%s)""",(l[0],l[1],l[2][0:-1]))
            db.commit()
        
#loadAuthorGalleryMapping()
#generateGalleryDistribution()                
dumpToDatabase()      
                    
                    
                    
                    
                    
                    
                    
                    
                    
                    
                    
                    