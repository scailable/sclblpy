import pickle
import time
from sclblpy import *
from sclblpy._jwt import __check_jwt, __sign_in, __get_user_details
from sclblpy._utils import __get_model_name, __get_model_package


def test_remove_credentials():
    """ Test of get user details"""
    __get_user_details()
    remove_credentials()


# Run tests
if __name__ == '__main__':
    test_remove_credentials()
    print("All tests passed.")
