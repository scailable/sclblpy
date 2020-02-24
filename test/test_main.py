import pickle
import time

from sclblpy._bundle import __gzip_load
from sclblpy._jwt import __get_user_details
from sclblpy.main import remove_credentials, upload

from sklearn import svm
from sklearn import datasets

import numpy as np
import statsmodels.api as sm

def test_upload():
    """ Test the upload function"""

    # Start fitting a simple model
    clf = svm.SVC()
    X, y = datasets.load_iris(return_X_y=True)
    clf.fit(X, y)
    row = X[0,:]

    upload(clf)
    upload(clf, row, _keep=True)

    obj = __gzip_load()
    print(obj)




def test_remove_credentials():
    """ Test of get user details"""
    __get_user_details()
    remove_credentials()


# Run tests
if __name__ == '__main__':
    print("Running tests of main.py")
    # test_remove_credentials()
    test_upload()
    print("All tests passed.")
