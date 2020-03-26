# File contains all public methods of the scblpy package
import json
import numpy as np
import requests

import sclblpy._globals as glob
from sclblpy._bundle import _gzip_save, _gzip_delete
from sclblpy._jwt import _check_jwt, _remove_credentials
from sclblpy._utils import _get_model_name, _get_system_info, _predict, _get_model_package, _load_supported_models
from sclblpy.errors import UserManagerError, JWTError


def upload(mod, docs=None, feature_vector=np.empty(0), _verbose=False, _keep=False):
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

    Args:
        mod: The model to be uploaded.
        docs: A dict{} containing the fields 'name' and 'documentation'
        feature_vector: A np.array, usually the first fow of a training dataset obtained using row = X[0,:]
        _verbose: Bool indicating whether elaborate user feedback should be printed. Default False.
        _keep: Bool indicating whether the .gzipped file should be retained. Default False.

    Returns:
        False if upload failed, true otherwise

    Raises:
    """
    bundle = {}
    bundle['fitted_model'] = mod

    bundle['example'] = {}
    if feature_vector.any():
        inputStr = '[[%s]]' % ', '.join([str(i) for i in feature_vector.tolist()])
        example = {'input': inputStr}
        try:
            output = _predict(mod, feature_vector)
            example["output"] = json.dumps(output)
        except Exception as e:
            if not glob.SILENT:
                print("WARNING: we were unable to create an example inference.")
            if _verbose:
                print("Unable to predict: " + str(e))
        bundle['example'] = example
    else:
        if not glob.SILENT:
            print("WARNING: You did not provide an example instance. (see docs). \n"
                  "Providing an example allows us automatically generate and test your feature vector.")

    bundle['docs'] = {}
    if docs:
        bundle['docs'] = docs
    else:
        bundle['docs']['name'] = _get_model_name(mod)
        bundle['docs']['documentation'] = "None."
        if not glob.SILENT:
            print("WARNING: You did not provide any documentation. We will simply use \n"
                  "the name of your model as its title.")

    bundle['system_info'] = _get_system_info()

    try:
        _gzip_save(bundle)
    except Exception as e:
        if not glob.SILENT:
            print("FATAL: Unable to gzip your model bundle. Your model has not been uploaded.")
        if _verbose:
            print(str(e))
        return False

    try:
        auth = _check_jwt()
    except Exception as e:
        if not glob.SILENT:
            print("FATAL: Unable to obtain JWT authorization for your account. Your model has not been uploaded.")
        if _verbose:
            print(str(e))
        return False

    if auth:

        url = glob.TOOLCHAIN_URL + "/upload/" + glob.JWT_USER_ID

        # Map python package to the right toolchain:
        pkg_name = _get_model_package(mod)
        toolchain_name = ""
        if pkg_name == "sklearn":
            toolchain_name = "sklearn"
        elif pkg_name == "statsmodels":
            toolchain_name = "sklearn"
        elif pkg_name == "xgboost":
            toolchain_name = "sklearn"

        # Setup the actual request
        data: dict = {
            # email : bool.
            'package': glob.PKG_NAME,
            'toolchain': toolchain_name,
            'name': bundle['docs'].get('name', "No name found."),
            'docs': bundle['docs'].get('documentation', "No docs provided."),
            'exampleinput': bundle['example'].get('input', "[]"),
            'exampleoutput': bundle['example'].get('output', "[]")
        }
        payload: dict = {
            'data': json.dumps(data)
        }

        files = [('bundle', open(glob.BUNDLE_NAME, 'rb'))]
        headers = {
            'Authorization': glob.JWT_TOKEN
        }

        # Do the request
        try:
            response = requests.post(url, headers=headers, data=payload, files=files)
        except Exception as e:
            if not glob.SILENT:
                print("FATAL: Unable to carry out the upload request. Your model has not been uploaded.")
            if _verbose:
                print(str(e))
            return False

        # Error handling
        try:
            response_data = json.loads(response.text)
        except Exception as e:
            if not glob.SILENT:
                print("FATAL: No valid JSON response received. Your model has not been uploaded.")
            if _verbose:
                print(str(e))
            return False

        if response_data['error']:
            if not glob.SILENT:
                print("FATAL: Error returned from server. Your model has not been uploaded.")
            if _verbose:
                print(str(response_data['error']))
            return False

        if _verbose:
            print("The following content has been send to the toolchain server:")
            print(bundle)

    if not _keep:
        _gzip_delete()

    return True


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
        _check_jwt()
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
        if _verbose:
            print(str(e))
        raise UserManagerError("Unable to retrieve endpoints. " + str(e))

    # Todo (McK): Print nicer message if 0.
    if not glob.SILENT:
        print("You currently own the following endpoints:")
        for key in result:
            print('Name: {}, cfid: {}.'.format(key['name'], key['cfid']))

    return result


def delete_endpoint(cfid: str, _verbose=False):
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
        _check_jwt()
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
        if _verbose:
            print(str(e))
        raise UserManagerError("Unable to delete endpoint. " + str(e))

    if not glob.SILENT:
        print(result['message'])

    return True


def remove_credentials(_verbose=True):
    """Remove your stored credentials.

    Remove the .creds.json file that stores the username and password
    of the current user.

    Args:
        _verbose: Boolean indicator whether or not feedback should be printed. Default False.
    """
    # If silent, be silent:
    if glob.SILENT:
        _verbose =  False

    # actual function in _utils.py to prevent circular includes.
    _remove_credentials(_verbose)


def stop_print():
    """Stop ALL printing from package"""
    glob.SILENT = True


def start_print():
    """(re)start printing user feedback"""
    print("Printing user feedback set to 'True'.")
    glob.SILENT = False


def list_models():
    """Print or return a list of all supported models.

    Returns:
        A dictionary detailing the supported models
    """
    if not glob.SUPPORTED_MODELS:
        _load_supported_models()

    if not glob.SILENT:
        print("Currently supported models:")
        print(json.dumps(glob.SUPPORTED_MODELS, sort_keys=True, indent=4))

    return glob.SUPPORTED_MODELS


def _set_toolchain_URL(url: str):
    """Change the location of the toolchain server

    Args:
        url: String specifying the location of the toolchain server
    """
    glob.TOOLCHAIN_URL = url

    if not glob.SILENT:
        print("Toolchain url changed to: " + glob.TOOLCHAIN_URL)


def _set_admin_URL(url: str):
    """Change the location of the toolchain server

    Args:
        url: String specifying the location of the toolchain server
    """
    glob.USER_MANAGER_URL = url

    if not glob.SILENT:
        print("User-manager (admin) url changed to: " + glob.USER_MANAGER_URL)


if __name__ == '__main__':
    print("No command line options available for main.py.")
