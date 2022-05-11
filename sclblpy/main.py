# File contains all public methods of the scblpy package
import json
import urllib
import requests
import sclblpy._globals as glob
from sclblpy._bundle import _gzip_save, _gzip_delete
from sclblpy._jwt import _check_jwt, _remove_credentials
from sclblpy._utils import  _get_system_info
from sclblpy.errors import UserManagerError, JWTError, UploadModelError, RunTaskError, CreateAssignmentError
from sclblpy.version import __version__


# welcome just prints a simple welcome message:
def welcome():
    """ Welcome simply prints a welcome message.
    """
    print("\n*** Thanks for importing sclblpy! ***")
    print("You can use the 'upload()' function to upload your models.")
    print("To inspect your currently uploaded models, use `endpoints()`.")
    print("Check the docs at https://pypi.org/project/sclblpy/ for more info. \n")




# upload_onnx uploads an onnx file to the toolchain-server
def upload_onnx(path, example="", docs={}, email=True) -> bool:
    """upload_onnx uploads a fitted onnx model to Scailable.

    - The function first checks if the supplied path indeed references a .onnx file
    - Next, the docs are checked; if none are provided a warning is issued and a simple
    name is provided based on the model type.
    - Finally the onnx file and the supporting docs are uploaded to the toolchain.

    Note: This method prints user-feedback by default. This feedback can be suppressed by calling the
        stop_print() method.

    Args:
        path: The path referencing the onnx model location (i.e., the .onnx file location).
        example: String example input for the onnx file.
        docs: A dict{} containing the fields 'name' and 'documentation'.
        email: Bool indicating whether a confirmation email of a successful conversion should be send. Default True.

    Returns:
        False if upload failed, true otherwise

    Raises  (in debug mode):
        UploadModelError if unable to successfully bundle and upload the model.
    """
    if glob.DEBUG:
        print("We are checking your .onnx file...")

    bundle = {}

    # simply add example string to bundle:
    bundle['example'] = example

    # check the docs:
    bundle['docs'] = {}
    if docs:
        bundle['docs'] = docs
    else:
        try:  # This should work, but catching the exception just in case:
            name = path
        except Exception:
            name = "NAMELESS MODEL"
        bundle['docs']['name'] = name
        bundle['docs']['documentation'] = "-- EMPTY --"
        if not glob.SILENT:
            print("WARNING: You did not provide any documentation. \n"
                  "We will simply use " + name + " as its name without further documentation.")

    # check if file exists:
    if not path.endswith('.onnx'):
        if not glob.SILENT:
            print("FATAL: You did not specify a .onnx path. \n")
        if glob.DEBUG:
            raise UploadModelError("We were unable to open the specified onnx file (no .onnx extension).")

    # try to open the file
    try:
        files = [('bundle', open(path, 'rb'))]
    except Exception:
        if not glob.SILENT:
            print("FATAL: We were unable to open the specified onnx file. Is the path correct? \n")
        if glob.DEBUG:
            raise UploadModelError("We were unable to open the specified onnx file.")
        return False

    # check authorization:
    auth = _check_jwt()
    if not auth:
        if not glob.SILENT:
            print("FATAL: We were unable to obtain JWT authorization for your account. \n"
                  "Your model has not been uploaded. \n")
        if glob.DEBUG:
            raise UploadModelError("We were unable to obtain JWT authorization.")
        return False

    # get system information
    bundle['system_info'] = _get_system_info()

    # all ok, upload:
    if auth:

        url = glob.TOOLCHAIN_URL + "/upload/" + glob.JWT_USER_ID

        # Hard coded tootlchain name:
        toolchain_name = "onnx2c"

        # Setup the actual request
        data: dict = {
            'email': email,
            'package': __version__,
            'toolchain': toolchain_name,
            'name': bundle['docs'].get('name', "No name found."),
            'docs': bundle['docs'].get('documentation', "No docs provided."),
            'exampleInput': example,
            'exampleOutput': ""
        }
        payload: dict = {
            'data': json.dumps(data)
        }

        headers = {
            'Authorization': glob.JWT_TOKEN,
        }

        # Do the request
        try:
            response = requests.post(url, headers=headers, data=payload, files=files)
        except Exception as e:
            if not glob.SILENT:
                print("FATAL: Unable to carry out the upload request: the toolchain is not available. \n"
                      "Your model has not been uploaded. PLACE 1 URL: {url}\n")
            if glob.DEBUG:
                raise UploadModelError("We were unable to obtain JWT authorization: " + str(e))
            return False

        # Error handling
        try:
            response_data = json.loads(response.text)
        except Exception as e:
            if not glob.SILENT:
                print("FATAL: We did not receive a valid JSON response from the toolchain-server. \n"
                      "Your model has not been uploaded. \n")
            if glob.DEBUG:
                raise UploadModelError("We did not receive a valid response from the server: " + str(e))
            return False

        if response_data['error']:
            if not glob.SILENT:
                print("FATAL: An error was returned by the toolchain-server. \n"
                      "Your model has not been uploaded. \n")
            if glob.DEBUG:
                raise UploadModelError("We did not receive a valid response from the server: " + response_data['error'])
            return False

        if glob.DEBUG:
            print("The following content has been send to the toolchain server:")
            print(bundle)

        # user feedback:
        if not glob.SILENT:
            print("Your ONNX file was successfully uploaded to Scailable!")
            print("NOTE: After transpiling, we will send you an email and your model will be available at "
                  "https://admin.sclbl.net.")
            print("Or, alternatively, you can use the 'models()' function to list all your uploaded models. \n")

        return True

    else:
        return False






