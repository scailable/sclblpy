import time

from sclblpy import _set_toolchain_URL, _set_admin_URL
from sclblpy._jwt import _check_jwt, _sign_in, _remove_credentials, _get_user_details
from sclblpy.errors import LoginError, JWTError

# Script settings:
RUN_TESTS = False  # Prevent unintended testing
ADMIN_URL = "http://localhost:8008"  # Location of admin for this test
TOOLCHAIN_URL = "http://localhost:8010"  # Location of toolchain for this test

def test_JWT():
    """ Test __check_jwt() function """

    # Test with try:
    try:
        _check_jwt(seconds_refresh=2, seconds_renew=3)
        print("Success!")
    except JWTError as e:
        print("JWT error: " + str(e))

    # Test over time:
    _check_jwt(seconds_refresh=2, seconds_renew=3)
    _check_jwt(seconds_refresh=2, seconds_renew=3)
    time.sleep(2)
    _check_jwt(seconds_refresh=2, seconds_renew=3)
    time.sleep(4)
    _check_jwt(seconds_refresh=2, seconds_renew=3)
    _remove_credentials()
    _check_jwt(seconds_refresh=2, seconds_renew=3)
    time.sleep(4)
    _check_jwt(seconds_refresh=2, seconds_renew=3)


def test_signin():
    """Test __signin() function"""

    # Try empty
    username: str = ""
    password: str = ""
    try:
        _sign_in(username, password)
    except LoginError as e:
        print("Unable to login: " + str(e))
        print("CORRECT!")

    # Try invalid
    username = "maurits@mauritskaptein.com"
    password = "dsfasfdaf90234i143"
    try:
        _sign_in(username, password)
    except LoginError as e:
        print("Unable to login: " + str(e))
        print("CORRECT!")

    # Try valid
    username = "maurits@mauritskaptein.com"
    password = "test"
    try:
        _sign_in(username, password)
        print("login successful")
        print("CORRECT!")
    except LoginError as e:
        print("Unable to login: " + str(e))


def test_get_user_details():
    """ Test of get user details"""
    print(_get_user_details())
    print(_remove_credentials())
    print(_get_user_details())


# Run tests
if __name__ == '__main__':

    if not RUN_TESTS:
        print("Not running tests.")
        exit()

    print("Running tests of _jwt.py")
    print("These take a few seconds to simulate refreshing etc.")
    print("===============================")

    # Set correct endpoints
    _set_toolchain_URL(TOOLCHAIN_URL)
    _set_admin_URL(ADMIN_URL)

    test_signin()
    test_get_user_details()
    test_JWT()
    print("If no  errors / exceptions, all tests passed.")

    print("===============================")
    print("All tests passed.")