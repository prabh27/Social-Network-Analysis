import MySQLdb
import math
import numpy
import scipy
import gensim
import nltk.stem
import time


db = MySQLdb.connect("localhost","root","ritesh","flickr_data",use_unicode=True)

allTags = {}
cursor = db.cursor()
sentences = []
#cursor = []

def timing(f):
    def wrap(*args):
        time1 = time.time()
        ret = f(*args)
        time2 = time.time()
        print '%s function took %0.3f ms' % (f.func_name, (time2-time1)*1000.0)
        return ret
    return wrap


st = nltk.stem.porter.PorterStemmer()
#lancaster = nltk.stem.lancaster.LancasterStemmer()

@timing
def fillStemmedTags():
    query = "select * from author_photos_tags"
    cursor.execute(query)
    res = cursor.fetchall()
    for row in res:
        val = row[2][1:-1]
        l = val.split(",")
        for i in range(len(l)):
            l[i] = st.stem(l[i].strip())
        sentences.append(l)
        if allTags.has_key(row[0])==False:
            allTags[row[0]] = l
        else:
            for tag in l:
                if tag not in allTags[row[0]]:
                    allTags[row[0]].append(tag)
    print "Total Sentences", len(sentences)

def fillTags():
    query = "select * from author_photos_tags"
    cursor.execute(query)
    res = cursor.fetchall()
    for row in res:
        if allTags.has_key(row[0])==False:
            val = row[2][1:-1]
            l = val.split(",")
            for i in range(len(l)):
                l[i] = l[i].strip()
            sentences.append(l)
            allTags[row[0]] = l
        else:
            k = allTags[row[0]]
            val = row[2][1:-1]
            l = val.split(",")
            for i in range(len(l)):
                l[i] = l[i].strip()
            sentences.append(l)
            for i in range(len(l)):
                if l[i].strip() not in k:
                    k.append(l[i].strip())
    print "Total Sentences", len(sentences)

def findJaccardSim():
    myfile = open("C:/Users/Ritesh/Desktop/LiveJournalDatasets/FlickrDataset/data_stats/tagJaccardSim.txt", "w")
    lc = 1
    with open("C:/Users/Ritesh/Desktop/LiveJournalDatasets/FlickrDataset/data_stats/authorEdges.csv", "r") as f:
        for line in f:
            line = line[0:-1]
            print lc
            lc+=1
            l = line.split(" ")
            if allTags.has_key(l[0])==False or allTags.has_key(l[1])==False:
                continue
            
            s1 = set(allTags[l[0]])
            s2 = set(allTags[l[1]])
            
            sim = float(len(s1.intersection(s2)))/len(s1.union(s2))
            myfile.write(l[0]+" "+l[1]+" "+str(sim)+"\n")
            myfile.flush()

def findCosineSimilarity(model):
   ''' print "Cosine"
    model = gensim.models.Word2Vec(sentences, workers=4, min_count=1)
    print "Training Done"
    #now takes model instead
    '''
    myfile = open("C:/Users/Ritesh/Desktop/LiveJournalDatasets/FlickrDataset/data_stats/tagCosine_bigram_stemmed_Phrases.txt", "w")
    lc = 1
    with open("C:/Users/Ritesh/Desktop/LiveJournalDatasets/FlickrDataset/data_stats/authorEdges.csv", "r") as f:
        for line in f:
            line = line[0:-1]
            print lc
            lc+=1
            l = line.split(" ")
            if allTags.has_key(l[0])==False or allTags.has_key(l[1])==False:
                continue
            val = 0.0
            try:
                val = model.n_similarity(allTags[l[0]], allTags[l[1]])
            except:
                pass
            
            myfile.write(l[0]+" "+l[1]+" "+str(val)+"\n")
            myfile.flush()
    

def learnModel(sentences,saveas):
    model = gensim.models.Word2Vec(sentences, workers=4, min_count=1)
    model.save("../Models/"+saveas)
    return model


#fillTags()
'''
#for learning model based on stemmed bigrams

fillStemmedTags()

#bigram_transformer_stemmed = gensim.models.Phrases(sentences)
#bigram_transformer_stemmed.save("/home/prateek/SNA/Social-Network-Analysis/Flickr/Models/bigram_transformed_stemmmed_phrases")

#use saved phrases instead
bigram_transformer_stemmed = gensim.models.Phrases.load("/home/prateek/SNA/Social-Network-Analysis/Flickr/Models/bigram_transformed_stemmmed_phrases")
model=learnModel(bigram_transformer_stemmed[sentences] ,Word2VecForHashtags_StemmedPhrases)
'''

#findJaccardSim()
model = gensim.models.Word2Vec.load("../Models/Word2VecForHashtags_StemmedPhrases")
findCosineSimilarity(model)