# update_onnx updates an onnx model
def update_onnx(path, cfid, example="", docs={}, email=True) -> bool:
    """upload_onnx updates a fitted onnx model to Scailable.

    The update function is similar to the upload function in most respects (so, see its docs),
    but instead of creating a new endpoint it overwrites the docs and model of an already existing
    endpoint. Thus, there is an additional argument "cfid" providing the computeFunction Id
    of the endpoint that needs to be updated. Use sp.list_models() to get a list of your already
    existing endpoints.

    Note: If you solely want to change the documentation of an endpoint, you can either use the
        update_docs() function or the online admin interface at https://admin.sclble.net.

    Args:
        path: The path referencing the onnx model location (i.e., the .onnx file location).
        cfid: a string with a valid computeFunction ID.
        example: String example input for the onnx file.
        docs: A dict{} containing the fields 'name' and 'documentation'.
        email: Bool indicating whether a confirmation email of a successful conversion should be send. Default True.

    Returns:
        False if upload failed, true otherwise

    Raises  (in debug mode):
        UploadModelError if unable to successfully bundle and upload the model.
    """
    if glob.DEBUG:
        print("We are checking your updated .onnx file...")

    bundle = {}

    # simply add example string to bundle:
    bundle['example'] = example

    # check the docs:
    bundle['docs'] = {}
    if docs:
        bundle['docs'] = docs
    else:
        try:  # This should work, but catching the exception just in case:
            name = path
        except Exception:
            name = "NAMELESS MODEL"
        bundle['docs']['name'] = name
        bundle['docs']['documentation'] = "-- EMPTY --"
        if not glob.SILENT:
            print("WARNING: You did not provide any documentation. \n"
                  "We will simply use " + name + " as its name without further documentation.")

    # check if file exists:
    if not path.endswith('.onnx'):
        if not glob.SILENT:
            print("FATAL: You did not specify a .onnx path. \n"
                  "Your model has not been updated. \n")
        if glob.DEBUG:
            raise UploadModelError("We were unable to open the specified onnx file (no .onnx extension).")

    # try to open the file
    try:
        files = [('bundle', open(path, 'rb'))]
    except Exception:
        if not glob.SILENT:
            print("FATAL: We were unable to open the specified onnx file. Is the path correct? \n"
                  "Your model has not been updated. \n")
        if glob.DEBUG:
            raise UploadModelError("We were unable to open the specified onnx file.")
        return False

    # check authorization:
    auth = _check_jwt()
    if not auth:
        if not glob.SILENT:
            print("FATAL: We were unable to obtain JWT authorization for your account. \n"
                  "Your model has not been updated. \n")
        if glob.DEBUG:
            raise UploadModelError("We were unable to obtain JWT authorization.")
        return False

    # get system information
    bundle['system_info'] = _get_system_info()

    # all ok, upload:
    if auth:

        url = glob.TOOLCHAIN_URL + "/upload/" + glob.JWT_USER_ID + "/" + cfid

        # Hard coded tootlchain name:
        toolchain_name = "onnx2c"

        # Setup the actual request
        data: dict = {
            'email': email,
            'package': __version__,
            'toolchain': toolchain_name,
            'name': bundle['docs'].get('name', "No name found."),
            'docs': bundle['docs'].get('documentation', "No docs provided."),
            'exampleInput': example,
            'exampleOutput': ""
        }
        payload: dict = {
            'data': json.dumps(data)
        }

        headers = {
            'Authorization': glob.JWT_TOKEN,
        }

        try:
            response = requests.put(url, headers=headers, data=payload, files=files)
        except Exception as e:
            if not glob.SILENT:
                print(f"FATAL: Unable to carry out the update request: the toolchain is not available. \n"
                      f"Your model has not been updated. {url}, user id: {glob.JWT_USER_ID}, cfid:  {cfid}\n")
            if glob.DEBUG:
                raise UploadModelError("We were unable to obtain JWT authorization: " + str(e))
            return False

        # Error handling
        try:
            response_data = json.loads(response.text)
        except Exception as e:
            if not glob.SILENT:
                print("FATAL: We did not receive a valid JSON response from the toolchain-server. \n"
                      "Your model has not been updated. \n")
            if glob.DEBUG:
                raise UploadModelError("We did not receive a valid response from the server: " + str(e))
            return False

        if response_data['error']:
            if not glob.SILENT:
                print("FATAL: An error was returned by the toolchain-server. \n"
                      "Your model has not been updated. \n")
            if glob.DEBUG:
                raise UploadModelError("We did not receive a valid response from the server: " + response_data['error'])
            return False

        if glob.DEBUG:
            print("The following content has been send to the toolchain server:")
            print(bundle)

        # user feedback:
        if not glob.SILENT:
            print("Your model was successfully submitted for an update. \n")

        return True

    else:
        return False


