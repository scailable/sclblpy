from sclblpy import *
from sclblpy._jwt import __check_jwt, __sign_in, __get_user_details
from sclblpy.main import remove_credentials


def test_JWT():
    """ Test __check_jwt() function """

    # Test with try:
    try:
        __check_jwt(seconds_refresh=2, seconds_renew=3)
        print("Success!")
    except JWTError as e:
        print("JWT error: " + str(e))

    # Test over time:
    __check_jwt(seconds_refresh=2, seconds_renew=3)
    __check_jwt(seconds_refresh=2, seconds_renew=3)
    time.sleep(2)
    __check_jwt(seconds_refresh=2, seconds_renew=3)
    time.sleep(4)
    __check_jwt(seconds_refresh=2, seconds_renew=3)
    remove_credentials()
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
        print("CORRECT!")

    # Try invalid
    username = "maurits@mauritskaptein.com"
    password = "dsfasfdaf90234i143"
    try:
        __sign_in(username, password)
    except LoginError as e:
        print("Unable to login: " + str(e))
        print("CORRECT!")

    # Try valid
    username = "maurits@mauritskaptein.com"
    password = "test"
    try:
        __sign_in(username, password)
        print("login successful")
        print("CORRECT!")
    except LoginError as e:
        print("Unable to login: " + str(e))


def test_get_user_details():
    """ Test of get user details"""
    print(__get_user_details())


# Run tests
if __name__ == '__main__':
    test_signin()
    test_get_user_details()
    test_JWT()  # check
    print("All tests passed.")