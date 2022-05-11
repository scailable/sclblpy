import time

from sclblpy import _set_toolchain_URL, _set_usermanager_URL, stop_print
from sclblpy._jwt import _check_jwt, _sign_in, _remove_credentials, _get_user_details
from sclblpy.errors import JWTError
from sclblpy.main import _toggle_debug_mode

# Script settings:
RUN_TESTS = 1  # Prevent unintended testing
DEBUG = 0  # Set to debug mode; if true it will raise exceptions
PRINTING = 1  # Toggle printing on and off.
ADMIN_URL = "https://usermanager.sclbl.net"  # Location of admin for this test
TOOLCHAIN_URL = "https://toolchain.sclbl.net"  # Location of toolchain for this test

# For the tests to pass we need a valid email and password:
EMAIL = "email-here"
PASSWORD = "password-here"


def test_JWT():
    """ Test __check_jwt() function """

    assert _check_jwt(seconds_refresh=2, seconds_renew=3) is True, "This should be true with the right credentials"

    # Test over time:
    assert _check_jwt(seconds_refresh=2, seconds_renew=3) is True, "This should be true with the right credentials"
    assert _check_jwt(seconds_refresh=2, seconds_renew=3) is True, "This should be true with the right credentials"
    time.sleep(2)
    assert _check_jwt(seconds_refresh=2, seconds_renew=3) is True, "This should be true with the right credentials"
    time.sleep(4)
    assert _check_jwt(seconds_refresh=2, seconds_renew=3) is True, "This should be true with the right credentials"
    _remove_credentials()
    assert _check_jwt(seconds_refresh=2, seconds_renew=3) is True, "This should be true with the right credentials"
    time.sleep(4)
    assert _check_jwt(seconds_refresh=2, seconds_renew=3) is True, "This should be true with the right credentials"


def test_signin():
    """Test __signin() function"""

    # Try empty
    email: str = ""
    password: str = ""
    assert _sign_in(email, password) is False, "This should not log in"

    # Try invalid
    email = "blabla@blabla.com"
    password = "not-a-valid-password"
    assert _sign_in(email, password) is False, "This should not log in 2"

    # Try valid
    email = EMAIL
    password = PASSWORD
    assert _sign_in(email, password) is True, "This should sign in (if the email and pass indeed exist)."


def test_get_user_details():
    """ Test of get user details"""
    assert type(_get_user_details()) is dict, "This should be a dict"
    assert _remove_credentials() is True, "This should be True"
    assert type(_get_user_details()) is dict, "This should be a dict"


# Run tests
if __name__ == '__main__':

    if not RUN_TESTS:
        print("Not running tests.")
        exit()

    if not PRINTING:
        stop_print()

    if DEBUG:
        _toggle_debug_mode()

    print("Running tests of _jwt.py")
    print("These take a few seconds to simulate refreshing etc.")
    print("===============================")

    # Set correct endpoints
    _set_toolchain_URL(TOOLCHAIN_URL)
    _set_usermanager_URL(ADMIN_URL)

    test_signin()
    test_get_user_details()
    test_JWT()

    print("===============================")
    print("All tests passed.")