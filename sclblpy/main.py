import warnings

import requests as req
import time
import json
from getpass import getpass, GetPassWarning

USER_MANAGER_URL = "http://localhost:8008"  # Location of the user manager
TOOLCHAIN_URL = "http://check-with-robin.scailable.net"  # Location of the toolchain
JWT_TOKEN: str = ""  # JWT token
JWT_TIMESTAMP: float = 0.0  # Timestamp in seconds


# def upload():
#     """ Upload a fitted sklearn model to Scailable
#
#     ...
#
#     :return:
#     """
#     print("upload")
#     print(JWT_STRING)
#
#

def remove_credentials() -> bool:
    """ Remove your stored credentials """


def __check_jwt(seconds_refresh=120, seconds_renew=300) -> bool:
    """Checks whether a valid JWT string is present

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

    Returns:
        True if valid JWT string is present

    Raises:
        JWTError: if unable to obtain a valid JWT string
    """
    global JWT_TOKEN
    global JWT_TIMESTAMP

    now: float = time.time()
    time_refresh: float = now - seconds_refresh
    time_renew: float = now - seconds_renew

    if not JWT_TOKEN or JWT_TIMESTAMP < time_renew:
        print("Renew sign in:: NOT YET IMPLEMENTED!!")
        return False

    if JWT_TIMESTAMP < time_refresh:
        try:
            if __refresh_jwt():
                print("Refreshed JWT")
                return True
        except JWTError as e:
            raise JWTError("Unable to refresh JWT TOKEN. " + str(e))

    # else all ok:
    print("JWT OK")
    return True


def __get_user_details() -> dict:
    """ Get the username and password from a user """

    details: dict = {}
    try:
        with open("creds.json", "r") as f:
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
        with open("creds.json", "w+") as f:
            json.dump(details, f)

    print(details)
    return details


def __refresh_jwt() -> bool:
    """ Refresh JWT string

    Refresh the JWT string based on an existing token.

    Args:

    Returns:
        True if refresh successful

    Raises:
        JWTError if something is wrong.
    """
    global JWT_TOKEN
    global JWT_TIMESTAMP

    if not JWT_TOKEN:
        raise JWTError("No JWT token found")

    url: str = USER_MANAGER_URL + "/user/refresh/"
    headers = {
        'Authorization': JWT_TOKEN
    }

    try:
        resp: req.models.Response = req.get(url=url, headers=headers)
        result: dict = resp.json()
        if result.get("error") is not None:
            raise JWTError(result.get("error"))
        if result.get("token") is not None:
            JWT_TOKEN = result.get("token")
            JWT_TIMESTAMP = time.time()
            return True

    except req.exceptions.RequestException as a:
        raise LoginError("Cannot connect to Scailable servers.")


def __sign_in(username: str, password: str) -> bool:
    """ Perform signing of a user

    The function signin performs a signin of a user based
    on the username (str) and password (str). It returns
    a boolean value indicating whether the signin was succesful.

    Args:
        username: A string (email) to login the user
        password: A string (password for login

    Returns:
        True if sign in is successful

    Raises:
        LoginError: if unable to login
    """
    global JWT_TOKEN
    global JWT_TIMESTAMP

    if len(username) < 1 or len(password) < 1:
        raise LoginError("No username or password provided.")

    url: str = USER_MANAGER_URL + "/user/signin/"
    print(url)
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
            raise LoginError(result.get("error"))
        if result.get("token") is not None:
            JWT_TOKEN = result.get("token")
            JWT_TIMESTAMP = time.time()
            return True

    except req.exceptions.RequestException as a:
        raise LoginError("Cannot connect to Scailable servers.")

    return False


class LoginError(Exception):
    """ Login error """
    pass

class JWTError(Exception):
    """ JWT Error """
    pass


if __name__ == '__main__':
    print("No command line options yet.")