# update_docs updates the docs of a given model (but not the model itself:
def update_docs(cfid, docs) -> bool:
    """Updates the documentation of an already existing model

    The update_docs function can be used to upload the documentation of an already existing model
    by simply providing the cfid and the new docs object.

    Args:
        cfid: a string with a valid computeFunction ID.
        docs: A dict{} containing the fields 'name' and 'documentation'

    Returns:
        False if upload failed, true otherwise

    Raises  (in debug mode):
        UploadModelError if unable to successfully bundle and upload the model.
    """

    # check the docs:
    print(docs)
    name = docs.get('name', "")
    if name == "":
        print("FATAL: Please make sure to add a name to your documentation (using the 'name') field \n"
              "Your model documentation has not been updated. \n")
        return False
    documentation = docs.get('documentation', "")
    if documentation == "":
        print("FATAL: Please make sure to your documentation (using the 'documentation' field) \n"
              "Your model documentation has not been updated. \n")
        return False

    # check authorization:
    auth = _check_jwt()
    if not auth:
        if not glob.SILENT:
            print("FATAL: We were unable to obtain JWT authorization for your account. \n"
                  "Your model has not been uploaded. \n")
        if glob.DEBUG:
            raise UploadModelError("We were unable to obtain JWT authorization.")
        return False

    # all ok, upload:
    if auth:

        url = glob.USER_MANAGER_URL + "/compute-function/" + glob.JWT_USER_ID + "/" + cfid

        # Setup the actual request
        data: dict = {
            "language": "WASM",
            "public": True,
            "profit": 0.1,
            "cycles": 1.0,
            "name": name,
            "docs": documentation
        }
        payload: dict = {
            'data': json.dumps(data)
        }

        files = []
        headers = {
            'Authorization': glob.JWT_TOKEN
        }

        # Do the request (and make sure to delete the gzip if errors occur)
        try:
            response = requests.put(url, headers=headers, data=payload, files=files)
        except Exception as e:
            if not glob.SILENT:
                print(f"FATAL: Unable to carry out the upload request: the toolchain is not available. \n"
                      "Your model documentation has not been updated. PLACE 2 URL: {url} \n")
                print(url)
            if glob.DEBUG:
                raise UploadModelError("We were unable to obtain JWT authorization: " + str(e))
            return False

        # Error handling
        try:
            response_data = json.loads(response.text)
        except Exception as e:
            if not glob.SILENT:
                print("FATAL: We did not receive a valid JSON response from the toolchain-server. \n"
                      "Your model documentation has not been updated. \n")
            if glob.DEBUG:
                raise UploadModelError("We did not receive a valid response from the server: " + str(e))
            return False

        if response_data['error']:
            if not glob.SILENT:
                print("FATAL: An error was returned by the server. \n"
                      "Your model documentation has not been updated. \n")
            if glob.DEBUG:
                raise UploadModelError("We did not receive a valid response from the server: " + response_data['error'])
            return False

        if glob.DEBUG:
            print("The documentation for " + cfid + " has been updated using:")
            print(data)

        # user feedback:
        if not glob.SILENT:
            print("Your model documentation has been updated. \n")
        return True

    else:
        return False


