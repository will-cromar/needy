import time
import os
from os import path
import pickle

PICKLE_DIR = "pickles/"

def savePickle(object, name):
    epoch = time.time()
    filename = name + str(epoch) + ".pkl"
    fullPath = path.join(PICKLE_DIR, filename)
    with open(fullPath, "w") as outfile:
        pickle.dump(object, outfile)

def getMostRecentPickle(name):
    fileNames = [f for f in os.listdir(PICKLE_DIR) if name in f]
    if len(fileNames) != 0:
        sorted(fileNames).reverse()
        with open(path.join(PICKLE_DIR, fileNames[0]), "r") as pickleFile:
            return pickle.load(pickleFile)
    else:
        return None

#Testing code. Run this once to make sure it works
obj1 = "Less recent"
obj2 = "More recent"

savePickle(obj1, "stringtest")
time.sleep(20)
savePickle(obj2, "stringtest")

print getMostRecentPickle("stringtest")