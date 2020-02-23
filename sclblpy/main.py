# File contains all public methods of the scblpy package
from sclblpy import *
import os

# Todo(Mck): Work on upload; first figure our how sklearn stors its models

# def upload(mod, _verbose=True):
#     """ Upload a fitted sklearn model to Scailable
#
#     ...
#
#
#     """
#     1. Inspect the module object
#       - See if its type matches our options
#       - Clean it (strip data)
#
#     2. Use joblib to store the saved file / zip it?
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