# assign assigns a model to a device
def assign(cfid, did, rid, _verbose=False):
    """ Assign a model to a device.

    Using the global JWT string this function assigns a model (using its cfid) to a device (using its did).

    Args:
        cfid: String identifying the model / compute-function
        did: String identifying the device
        rid: String identifying the registration ID of the device (not, run "devices"
        _verbose: Print feedback, default False

    Returns:
        Boolean indicating whether the assignment was successful.

    Raises (in debug mode):
        JWTError if unable to obtain JWT authorization
        CreateAssignmentError for other failures.
    """
    # check authorization:
    auth = _check_jwt()
    if not auth:
        if not glob.SILENT:
            print("FATAL: We were unable to obtain JWT authorization for your account. \n"
                  "Your model has not been uploaded. \n")
        if glob.DEBUG:
            raise CreateAssignmentError("We were unable to obtain JWT authorization.")
        return False

    # check fields not empty
    if not cfid or not did or not rid:
        if not glob.SILENT:
            print("FATAL: Please specify the correct ids. \n"
                  "Your assignment has not been submitted. \n")
        if glob.DEBUG:
            raise CreateAssignmentError("We were unable submit your assignment.")
        return False

    # all ok, assign:
    if auth:

        url = glob.USER_MANAGER_URL + "/assign/" + glob.JWT_USER_ID

        # Setup the actual request
        data: dict = {
            'modelId': cfid,
            'deviceId': did,
            'registrationId': rid
        }
        headers = {
            'Authorization': glob.JWT_TOKEN,
        }

        try:
            response = requests.post(url, headers=headers, data=json.dumps(data))
        except Exception as e:
            if not glob.SILENT:
                print("FATAL: Unable to carry out the assignment; the usermanager is not available. \n"
                      "Your model has not been assigned. \n")
            if glob.DEBUG:
                raise CreateAssignmentError("We were unable to obtain JWT authorization: " + str(e))
            return False

        # Error handling
        try:
            response_data = json.loads(response.text)
        except Exception as e:
            if not glob.SILENT:
                print("FATAL: We did not receive a valid JSON response from the user manager. \n"
                      "Your assignment has not been submitted. \n")
            if glob.DEBUG:
                raise CreateAssignmentError("We did not receive a valid response from the server: " + str(e))
            return False

        if response_data['error']:
            if not glob.SILENT:
                print("FATAL: An error was returned by the usermanager. \n"
                      "Your assignment has not been submitted. \n")
            if glob.DEBUG:
                raise UploadModelError("We did not receive a valid response from the server: " + response_data['error'])
            return False

        if glob.DEBUG:
            print("The following content has been send to the usermanager to create an assignment:")
            print(data)

        # user feedback:
        if not glob.SILENT:
            if _verbose:
                print("Your assignment has been added. \n")

        return True

    else:
        return False


# assignments gets all the assignments owned by the current user:
def assignments(offset=0, limit=20, _verbose=True, _return=False) -> dict:
    """ Get all assignments (i.e., cfid-did combinations).

    Args:
        offset: Int indicating the pagination offset. Default 0
        limit: Int inidcating the pagination limit. Default 20
        _verbose: Bool indicating whether the endpoints should be printed. Default True.
        _return: Bool indicating whether the endpoints should be returned as a dict. Default False.

    Returns:
         endpoints: if _return = True, a dict containing all the endpoints by the current user. [{},{},{}]
         otherwise the function will simply return True after printing the endpoints to the screen.

    Raises (in debug mode):
        JWTError if unable to obtain JWT authorization
        UserManagerError if unable to retrieve endpoint details
    """
    try:
        _check_jwt()
    except Exception as e:
        if not glob.SILENT:
            print("We were unable to renew your JWT lease. \n"
                  "If this recurs use the remove_credentials() function to reset your login credentials.")
        if glob.DEBUG:
            raise JWTError("Unable to check JWT authorization. " + str(e))
        return False

    url = glob.USER_MANAGER_URL + "/assignments/user/" + glob.JWT_USER_ID + "?limit=" + str(limit) + "&offset=" + str(
        offset)
    headers = {
        'Authorization': glob.JWT_TOKEN
    }

    try:
        response = requests.request("GET", url, headers=headers, data={})
        result = json.loads(response.text)
    except Exception as e:
        if not glob.SILENT:
            print("We were unable retrieve your assignments.")
        if glob.DEBUG:
            raise UserManagerError("Unable to retrieve assignments. " + str(e))
        return False

    # print if requested:
    if _verbose and not glob.SILENT:
        if not result:
            if offset == 0:
                print("You have not yet made any assignments.")
                print("\nNeed help getting started?")
                print(" - See the sclblpy docs at https://pypi.org/project/sclblpy/.")
                print(" - See our getting started tutorial at "
                      "https://github.com/scailable/sclbl-tutorials/tree/master/sclbl-101-getting-started.")
                print(" - Or, login to your admin at https://admin.sclbl.net. \n")
            else:
                print("No assignments found given the current settings; You could try to decrease the offset.")
        else:
            # Pretty printing of list
            i = 1
            print("We found the following assignments:\n")
            for key in result:
                print('  {}: {} <-> {} \n'
                      '   - cfid: {} \n'
                      '   - did: {} \n'
                      '   - rid: {} \n'.format(i, key['model_name'], key['device_name'], key['cfid'], key['did'], key['rid']))
                i = i + 1

    if _return:
        return result
    else:
        return True


