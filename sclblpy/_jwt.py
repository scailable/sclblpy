# File contains all (private) method for jwt interaction.
import os
import warnings
import requests as req
import time
import json
from getpass import getpass, GetPassWarning

import sclblpy._globals as glob
from sclblpy.errors import LoginError, JWTError


def _check_jwt(seconds_refresh=120, seconds_renew=280, _verbose=True) -> bool:
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
        _verbose: Bool indicating whether feedback should be printed. Default True.

    Returns:
        True if valid JWT string is present.

    Raises:
        JWTError: if unable to obtain a valid JWT string.
    """
    now: float = time.time()
    time_refresh: float = now - seconds_refresh
    time_renew: float = now - seconds_renew

    if not glob.JWT_TOKEN or glob.JWT_TIMESTAMP < time_renew:
        user_details: dict = _get_user_details()
        try:
            _sign_in(user_details['username'], user_details['password'])
        except LoginError as e:
            raise JWTError("Unable to obtain JWT TOKEN. " + str(e))

    if glob.JWT_TIMESTAMP < time_refresh:
        try:
            if _refresh_jwt():
                return True
        except JWTError as e:
            raise JWTError("Unable to refresh JWT TOKEN. " + str(e))

    # JWT token is present and no need to refresh yet:
    return True


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
        raise LoginError("No username or password provided.")

    url: str = glob.USER_MANAGER_URL + "/user/signin/"
    data: dict = {
        'email': username,
        'pwd': password
    }
    headers: dict = {
        'Content-Type': 'text/plain'
    }

    try:
        resp: req.models.Response = req.post(url=url, headers=headers, json=data)
        result: dict = resp.json()
        if result.get("error") is not None:
            if _remove_file:
                _remove_credentials(False)  # Removing user credentials if they are not right
            raise LoginError(result.get("error"))
        if result.get("token") is not None:
            glob.JWT_TOKEN = result.get("token")
            glob.JWT_USER_ID = result.get("uuid")
            glob.JWT_TIMESTAMP = time.time()
            return True

    except req.exceptions.RequestException as a:
        raise LoginError("Cannot connect to Scailable servers.")

    return False


def _get_user_details() -> dict:
    """Gets the username and password from a user.

    Function tries to
    a. Retrieve username and password from .creds.json file.
    b. Retrieve username and password by prompting the user.

    If user responds 'y' to prompt to save the function will create
    .creds.json and store the user credentials.

    Args:

    Returns:
        A dict containing the fields
            'username' String
            'password' String

    Raises:


    """

    details: dict = {}
    try:
        with open(glob.USER_CREDENTIALS_FOLDER + ".creds.json", "r") as f:
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
        answ = query[0].lower()
        if query == '' or not answ in ['y', 'n']:
            print('Please answer with yes or no')
        else:
            break
    if answ == 'y':
        with open(glob.USER_CREDENTIALS_FOLDER + ".creds.json", "w+") as f:
            json.dump(details, f)

    return details


def _refresh_jwt() -> bool:
    """Refreshes the JWT string.

    Refresh the JWT string based on an existing token.

    Args:

    Returns:
        True if refresh successful

    Raises:
        JWTError if something is wrong with the JWT string.
        LoginError if unable to connect to servers.
    """
    if not glob.JWT_TOKEN:
        raise JWTError("No JWT token found")

    url: str = glob.USER_MANAGER_URL + "/user/refresh/"
    headers = {
        'Authorization': glob.JWT_TOKEN
    }

    try:
        resp: req.models.Response = req.get(url=url, headers=headers)
        result: dict = resp.json()
        if result.get("error") is not None:
            raise JWTError(result.get("error"))
        if result.get("token") is not None:
            glob.JWT_TOKEN = result.get("token")
            glob.JWT_TIMESTAMP = time.time()
            return True

    except req.exceptions.RequestException as a:
        raise LoginError("Cannot connect to Scailable servers.")


def _remove_credentials(_verbose=True):
    """Removes stored user credentials.

    Assuming credentials are stored in .creds.json the function
    deletes the .creds.json file.

    Args:
        _verbose: Bool indicating whether feedback should be printed. Default True.

    """
    path: str = glob.USER_CREDENTIALS_FOLDER + ".creds.json"
    if os.path.exists(path):
        os.remove(path)
        if _verbose:
            print("Removed user credentials.")
    else:
        if _verbose:
            print("No user credentials found.")


if __name__ == '__main__':
    print("No command line options yet for _jwt.py.")