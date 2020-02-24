# _bundle.py contains private methods for gzip bundling of object
import gzip
import pickle
import os


def __gzip_save(object, filename: str="temp_sclbl_mod.gzip", protocol=0):
    """Saves a compressed object to disk
    """
    fp = gzip.open(filename, 'wb')
    pickle.dump(object, fp)
    fp.close()


def __gzip_load(filename: str="temp_sclbl_mod.gzip"):
    """Loads a compressed object from disk
    """
    fp = gzip.open(filename, 'rb')
    obj = pickle.load(fp)
    fp.close()
    return obj


def __gzip_delete(filename="temp_sclbl_mod.gzip"):
    """delete file from user machine"""
    if os.path.exists(filename):
        os.remove(filename)
        print("deleted gzipped file.")
