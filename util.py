import time
import os
from os import path
import pickle

# Relative path of pickle cache from working directory
PICKLE_DIR = "pickles/"

def savePickle(object, name):
    """
    Caches object as [name][epoch time].pkl
    :param object: Object to cache
    :param name: name in cache
    :return: None
    """
    epoch = time.time()
    filename = name + str(epoch) + ".pkl"       # Save name
    fullPath = path.join(PICKLE_DIR, filename)  # Save path

    # Get permissions and save the file
    with open(fullPath, "w") as outfile:
        pickle.dump(object, outfile)

def getMostRecentPickle(name):
    """
    Finds the most recent pickle in the cache with the given name
    :param name: Savename of pickle (without epoch time)
    :return: Object in cache on success, None on miss
    """
    # List the directory
    fileNames = [f for f in os.listdir(PICKLE_DIR) if name in f]

    # If the directory is not empty...
    if len(fileNames) != 0:
        # Sort in descending order by epoch time
        fileNames.sort()
        fileNames.reverse()

        # Open, load, and return pickle
        with open(path.join(PICKLE_DIR, fileNames[0]), "r") as pickleFile:
            return pickle.load(pickleFile)
    # Return None on cache miss
    else:
        return None

def pickleExists(name):
    """
    Returns True if there is a pickle with name in cache, False otherwise. Used to prevent
    cache misses
    :param name: Name to look for in cache
    :return: True on hit, False on miss
    """
    fileNames = [f for f in os.listdir(PICKLE_DIR) if name in f]
    return not len(fileNames) == 0