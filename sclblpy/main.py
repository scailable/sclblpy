# File contains all public methods of the scblpy package
from sclblpy import *
from sclblpy._utils import __check_model

import numpy as np
import os
import warnings



def upload(mod, row=np.empty(0), _verbose=True):
    """Upload a fitted sklearn model to Scailable

    The upload function is the main workhorse


    """
    try:
        model_ok = __check_model(mod)
    except ModelSupportError as e:
        print("The uploaded model is not (yet) supported")
        print(str(e))
        return False

    # Warn in no row is provided
    row_provided = True
    if not row.any():
        row_provided = False
        warnings.warn("No example row provided. This means we will not be able to test your compute-function.")

    package = {}
    package["fitted_model"] = mod

    if row_provided:
        example = {}
        example["input"] = json.dumps(row.tolist())
        package["example"] = example
        # Prediction from fitted model works:
        # print(package["fitted_model"].predict(row.reshape(1, -1)))

    print(package)
#     2. Use pickle / gzip to store
#       -> https://wiki.python.org/moin/Asking%20for%20Help/How%20do%20I%20use%20gzip%20module%20with%20pickle%3F
#     3. Retrieve / check JWT TOKEN
#     4. POST .zip file using JWT token.
#     5. Make sure an informative message is posted back (demonstrating where and how to use the REST endpoint)


# def endpoints():
#     """List endpoints for current user.
#     """
#
# def delete_endpoint(cfid: str):
#     """Delete an endpoint by cfid
#     """


def remove_credentials(_verbose=True):
    """Remove your stored credentials.

    Remove the .creds.json file that stores the username and password
    of the current user.

    Args:
        _verbose: Boolean indicator whether or not feedback should be printed. Default True.
    """
    global USER_CREDENTIALS_FOLDER
    path: str = USER_CREDENTIALS_FOLDER + ".creds.json"

    if os.path.exists(path):
        os.remove(path)
        if _verbose:
            print("Removed user credentials.")
    else:
        if _verbose:
            print("No user credentials found.")


if __name__ == '__main__':
    print("No command line options available.")