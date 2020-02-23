import pickle
import time

from sclblpy import *
from sclblpy import __sign_in
from sclblpy import __check_jwt
from sclblpy import __get_user_details

from sklearn import svm
from sklearn import datasets


def test_JWT():
    """ Test __check_jwt() function """

    # Test fist try
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


def test_get_user_details():
    """ Test of get user details"""
    print(__get_user_details())
    remove_credentials()
    print(__get_user_details())


def test_sklearn():
    """ Playing around with SKlearn and inspecting the model """
    # Check: https://scikit-learn.org/stable/tutorial/basic/tutorial.html
    clf = svm.SVC()
    X, y = datasets.load_iris(return_X_y=True)
    clf.fit(X, y)

    print(clf)
    print(type(clf))

    print(type(clf).__name__)

    s = pickle.dumps(clf)
    print(str(s))


# Run tests
if __name__ == '__main__':
    # test_JWT()  # check
    test_sklearn()
    print("All tests passed.")
