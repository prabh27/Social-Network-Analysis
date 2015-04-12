'''
Created on 23-Mar-2015

@author: Ritesh
'''
myfile = open("C:/Users/Ritesh/Desktop/LiveJournalDatasets/FlickrDataset/csvs_and_sql/authorEdges_try2.csv","a")
lc = 0
with open("C:/Users/Ritesh/Desktop/LiveJournalDatasets/FlickrDataset/csvs_and_sql/authorEdges.csv","r") as f:
        for line in f:
            lc+=1
            myfile.write(line)
            myfile.flush()
            if lc==20000:
                break
myfile.close()