# delete_assignments delete an assignment using its aid:
def delete_assignment(aid) -> bool:
    """ Delete an assignment

    Args:
        aid: String, the assignment id (UUID format)

    Returns:
        Boolean, True if assignment is deleted

    Raises (in debug mode):
        JWTError if unable to obtain JWT authorization
        UserManagerError if unable to retrieve endpoint details
    """
    try:
        _check_jwt()
    except Exception as e:
        if not glob.SILENT:
            print("We were unable to renew your JWT lease. \n"
                  "If this recurs use the remove_credentials() function to reset your login credentials.")
        if glob.DEBUG:
            raise JWTError("Unable to check JWT authorization. " + str(e))
        return False

    url = glob.USER_MANAGER_URL + "/assign/" + glob.JWT_USER_ID + "/" + aid
    headers = {
        'Authorization': glob.JWT_TOKEN
    }

    try:
        response = requests.request("DELETE", url, headers=headers)
        result = json.loads(response.text)
    except Exception as e:
        if not glob.SILENT:
            print("We were unable delete your assignment.")
        if glob.DEBUG:
            raise UserManagerError("Unable to delete assignment. " + str(e))
        return False

    if glob.DEBUG:
        print(result)

    return True


# devices lists all the devices owned by the current user:
def devices(offset=0, limit=20, _verbose=True, _return=False) -> dict:
    """ Get all devices owned by the current user.

    Args:
        offset: Int indicating the pagination offset. Default 0
        limit: Int inidcating the pagination limit. Default 20
        _verbose: Bool indicating whether the endpoints should be printed. Default True.
        _return: Bool indicating whether the endpoints should be returned as a dict. Default False.

    Returns:
         endpoints: if _return = True, a dict containing all the endpoints by the current user. [{},{},{}]
         otherwise the function will simply return True after printing the endpoints to the screen.

    Raises (in debug mode):
        JWTError if unable to obtain JWT authorization
        UserManagerError if unable to retrieve endpoint details
    """
    try:
        _check_jwt()
    except Exception as e:
        if not glob.SILENT:
            print("We were unable to renew your JWT lease. \n"
                  "If this recurs use the remove_credentials() function to reset your login credentials.")
        if glob.DEBUG:
            raise JWTError("Unable to check JWT authorization. " + str(e))
        return False

    url = glob.USER_MANAGER_URL + "/devices/" + glob.JWT_USER_ID + "?limit=" + str(limit) + "&offset=" + str(
        offset)
    headers = {
        'Authorization': glob.JWT_TOKEN
    }

    try:
        response = requests.request("GET", url, headers=headers, data={})
        result = json.loads(response.text)
    except Exception as e:
        if not glob.SILENT:
            print("We were unable retrieve your devices.")
        if glob.DEBUG:
            raise UserManagerError("Unable to retrieve devices. " + str(e))
        return False

    # print if requested:
    if _verbose and not glob.SILENT:
        if not result:
            if offset == 0:
                print("You have not yet registered any devices")
                print("\nNeed help getting started?")
                print(" - See the sclblpy docs at https://pypi.org/project/sclblpy/.")
                print(" - See our getting started tutorial at "
                      "https://github.com/scailable/sclbl-tutorials/tree/master/sclbl-101-getting-started.")
                print(" - Or, login to your admin at https://admin.sclbl.net. \n")
            else:
                print("No devices found given the current settings; You could try to decrease the offset.")
        else:
            # Pretty printing of list
            baseUrl = glob.EXAMPLE__BASE_URL
            i = 1
            print("We found the following device registrations:\n")
            for key in result:
                print('  {}: {}, \n'
                      '   - did: {} \n'
                      '   - rid: {} \n'.format(i, key['name'], key['did'], key['rid']))
                i = i + 1
            print("Login at https://admin.sclbl.net to administer your devices.\n")

    if _return:
        return result
    else:
        return True


# delete_device delete a device using its device id
def delete_device(did) -> bool:
    """ Delete a device

    Args:
        did: String, the device id (aaa-bbb-ccc format)

    Returns:
        Boolean, True if device is deleted

    Raises (in debug mode):
        JWTError if unable to obtain JWT authorization
        UserManagerError if unable to retrieve endpoint details
    """
    try:
        _check_jwt()
    except Exception as e:
        if not glob.SILENT:
            print("We were unable to renew your JWT lease. \n"
                  "If this recurs use the remove_credentials() function to reset your login credentials.")
        if glob.DEBUG:
            raise JWTError("Unable to check JWT authorization. " + str(e))
        return False

    url = glob.USER_MANAGER_URL + "/device/" + glob.JWT_USER_ID + "/" + did
    headers = {
        'Authorization': glob.JWT_TOKEN
    }

    try:
        response = requests.request("DELETE", url, headers=headers)
        result = json.loads(response.text)
    except Exception as e:
        if not glob.SILENT:
            print("We were unable delete your device.")
        if glob.DEBUG:
            raise UserManagerError("Unable to delete device. " + str(e))
        return False

    if glob.DEBUG:
        print(result)

    return True

