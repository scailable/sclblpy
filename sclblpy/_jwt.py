# File contains all (private) methods for jwt interaction.
import os
import warnings
import requests as req
import time
import json
from getpass import getpass, GetPassWarning

import sclblpy._globals as glob
from sclblpy.errors import LoginError, JWTError


def _check_jwt(seconds_refresh=120, seconds_renew=280) -> bool:
    """Checks whether a valid JWT string is present.

    Checks whether a valid JWT string is present. If so,
    checks whether the JWT string needs refreshing (more than 2 mins old)
    and refreshes if necessary. Returns True when a valid and
    fresh JWT string is located.

    Note, if no JWT string is present, or the JWT string has expired,
    the function tries to
    a. Read username and pass from file
    b. Prompt user for username and pass
    and subsequently sign in.

    Args:
        seconds_refresh: int, seconds before a refresh is attempted. Default 120.
        seconds_renew: int, seconds before a renew is attempted. Default 280.

    Returns:
        True if valid JWT string is present and valid. False otherwise.

    Raises (in debug mode):
        JWTError: if unable to obtain a valid JWT string.
    """
    now: float = time.time()
    time_refresh: float = now - seconds_refresh
    time_renew: float = now - seconds_renew

    if not glob.JWT_TOKEN or glob.JWT_TIMESTAMP < time_renew:
        user_details: dict = _get_user_details()
        try:
            if _sign_in(user_details['username'], user_details['password']):
                return True
            else:
                return False
        except LoginError as e:
            if not glob.SILENT:
                print("JWT error: sign in failed:" + str(e))
            if glob.DEBUG:
                raise JWTError("Unable to obtain JWT TOKEN. " + str(e))
            return False

    if glob.JWT_TIMESTAMP < time_refresh:
        try:
            if _refresh_jwt():
                return True
            else:
                return False
        except JWTError as e:
            if not glob.SILENT:
                print("JWT error: refresh failed:" + str(e))
            if glob.DEBUG:
                raise JWTError("Unable to refresh JWT TOKEN. " + str(e))
            return False

    # JWT token is present and no need to refresh yet:
    if glob.JWT_TOKEN:
        return True
    else:
        # Edge case; JWT token empty:
        return False


def _sign_in(username: str, password: str, _remove_file=True) -> bool:
    """Performs the sign in of a user.

    The function sign in performs a sign in of a user based
    on the username (str) and password (str). It returns
    a boolean value indicating whether the sign in was successful.

    Args:
        username: A string (email) to login the user
        password: A string (password for login
        _remove_file: A bool indicating if the credentials should be removed on failed login. Default True.

    Returns:
        True if sign in is successful.

    Raises:
        LoginError: if unable to login.
    """
    if len(username) < 1 or len(password) < 1:
        if not glob.SILENT:
            print("JWT error: no username and password provided.")
        if glob.DEBUG:
            raise LoginError("No username or password provided.")
        return False

    url: str = glob.USER_MANAGER_URL + "/user/signin/"
    data: dict = {
        'email': username,
        'pwd': password
    }
    headers: dict = {
        'Content-Type': 'text/plain'
    }

    # Try connecting to server:
    try:
        resp: req.models.Response = req.post(url=url, headers=headers, json=data)

        # Check if content type is JSON and at least 10 bytes long
        if 'json' in resp.headers.get('Content-Type') and len(resp.content) > 10 and len(resp.content) < 400:
            try:
                # See if able to decode the JSON
                result: dict = resp.json()
            except ValueError:  # simplejson.decoder.JSONDecodeError
                if not glob.SILENT:
                    print("Unable to decode JSON error.")
                if glob.DEBUG:
                    raise LoginError(result.get("Unable to decode JSON error."))
                return False
        else:
            if not glob.SILENT:
                print("Server at", glob.USER_MANAGER_URL, "did not return a valid JSON document.")
            if glob.DEBUG:
                raise LoginError("Server at", glob.USER_MANAGER_URL, "did not return a valid JSON document.")
            return False

        if result.get("error") is not None:
            if _remove_file:
                _remove_credentials()  # Removing user credentials since they are not right
            if not glob.SILENT:
                print("JWT error: the server generated an error: " + result.get("error"))
            if glob.DEBUG:
                raise LoginError(result.get("JWT server error: " + result.get("error")))
            return False

        # If a JSON contains a token and a uid, all is ok:
        if result.get("token") is not None and result.get("uid") is not None:
            glob.JWT_TOKEN = result.get("token")
            glob.JWT_USER_ID = result.get("uid")
            glob.JWT_TIMESTAMP = time.time()
            return True
        else:
            # Token or UUID missing
            if not glob.SILENT:
                print("Missing key in server JWT response.")
            if glob.DEBUG:
                raise LoginError("Missing key in server response, server at:", glob.USER_MANAGER_URL)
            return False

    except req.exceptions.RequestException as a:
        if not glob.SILENT:
            print("JWT error: Unable to connect to scailable servers.")
        if glob.DEBUG:
            raise LoginError("Unable to connect to Scailable servers.")
        return False


