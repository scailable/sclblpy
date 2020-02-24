# File contains all public methods of the scblpy package
import json
import sys
import warnings
import numpy as np

from sclblpy._bundle import __gzip_save, __gzip_delete
from sclblpy._jwt import __check_jwt, __remove_credentials
from sclblpy._utils import __check_model, __get_model_name
from sclblpy._globals import JWT_USER_ID
from sclblpy.errors import ModelSupportError


def upload(mod, row=np.empty(0), docs={}, _verbose=True, _keep=False):
    """Upload a fitted sklearn model to Scailable

    The upload function is the main workhorse


    """
    global JWT_USER_ID

    try:
        model_ok = __check_model(mod)
    except ModelSupportError as e:
        print("The uploaded model is not (yet) supported")
        print(str(e))
        return False

    package = {}
    package["fitted_model"] = mod

    row_provided = True
    if not row.any():
        row_provided = False
        warnings.warn("No example row provided. This means we will not be able to test your compute-function.")

    example = {}
    if row_provided:
        input = json.dumps(row.tolist())
        example["input"] = input
        output = mod.predict(row.reshape(1, -1))
        example["output"] = json.dumps(output.tolist())

    package["example"] = example

    if not docs:
        warnings.warn("No docs provided; using model name as name without further documentation.")

    if docs:
        package["docs"] = docs
    else:
        package["docs"] = __get_model_name(mod)

    try:
        __gzip_save(package)
    except:
        e = sys.exc_info()[0]
        print("Unable to gzip.")
        print(str(e))

    try:
        auth = __check_jwt()
    except:
        e = sys.exc_info()[0]
        print("Unable to authorize.")
        print(str(e))

    if auth:
        print(JWT_USER_ID)
        print("AT THIS POINT WE SHOULD POST THE GZIPPED FILE TO THE TOOLCHAIN\n"
              "(user id is: " + JWT_USER_ID + ")\n"
              "... and perhaps wait for the response by the server...")

    if not _keep:
        __gzip_delete()
    print("(done)")


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
    __remove_credentials()


if __name__ == '__main__':
    print("No command line options available.")
