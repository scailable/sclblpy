import pickle
import time
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
    #print(row)
    #print(type(row))
    #print(row.shape)

    x = np.linspace(0, 10, 100)
    X = np.column_stack((x, x ** 2))
    X = sm.add_constant(X)
    row2 = X[0,:]
    #print(row2)
    #print(type(row2))
    #print(row2.shape)

    print("====")
    upload(clf)
    upload(clf, row)




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
