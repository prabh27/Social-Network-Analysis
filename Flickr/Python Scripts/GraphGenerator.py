'''
Created on 25-Mar-2015

@author: Ritesh
'''
tagCount = open("C:/Users/Ritesh/Desktop/LiveJournalDatasets/FlickrDataset/data_stats/tagDistribution.csv","a")
photoCount = open("C:/Users/Ritesh/Desktop/LiveJournalDatasets/FlickrDataset/data_stats/photoDistribution.csv","a")

countPhotosToAuthors = {}
countTagsToAuthors = {}


totalAuthors = 58522

def calculatePhoto():
    with open("C:/Users/Ritesh/Desktop/LiveJournalDatasets/FlickrDataset/data_stats/authorPhotoCount.txt","r") as f:
        for line in f:
            l = line.split(",")
            l[1] = int(l[1].replace("\n",""))
            if countPhotosToAuthors.has_key(l[1])==False:
                countPhotosToAuthors[l[1]] = 1
            else:
                val = countPhotosToAuthors[l[1]]
                val+=1
                countPhotosToAuthors[l[1]] = val
    for key in sorted(countPhotosToAuthors):
        #photoCount.write(str(key)+","+str((countPhotosToAuthors[key]*100)/float(totalAuthors))+"\n")
        photoCount.write(str(key)+","+str(countPhotosToAuthors[key])+"\n")
        photoCount.flush()
        
def calculateTag():
    with open("C:/Users/Ritesh/Desktop/LiveJournalDatasets/FlickrDataset/data_stats/authorAvgTagUsage.txt","r") as f:
        for line in f:
            l = line.split(",")
            l[1] = int(float(l[1].replace("\n","")))
            if countTagsToAuthors.has_key(l[1])==False:
                countTagsToAuthors[l[1]] = 1
            else:
                val = countTagsToAuthors[l[1]]
                val+=1
                countTagsToAuthors[l[1]] = val
    for key in sorted(countTagsToAuthors):
        #tagCount.write(str(key)+","+str((countTagsToAuthors[key]*100)/float(totalAuthors))+"\n")
        tagCount.write(str(key)+","+str(countTagsToAuthors[key])+"\n")
        tagCount.flush()


#calculatePhoto()
#calculateTag()