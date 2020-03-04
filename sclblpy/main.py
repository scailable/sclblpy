# File contains all public methods of the scblpy package
import json
import sys
import warnings
import numpy as np
import requests

import sclblpy._globals as glob
from sclblpy._bundle import _gzip_save, _gzip_delete
from sclblpy._jwt import _check_jwt, _remove_credentials
from sclblpy._utils import _check_model, _get_model_name, _get_system_info, _predict
from sclblpy.errors import ModelSupportError, UserManagerError, JWTError


def upload(mod, docs={}, feature_vector=np.empty(0), _verbose=False, _keep=False):
    """Uploads a fitted sklearn model to Scailable.

    The upload function is the main workhorse of the sclblpy package.
    The function first checks whether the supplied model is ok (part of the list and fitted).

    Next, it checks whether an example row is provided and if so it creates the example
    input and output .json objects. If not, it prints a warning (note, using 'print()' rather
    than warnings.warn as this ensures that the order is maintained).

    Next, the docs are checked; if none are provided a warning is issued and a simple
    name is provided based on the model type.

    Subsequently, we package the whole thing, including details of the user system, into a
    gzipped file that is stored on disc.

    Finally the whole package is uploaded to the toolchain.

    Todo(Mck): Finalize the final upload.

    Args:
        mod: The model to be uploaded.
        docs: A dict{} containing the fields 'name' and 'documentation'
        feature_vector: A np.array, usually the first fow of a training dataset obtained using row = X[0,:]
        _verbose: Bool indicating whether elaborate user feedback should be printed. Default False.
        _keep: Bool indicating whether the .gzipped file should be retained. Default False.

    Returns:

    Raises:
    """
    bundle = {}

    try:
        model_ok = _check_model(mod)
    except ModelSupportError as e:
        print("FATAL: The model you are trying to upload is not (yet) supported. \n"
              "Please see README.md for a list of supported models.")
        if _verbose:
            print(str(e))
        return
    bundle['fitted_model'] = mod

    if feature_vector.any():  # this does not fail gracefully...
        example = {}
        example['input'] = feature_vector.tolist()
        try:
            output = _predict(mod, feature_vector)
            example["output"] = json.dumps(output)
        except Exception as e:
            print("WARNING: we were unable to create an example inference.")
            if _verbose:
                print("Unable to predict: " + str(e))
        bundle['example'] = example
    else:
        print("WARNING: You did not provide an example instance. (see docs). \n"
              "Providing en example allows us automatically generate and test your feature vector.")

    bundle['docs'] = {}
    if docs:
        bundle['docs'] = docs
    else:
        bundle['docs']['name'] = _get_model_name(mod)
        print("WARNING: You did not provide any documentation. We will simply use \n"
              "the name of your model as its title.")

    bundle['system_info'] = _get_system_info()

    try:
        _gzip_save(bundle)
    except Exception as e:
        print("FATAL: Unable to gzip your model bundle. Model not uploaded.")
        if _verbose:
            print(str(e))
        return False

    try:
        auth = _check_jwt()
    except Exception as e:
        print("FATAL: Unable to obtain JWT authorization for your account. Model not uploaded.")
        if _verbose:
            print(str(e))

    if auth:

        url = glob.TOOLCHAIN_URL + "/upload/" + glob.JWT_USER_ID

        # Todo: Make this dynamic
        payload = {'data': '{"package":"sclblpy","toolchain":"sklearn"}'}
        files = [('bundle', open('/Users/mauritskate/Desktop/bundle.gzip', 'rb'))]
        headers = {
             'Content-Type': 'application/x-www-form-urlencoded',
             'Authorization': glob.JWT_USER_ID
        }

        # Todo: add try except here:
        response = requests.request("POST", url, headers=headers, data=payload, files=files)

        # Todo: add the right feedback:
        print(response)

    if _verbose:
        print("The following content is send to the toolchain server:")
        print(bundle)

    if not _keep:
        _gzip_delete()


def endpoints(_verbose=True):
    """Lists the endpoints for current user.

    Using the global JWT string this function returns a dict
    of the endpoints by the current user.

    Args:
        _verbose: Bool indicating whether the endpoints should be printed. Default True.

    Returns:
         endpoints: a list containing all the endpoints by the current user. [{},{},{}]

    Raises:
        JWTError if unable to obtain JWT authorization
        UserManagerError if unable to retrieve endpoint details

    """
    try:
        auth = _check_jwt()
    except Exception as e:
        if _verbose:
            print(str(e))
        raise JWTError("Unable to check JWT authorization. " + str(e))

    url = glob.USER_MANAGER_URL + "/compute-functions/" + glob.JWT_USER_ID
    headers = {
        'Authorization': glob.JWT_TOKEN
    }

    try:
        response = requests.request("GET", url, headers=headers, data={})
        result = json.loads(response.text)
    except Exception as e:
        raise UserManagerError("Unable to retrieve endpoints. " + str(e))

    if _verbose:
        print("You currently own the following endpoints:")
        for key in result:
            print('Name: {}, cfid: {}.'.format(key['name'], key['cfid']))
    return result


def delete_endpoint(cfid: str, _verbose=True):
    """Deletes an endpoint by cfid.

    Delete an endpoint owned by the currently logged in user by cfid.

    Args:
        cfid: String of the compute function id.
        _verbose: Bool indicating whether feedback should be printed. Default True.

    Returns:
        True if successful

    Raises:
        JWTError if unable to obtain JWT authorization
        UserManagerError if unable to delete endpoints
    """
    try:
        auth = _check_jwt()
    except Exception as e:
        if _verbose:
            print(str(e))
        raise JWTError("Unable to check JWT authorization. " + str(e))

    url = glob.USER_MANAGER_URL + "/compute-function/" + glob.JWT_USER_ID + "/" + cfid
    headers = {
        'Authorization': glob.JWT_TOKEN
    }
    try:
        response = requests.request("DELETE", url, headers=headers, data={})
        result = json.loads(response.text)
    except Exception as e:
        raise UserManagerError("Unable to delete endpoint. " + str(e))

    if _verbose:
        print(result['message'])
    return


def remove_credentials(_verbose=False):
    """Remove your stored credentials.

    Remove the .creds.json file that stores the username and password
    of the current user.

    Args:
        _verbose: Boolean indicator whether or not feedback should be printed. Default False.
    """
    # actual function in _utils.py to prevent circular includes.
    _remove_credentials(_verbose)


if __name__ == '__main__':
    print("No command line options available.")
