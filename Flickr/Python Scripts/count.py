import os

for filename in os.listdir(os.getcwd()):                 # Gets all the files in the current directory.
    d = {}
    if filename == "comments.cpp":
        continue
    if filename == "chota.txt":
        continue
    if filename == "count.py":
        continue
    if filename == "count.txt":
        continue
    print filename,
    print " ",
    with open(filename) as f:                           # Opens the file, counts the number of comments, adds it with the filename.
        content = f.readlines()                         # Filename is the commento id.
        for i in range(0, len(content)):
            user = ""
            for j in range(0, len(content[i])):
                if(content[i][j] != "\t"):
                    user += (content[i][j])
                else:
                    break
            user.replace(" ","")
            if user in d:
                d[user] += 1
            else:
                d[user] = 1
    print d.items()





