'''
Created on 12-Apr-2015

@author: Ritesh
'''

pair = {}

def readFiles():
    with open("C:/Users/Ritesh/Desktop/LiveJournalDatasets/FlickrDataset/data_stats/groupContributionKLD.txt","r") as f:
        lc = 1
        for line in f:
            print lc
            lc+=1
            line = line[0:-1]
            l = line.split(" ")
            if pair.has_key(l[0]+" "+l[1])==False:
                pair[l[0]+" "+l[1]] = float(l[2])
            
    with open("C:/Users/Ritesh/Desktop/LiveJournalDatasets/FlickrDataset/data_stats/groupPopularityKLD.txt","r") as f:
        lc = 1
        for line in f:
            print lc
            lc+=1
            line = line[0:-1]
            l = line.split(" ")
            if pair.has_key(l[0]+" "+l[1])==False:
                pair[l[0]+" "+l[1]] = float(l[2])
            else:
                val = pair[l[0]+" "+l[1]]
                val+=float(l[2])
                pair[l[0]+" "+l[1]] = val
    
    with open("C:/Users/Ritesh/Desktop/LiveJournalDatasets/FlickrDataset/data_stats/galleryContributionKLD.txt","r") as f:
        lc = 1
        for line in f:
            print lc
            lc+=1
            line = line[0:-1]
            l = line.split(" ")
            if pair.has_key(l[0]+" "+l[1])==False:
                pair[l[0]+" "+l[1]] = float(l[2])
            else:
                val = pair[l[0]+" "+l[1]]
                val+=float(l[2])
                pair[l[0]+" "+l[1]] = val
    
    with open("C:/Users/Ritesh/Desktop/LiveJournalDatasets/FlickrDataset/data_stats/galleryPopularityKLD.txt","r") as f:
        lc = 1
        for line in f:
            print lc
            lc+=1
            line = line[0:-1]
            l = line.split(" ")
            if pair.has_key(l[0]+" "+l[1])==False:
                pair[l[0]+" "+l[1]] = float(l[2])
            else:
                val = pair[l[0]+" "+l[1]]
                val+=float(l[2])
                pair[l[0]+" "+l[1]] = val
    
    with open("C:/Users/Ritesh/Desktop/LiveJournalDatasets/FlickrDataset/data_stats/tagCosine.txt","r") as f:
        lc = 1
        for line in f:
            print lc
            lc+=1
            line = line[0:-1]
            l = line.split(" ")
            if pair.has_key(l[0]+" "+l[1])==False:
                pair[l[0]+" "+l[1]] = float(l[2])
            else:
                val = pair[l[0]+" "+l[1]]
                val+=float(l[2])
                pair[l[0]+" "+l[1]] = val
    
def createEdgeWeightFile():
    myfile = open("C:/Users/Ritesh/Desktop/LiveJournalDatasets/FlickrDataset/data_stats/tagGraphWithWeightsSumFinal.txt","w")
    lc = 1
    for key in pair:
        print lc
        lc+=1
        myfile.write(key+" "+str(pair[key])+"\n")
        myfile.flush()
    
readFiles()
createEdgeWeightFile()

numbers = {}

def convertToNums():
    myfile = open("C:/Users/Ritesh/Desktop/LiveJournalDatasets/FlickrDataset/data_stats/tagGraphWithWeightsSumRenumberedFinal.txt","w")
    with open("C:/Users/Ritesh/Desktop/LiveJournalDatasets/FlickrDataset/data_stats/tagGraphWithWeightsSumFinal.txt","r") as f:
        lc = 1
        count = 1
        for line in f:
            print lc
            lc+=1
            line = line[0:-1]
            l = line.split(" ")
            if numbers.has_key(l[0])==False:
                numbers[l[0]] = count
                count+=1
            if numbers.has_key(l[1])==False:
                numbers[l[1]] = count
                count+=1
            myfile.write(str(numbers[l[0]]) + " " + str(numbers[l[1]]) + " " + str(l[2]) + "\n")
            myfile.flush()

convertToNums()