# models lists the models / endpoints for the current user.
def models(offset=0, limit=20, _verbose=True, _return=False) -> dict:
    """ Print or return the endpoints available for the current user.

    Simple wrapper for the endpoints() function.

    Args:
        offset: Int indicating the pagination offset. Default 0
        limit: Int inidcating the pagination limit. Default 20
        _verbose: Bool indicating whether the endpoints should be printed. Default True.
        _return: Bool indicating whether the endpoints should be returned as a dict. Default False.

    Returns:
         endpoints: if _return = True, a dict containing all the endpoints by the current user. [{},{},{}]
         otherwise the function will simply return True after printing the endpoints to the screen.

    Raises (in debug mode):
        JWTError if unable to obtain JWT authorization
        UserManagerError if unable to retrieve endpoint details
    """
    return endpoints(offset=offset, limit=limit, _verbose=_verbose, _return=_return)


# endpoints lists the models / end
def endpoints(offset=0, limit=20, _verbose=True, _return=False) -> dict:
    """Print or return the endpoints available for the current user.

    Using the global JWT string this function by default prints a summary of the endpoints
    owned by the current user. The endpoints can also be returned as a dict by setting _return=True.

    Note that the call is paginated: use the offset and limit arguments to retrieve the desired
    list of endpoints. Endpoints are sorted with the latest upload being first, and the function retrieves
    the items from offset to (offset+limit). By default the 20 most recently created endpoints are returned.

    Args:
        offset: Int indicating the pagination offset. Default 0
        limit: Int inidcating the pagination limit. Default 20
        _verbose: Bool indicating whether the endpoints should be printed. Default True.
        _return: Bool indicating whether the endpoints should be returned as a dict. Default False.

    Returns:
         endpoints: if _return = True, a dict containing all the endpoints by the current user. [{},{},{}]
         otherwise the function will simply return True after printing the endpoints to the screen.

    Raises (in debug mode):
        JWTError if unable to obtain JWT authorization
        UserManagerError if unable to retrieve endpoint details

    """
    try:
        _check_jwt()
    except Exception as e:
        if not glob.SILENT:
            print("We were unable to renew your JWT lease. \n"
                  "If this recurs use the remove_credentials() function to reset your login credentials.")
        if glob.DEBUG:
            raise JWTError("Unable to check JWT authorization. " + str(e))
        return False

    url = glob.USER_MANAGER_URL + "/compute-functions/" + glob.JWT_USER_ID + "?limit=" + str(limit) + "&offset=" + str(
        offset)
    headers = {
        'Authorization': glob.JWT_TOKEN
    }

    try:
        response = requests.request("GET", url, headers=headers, data={})
        result = json.loads(response.text)
    except Exception as e:
        if not glob.SILENT:
            print("We were unable retrieve your endpoints.")
        if glob.DEBUG:
            raise UserManagerError("Unable to retrieve endpoints. " + str(e))
        return False

    # print if requested:
    if _verbose and not glob.SILENT:
        if not result:
            if offset == 0:
                print("You currently do not own any active endpoints.")
                print("\nNeed help getting started?")
                print(" - See the sclblpy docs at https://pypi.org/project/sclblpy/.")
                print(" - See our getting started tutorial at "
                      "https://github.com/scailable/sclbl-tutorials/tree/master/sclbl-101-getting-started.")
                print(" - Or, login to your admin at https://admin.sclbl.net. \n")
                print("NOTE: if you have just uploaded a model, please check your email; we will let you know when its "
                      "available!\n")
            else:
                print("No endpoints found given the current settings; You could try to decrease the offset.")
        else:
            # Pretty printing of list
            baseUrl = glob.EXAMPLE__BASE_URL
            i = 1
            print("You currently own the following endpoints:\n")
            for key in result:
                url = baseUrl + "?cfid=" + key['cfid']
                url += "&exin=" + urllib.parse.quote(key['exampleinput'])

                print('  {}: {}, \n'
                      '   - cfid: {} \n'
                      '   - example: {} \n'.format(i, key['name'], key['cfid'], url))
                i = i + 1
            print("Login at https://admin.sclbl.net to administer your endpoints and see integration examples.\n")

    if _return:
        return result
    else:
        return True


