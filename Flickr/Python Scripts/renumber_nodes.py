'''
Created on 06-Apr-2015

@author: Ritesh
'''

authors = {}
i = 1

with open("C:/Users/Ritesh/Desktop/LiveJournalDatasets/FlickrDataset/csvs_and_sql/authorEdges.csv","r") as f:
        lc = 0
        for line in f:
            lc+=1
            print lc
            line = line[0:-1]
            a = line.split(" ")
            if authors.has_key(a[0])==False:
                authors[a[0]] = i
                i+=1
            if authors.has_key(a[1])==False:
                authors[a[1]] = i
                i+=1
        dl = len(authors)
        num = []
        for i in range(dl+1):
            num.append(0)
        
        myfile = open("C:/Users/Ritesh/Desktop/LiveJournalDatasets/FlickrDataset/csvs_and_sql/authorNumbers.txt","w")
        
        for key in authors:
            num[authors[key]] = key

        
        
        i = 1
        while i<dl+1:
            myfile.write(num[i]+"-"+str(i)+"\n")
            myfile.flush()
            i+=1

with open("C:/Users/Ritesh/Desktop/LiveJournalDatasets/FlickrDataset/csvs_and_sql/authorEdges.csv","r") as f:
    edges = open("C:/Users/Ritesh/Desktop/LiveJournalDatasets/FlickrDataset/csvs_and_sql/authorEdgesRenumbered.txt","w")
    for line in f:
        line = line[0:-1]
        a = line.split(" ")
        edges.write(str(authors[a[0]])+" "+str(authors[a[1]])+"\n")
        edges.flush()
