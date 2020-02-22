import time

from sclblpy import *
from sclblpy import __sign_in
from sclblpy import __check_jwt
from sclblpy import __get_user_details


def test_get_user_details():
    """ Test of get user details"""
    __get_user_details()


def test_JWT():
    """Test __validJWT() function"""

    # Test fist try
    try:
        __check_jwt(seconds_refresh=2, seconds_renew=3)
        print("Success!")
    except JWTError as e:
        print("JWT error: " + str(e))

    # Test over time:
    __check_jwt(seconds_refresh=2, seconds_renew=3)
    __sign_in("maurits@mauritskaptein.com", "test")
    __check_jwt(seconds_refresh=2, seconds_renew=3)
    time.sleep(2)
    __check_jwt(seconds_refresh=2, seconds_renew=3)
    time.sleep(4)
    __check_jwt(seconds_refresh=2, seconds_renew=3)


def test_signin():
    """Test __signin() function"""

    # Try empty
    username: str = ""
    password: str = ""
    try:
        __sign_in(username, password)
    except LoginError as e:
        print("Unable to login: " + str(e))

    # Try invalid
    username = "maurits@mauritskaptein.com"
    password = "dsfasfdaf90234i143"
    try:
        __sign_in(username, password)
    except LoginError as e:
        print("Unable to login: " + str(e))

    # Try valid
    username = "maurits@mauritskaptein.com"
    password = "test"
    try:
        __sign_in(username, password)
        print("login successful")
    except LoginError as e:
        print("Unable to login: " + str(e))


# Run tests
if __name__ == '__main__':
    #test_JWT()  # check
    #test_signin()
    test_get_user_details()

    print("All tests passed.")