# delete model deletes a model:
def delete_model(cfid: str) -> bool:
    """Deletes a model by cfid.

    Delete an model owned by the currently logged in user by cfid.

    Args:
        cfid: String of the compute function id.

    Returns:
        True if successful, False otherwise.

    Raises  (in debug mode):
        JWTError if unable to obtain JWT authorization
        UserManagerError if unable to delete endpoints
    """
    return delete_endpoint(cfid)


# delete_endpoint deletes a given endpoint by id
def delete_endpoint(cfid: str) -> bool:
    """Deletes an endpoint by cfid.

    Delete an endpoint owned by the currently logged in user by cfid.

    Args:
        cfid: String of the compute function id.

    Returns:
        True if successful, False otherwise.

    Raises  (in debug mode):
        JWTError if unable to obtain JWT authorization
        UserManagerError if unable to delete endpoints
    """
    try:
        _check_jwt()
    except Exception as e:
        if not glob.SILENT:
            print("We were unable to renew your JWT lease. \n"
                  "If this recurs use the remove_credentials() function to reset your login credentials.")
        if glob.DEBUG:
            raise JWTError("Unable to check JWT authorization. " + str(e))
        return False

    url = glob.USER_MANAGER_URL + "/compute-function/" + glob.JWT_USER_ID + "/" + cfid
    headers = {
        'Authorization': glob.JWT_TOKEN,
    }
    try:
        response = requests.request("DELETE", url, headers=headers, data={})
        # Check if content type is JSON
        if 'json' in response.headers.get('Content-Type'):
            try:
                result = json.loads(response.text)
            except ValueError:  # simplejson.decoder.JSONDecodeError
                if not glob.SILENT:
                    print("Unable to decode JSON response from usermanager error.")
                if glob.DEBUG:
                    raise UserManagerError(result.get("Unable to decode JSON response from usermanager error."))
                return False
        else:
            if not glob.SILENT:
                print("Server at", glob.USER_MANAGER_URL, "did not return a valid JSON document.")
            if glob.DEBUG:
                raise UserManagerError("Server at", glob.USER_MANAGER_URL, "did not return a valid JSON document.")
            return False
    except Exception as e:
        if not glob.SILENT:
            print("We were unable to remove this endpoint from the server. \n"
                  "Please try again later.")
        if glob.DEBUG:
            raise UserManagerError("Unable to delete endpoint. " + str(e))
        return False

    if result.get("error") != "":
        if not glob.SILENT:
            print("We were unable to remove this endpoint: \n"
                  "Server error: " + str(result.get("error")))
        if glob.DEBUG:
            raise UserManagerError("Unable to delete endpoint. " + result.get("error"))
        return False

    if not glob.SILENT:
        print("Endpoint with cfid " + cfid + " was successfully deleted.")

    return True


# remove_credentials removes the user credentials
def remove_credentials(_verbose=True) -> bool:
    """Remove your stored credentials.

    Remove the .creds.json file that stores the username and password
    of the current user.

    Args:
        _verbose: Boolean indicator whether or not feedback should be printed. Default False.

    Returns:
        True is user credentials are found and deleted. False otherwise (often because they were not found).
    """

    # actual function in _utils.py to prevent circular includes.
    removed = _remove_credentials()
    if removed:
        if _verbose and not glob.SILENT:
            print("Successfully removed your user credentials.")
        return True
    else:
        if _verbose and not glob.SILENT:
            print("No user credentials found.")
        return False


# stop_print stops verbose printing of the package
def stop_print(_verbose=False) -> bool:
    """Stop ALL printing of user feedback from package.

    Args:
        _verbose: Boolean indicator whether or not feedback should be printed. Default False.

    Returns:
        True
    """
    if _verbose:
        print("Printing user feedback set to 'False'.")
    glob.SILENT = True
    return True


# start_print starts verbose printing of the package
def start_print() -> bool:
    """(re)start printing user feedback

    Returns:
        True

    """
    print("Printing user feedback set to 'True'.")
    glob.SILENT = False
    return True



# _set_toolchain_URL sets the location of the toolchain (for local testing)
def _set_toolchain_URL(url: str) -> str:
    """Change the location of the toolchain server.

    This function is internal and should not be used by average users of the package. However,
    it is useful for trouble-shooting the package either locally or on development servers.

    Args:
        url: String specifying the location of the toolchain server.

    Returns:
        str: The toolchains url.
    """
    glob.TOOLCHAIN_URL = url

    if not glob.SILENT:
        print("Toolchain url changed to: " + glob.TOOLCHAIN_URL)

    return glob.TOOLCHAIN_URL


