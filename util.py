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
        fileNames.sort()
        fileNames.reverse()
        with open(path.join(PICKLE_DIR, fileNames[0]), "r") as pickleFile:
            return pickle.load(pickleFile)
    else:
        return None

def pickleExists(name):
    fileNames = [f for f in os.listdir(PICKLE_DIR) if name in f]
    return not len(fileNames) == 0