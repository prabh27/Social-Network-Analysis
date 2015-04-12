'''
Created on 24-Mar-2015

@author: Ritesh
'''

import MySQLdb

db = MySQLdb.connect("localhost","root","ritesh","flickr_data")
cursor = db.cursor()
tagdict = {}
authorPhotoCount = {}
authorTags = {}

countGroups = {}
countGallery = {}
groupCount = open("C:/Users/Ritesh/Desktop/LiveJournalDatasets/FlickrDataset/data_stats/groupDistribution.csv","a")
galleryCount = open("C:/Users/Ritesh/Desktop/LiveJournalDatasets/FlickrDataset/data_stats/galleryDistribution.csv","a")

myfile = open("C:/Users/Ritesh/Desktop/LiveJournalDatasets/FlickrDataset/data_stats/authorAvgTagUsage.txt","a")
photoCount = open("C:/Users/Ritesh/Desktop/LiveJournalDatasets/FlickrDataset/data_stats/authorPhotoCount.txt","a")

def calculateTagFrequency():
    query = "select * from author_photos_tags"
    cursor.execute(query)
    res = cursor.fetchall()
    for r in res:
        l = r[2].split(",")
        for m in l:
            m = m.replace("[","");
            m = m.replace("]","");
            if len(m) <=2:
                continue
            if tagdict.has_key(m)==True:
                val = tagdict.get(m)
                val+=1
                tagdict[m] = val;
            else:
                tagdict[m] = 1;

def dumpToDatabase():
    print len(tagdict)
    for key in tagdict:
        cursor.execute("""INSERT INTO tag_frequency VALUES (%s,%s)""",(key,str(tagdict.get(key))))
        db.commit()

def calculateAvgDescriptionSize():
    totalDescLen = 0
    query = "select description from photo_title_description"
    cursor.execute(query)
    res = cursor.fetchall()
    lc = 0
    for r in res:
        lc+=1
        totalDescLen += len(r[0])
    print totalDescLen, lc, totalDescLen/float(lc)
    
def calculateAvgTitleSize():
    totalTitleLen = 0
    query = "select title from photo_title_description"
    cursor.execute(query)
    res = cursor.fetchall()
    lc = 0
    for r in res:
        lc+=1
        totalTitleLen += len(r[0])
    print totalTitleLen, lc, totalTitleLen/float(lc)
    
def calculationHelperPhotoCount():
    query = "select author_id, photo_id from author_photos_tags"
    cursor.execute(query)
    res = cursor.fetchall()
    for row in res:
        if authorPhotoCount.has_key(row[0]) == True:
            val = authorPhotoCount[row[0]]
            val+=1
            authorPhotoCount[row[0]] = val
        else:
            authorPhotoCount[row[0]] = 1
            
def calculationHelperTagCount():
    query = "select author_id, tags from author_photos_tags"
    cursor.execute(query)
    res = cursor.fetchall()
    for row in res:
        if authorTags.has_key(row[0]) == True:
            val = authorTags[row[0]]
            val+=(len(row[1].split(",")))
            authorTags[row[0]] = val
        else:
            authorTags[row[0]] = len(row[1].split(","))
    
def avgTagsPerPhoto():
    lc = 0
    query = "select * from authors"
    cursor.execute(query)
    res = cursor.fetchall()
    total_tags = 0
    for row in res:
        lc+=1
        print lc
        num_tags = 0
        num_photos = 0
        if authorPhotoCount.has_key(row[0])==True:
            num_photos = authorPhotoCount[row[0]]
        if authorTags.has_key(row[0]) == True:
            num_tags = authorTags[row[0]]
        total_tags+=num_tags
        #photoCount.write(row[0]+","+str(num_photos)+"\n")    
        #photoCount.flush()
        #myfile.write(row[0]+","+str(float(num_tags)/num_photos)+"\n")
        #myfile.flush()
    print total_tags

def calculateGroup():
    query = "SELECT count(*) FROM author_group_distribution group by author_id"
    cursor.execute(query)
    res = cursor.fetchall()
    for row in res:
        if countGroups.has_key(row[0]) == False:
            countGroups[row[0]] = 1
        else:
            val = countGroups[row[0]]
            val+=1
            countGroups[row[0]] = val
    for key in countGroups:
        groupCount.write(str(key)+","+str(int(countGroups.get(key)))+"\n")
        groupCount.flush()
        
def calculateGallery():
    query = "SELECT count(*) FROM author_gallery_distribution group by author_id"
    cursor.execute(query)
    res = cursor.fetchall()
    for row in res:
        if countGallery.has_key(row[0]) == False:
            countGallery[row[0]] = 1
        else:
            val = countGallery[row[0]]
            val+=1
            countGallery[row[0]] = val
    for key in countGallery:
        galleryCount.write(str(key)+","+str(int(countGallery.get(key)))+"\n")
        galleryCount.flush()
        
calculateGallery()
#calculateTagFrequency()
#dumpToDatabase()
#calculateAvgDescriptionSize()
#calculateAvgTitleSize()

#calculationHelperPhotoCount()
#calculationHelperTagCount()
#avgTagsPerPhoto()