def _get_user_details() -> dict:
    """Gets the username and password from a user.

    Function tries to
    a. Retrieve username and password from .creds.json file.
    b. Retrieve username and password by prompting the user.

    If user responds 'y' to prompt to save the function we will store the user credentials.

    Args:

    Returns:
        A dict containing the fields
            'username' String
            'password' String

    Raises (in debug mode):
        LoginError
    """

    details: dict = {}
    try:
        with open(glob.USER_CREDENTIALS, "r") as f:
            details = json.load(f)
            return details
    except FileNotFoundError:
        pass

    username: str = input("Please provide your username: ")
    with warnings.catch_warnings():
        warnings.simplefilter('ignore', GetPassWarning)
        password = getpass('Please type your password: ')

    details['username'] = username
    details['password'] = password

    while True:
        query = input('Would you like us to store your user credentials (y/n)? ')
        answer = query[0].lower()
        if query == '' or not answer in ['y', 'n']:
            print('Please answer with yes or no')
        else:
            break
    if answer == 'y':
        os.makedirs(os.path.dirname(glob.USER_CREDENTIALS), exist_ok=True)  # create the folder if it does not exists.
        with open(glob.USER_CREDENTIALS, "w+") as f:
            json.dump(details, f)

    return details


def _refresh_jwt() -> bool:
    """Refreshes the JWT string.

    Refresh the JWT string based on an existing token.

    Args:

    Returns:
        True if refresh successful, False otherwise.

    Raises (in debug mode):
        JWTError if something is wrong with the JWT string.
    """
    if glob.DEBUG:
        print("Refreshing JWT string.")

    if not glob.JWT_TOKEN:
        if not glob.SILENT:
            print("JWT error: token not found, unable to refresh.")
        if glob.DEBUG:
            raise JWTError("No JWT token found")
        return False

    url: str = glob.USER_MANAGER_URL + "/user/refresh/"
    headers = {
        'Authorization': glob.JWT_TOKEN
    }

    try:
        resp: req.models.Response = req.get(url=url, headers=headers)
        if 'json' in resp.headers.get('Content-Type'):
            try:
                # See if able to decode the JSON
                result: dict = resp.json()
            except ValueError:  # simplejson.decoder.JSONDecodeError
                if not glob.SILENT:
                    print("Unable to decode JSON error.")
                if glob.DEBUG:
                    raise LoginError(result.get("Unable to decode JSON error."))
                return False
        else:
            if not glob.SILENT:
                print("Server at", glob.USER_MANAGER_URL, "did not return a valid JSON document.")
            if glob.DEBUG:
                raise LoginError("Server at", glob.USER_MANAGER_URL, "did not return a valid JSON document.")
            return False

        if result.get("error") is not None:
            if not glob.SILENT:
                print("JWT refresh server error: " + str(result.get("error")))
            if glob.DEBUG:
                raise JWTError("JWT refresh server error: " + str(result.get("error")))
            return False

        if result.get("token") is not None:
            glob.JWT_TOKEN = result.get("token")
            glob.JWT_TIMESTAMP = time.time()
            return True

    except req.exceptions.RequestException as a:
        if not glob.SILENT:
            print("JWT refresh error: Unable to connect to Scailable servers.")
        if glob.DEBUG:
            raise JWTError("JWT refresh error: Unable to connect to Scailable servers.")

    return False


def _remove_credentials():
    """Removes stored user credentials.

    Assuming credentials are stored in .creds.json the function
    deletes the .creds.json file.

    Args:

    Returns:
        True if file found and deleted, false otherwise.
    """
    glob.JWT_TOKEN = ""  # Remove token.

    # and remove file:
    path: str = glob.USER_CREDENTIALS
    if os.path.exists(path):
        try:
            os.remove(path)
        except Exception as e:
            if not glob.SILENT:
                print("JWT delete error: Unable to remove your credentials.")
            if glob.DEBUG:
                raise JWTError("JWT delete error: Unable to remove credentials: " + str(e))
            return False
        if not glob.SILENT:
            print("Your stored user credentials have been removed. \n"
                  "Please re-enter your username and password next time you try to upload a model.")

        return True
    else:
        return False


if __name__ == '__main__':
    print("No command line options for _jwt.py.")