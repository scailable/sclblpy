# _bundle.py contains private methods for gzip bundling of object
import gzip
import pickle
import os

from sclblpy.errors import ModelBundleError
import sclblpy._globals as glob


def _gzip_save(object, filename: str=glob.BUNDLE_NAME, _verbose=False):
    """Saves a compressed object to disk.

    Function is used to pickle and gzip an sclblpy model object as created
    by the upload() function. This package is send to the toolchain.

    Args:
        object: A dictionary containing all the information to be send.
        filename: a string stating where to store the .zip file. Default glob.BUNDLE_NAME
        _verbose: Bool indicating whether feedback should be printed. Default False.

    Returns:

    Raises:
          ModelBundleError if unable to store the model bundle.

    """
    try:
        fp = gzip.open(filename, 'wb')
        pickle.dump(object, fp, protocol=4)  # protocol = 4 is python 3.4 or higher
        fp.close()
        if _verbose:
            print("File successfully stored.")
    except Exception as e:
        if _verbose:
            print("Exception: " + str(e))
        raise ModelBundleError("Unable to pickle and gzip your model.")

    return


def _gzip_load(filename: str=glob.BUNDLE_NAME, _verbose=True):
    """Loads a compressed object from disk.

    Currently not used in the sclblpy package but syntax should be used on the toolchain side.

    Args:
        filename: Name of the gzipped pickle. Default "temp_sclbl_mod.gzip".
        _verbose: Bool indicating whether feedback should be printed. Default True.
    Returns:
        obj: A dictonary containing the unpickled and unzipped contents of the file. Empty dict if unable to open.

    Raises:
        ModelBundleError if fails.

    """
    obj = {}
    try:
        if os.path.exists(filename):
            fp = gzip.open(filename, 'rb')
            obj = pickle.load(fp)
            fp.close()
            if _verbose:
                print("Model bundle successfully loaded.")
        else:
            if _verbose:
                print("Model bundle not found.")
    except Exception as e:
        if _verbose:
            print("Exception: " + str(e))
        raise ModelBundleError("Unable to load model bundle.")

    return obj


def _gzip_delete(filename:str =glob.BUNDLE_NAME, _verbose=False):
    """Deletes a file from user machine.

    Args:
        filename: Str name of the file to delete, default: temp_sclbl_mod.gzip.
        _verbose: Bool indicating whether feedback should be printed. Default False.

    Returns:

    Raises:
        ModelBundleError if fails.

    """

    try:
        if os.path.exists(filename):
            os.remove(filename)
            if _verbose:
                print("Deleted gzipped model bundle.")
        else:
            if _verbose:
                print("File not found.")
    except Exception as e:
        print("Exception: " + str(e))
        raise ModelBundleError("Unable to delete file.")

    return


if __name__ == '__main__':
    print("No command line options yet for _bundle.py.")