# _set_usermanager_URL sets the location of the usermanager
def _set_usermanager_URL(url: str) -> str:
    """Change the location of the toolchain server

    This function is internal and should not be used by average users of the package. However,
    it is useful for trouble-shooting the package either locally or on development servers.

    Args:
        url: String specifying the location of the toolchain server

    Returns:
        The user-manager url
    """
    glob.USER_MANAGER_URL = url

    if not glob.SILENT:
        print("User-manager (admin) url changed to: " + glob.USER_MANAGER_URL)

    return glob.USER_MANAGER_URL


# _set_taskmanager_URL sets the location of the taskmanager
def _set_taskmanager_URL(url: str) -> str:
    """Change the location of the task manager

    This function is internal and should not be used by average users of the package. However,
    it is useful for trouble-shooting the package either locally or on development servers.

    Args:
        url: String specifying the location of the taskmanager server

    Returns:
        The task-manager url
    """
    glob.TASK_MANAGER_URL = url

    if not glob.SILENT:
        print("User-manager (admin) url changed to: " + glob.TASK_MANAGER_URL)

    return glob.TASK_MANAGER_URL


# _toggle_debug_mode turns debugging of or on.
def _toggle_debug_mode() -> bool:
    """Set debug to true or false.

    Can be used for debugging purposes such that exceptions are raised (including the stack trace)
    instead of suppressed.

    Note: the debug status is always printed when executing this method.

    Returns:
        Boolean indicating the status of the DEBUG global.
    """
    if glob.DEBUG:
        glob.DEBUG = False
        print("Debugging turned off.")
    else:
        glob.DEBUG = True
        print("Debugging turned on.")

    return glob.DEBUG


# _check_input_type
def _check_input_type(fv):
    """_check_input_type trie to determine the input type of the feature vector.

    Utility used by run()
    """
    if isinstance(fv, list):
        return "csv"
    else:

        # Parse to json
        try:
            js = json.loads(fv)
        except Exception as e:
            return False

        # Get the type
        try:
            input_type = js.get("type", False)
            if input_type in ["raw", "pb"]:
                return input_type
            else:
                return False
        except Exception as e:
            return False


def _run_csv(url, fv):
    """ run an endpoint using csv input. """
    # Create the input vector:
    try:
        data = ",".join(map(str, fv))
    except Exception as e:
        if not glob.SILENT:
            print("We were unable to convert your feature_vector to a valid input string. " + str(e))
        if glob.DEBUG:
            raise RunTaskError("We were unable to convert your feature_vector to a valid input string. " + str(e))
        return False

    # Do the actual call:
    try:
        payload = "{\"input\":{\"content-type\":\"json\",\"location\":\"embedded\",\"data\":\"{\\\"input\\\": [[" + data + "]]}\"},\"output\":{\"content-type\":\"json\",\"location\":\"echo\"},\"control\":1,\"properties\":{\"language\":\"WASM\"}}"
        headers = {
            'Content-Type': 'application/x-www-form-urlencoded'
        }
        response = requests.request("POST", url, headers=headers, data=payload)
    except Exception as e:
        if not glob.SILENT:
            print("We were unable execute the call. " + str(e))
        if glob.DEBUG:
            raise RunTaskError("We were unable to execute the call to our servers. " + str(e))
        return False

    return response


def _run_pb(url, fv):
    """ run an endpoint using pb input. """
    try:
        payload = "{\"input\":{\"content-type\":\"json\",\"location\":\"embedded\",\"data\":" \
                  + json.dumps(fv) + \
                  "},\"output\":{\"content-type\":\"json\",\"location\":\"echo\"}," \
                  "\"control\":1,\"properties\":{\"language\":\"WASM\"}}"
        headers = {
            'Content-Type': 'application/x-www-form-urlencoded'
        }
        response = requests.request("POST", url, headers=headers, data=payload)
    except Exception as e:
        if not glob.SILENT:
            print("We were unable execute the call. " + str(e))
        if glob.DEBUG:
            raise RunTaskError("We were unable to execute the call to our servers. " + str(e))
        return False

    return response


def _run_raw(url, fv):
    """ run an endpoint using raw input. """
    try:
        payload = "{\"input\":{\"content-type\":\"json\",\"location\":\"embedded\",\"data\":" \
                  + json.dumps(fv) + \
                  "},\"output\":{\"content-type\":\"json\",\"location\":\"echo\"}," \
                  "\"control\":1,\"properties\":{\"language\":\"WASM\"}}"
        headers = {
            'Content-Type': 'application/x-www-form-urlencoded'
        }
        response = requests.request("POST", url, headers=headers, data=payload)
    except Exception as e:
        if not glob.SILENT:
            print("We were unable execute the call. " + str(e))
        if glob.DEBUG:
            raise RunTaskError("We were unable to execute the call to our servers. " + str(e))
        return False

    return response


# No command line options for this script:
if __name__ == '__main__':
    print("No command line options available for main.py.")
