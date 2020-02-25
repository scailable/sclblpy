import pickle
import time

from sclblpy._bundle import _gzip_load, _gzip_delete
from sclblpy._jwt import _get_user_details
from sclblpy.main import remove_credentials, upload, endpoints, delete_endpoint

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

    print("# 1: Simple upload, no docs etc.")
    upload(clf)


    print("# 2: Docs, no example")
    docs = {}
    docs['name'] = "Name of model"
    docs['documentation'] = "A long .md thing...."
    upload(clf, docs)

    print("# 3: Example, no docs")
    row = X[130, :]
    upload(clf, feature_vector=row, _verbose=True)

    print("# 4: All args")
    upload(clf, docs, feature_vector=row, _verbose=True)

    # Test saving and loading:
    print("# 5: Test loading and retrieving:")
    upload(clf, docs, feature_vector=row, _verbose=False, _keep=True)
    obj = _gzip_load()
    _gzip_delete()
    mod = obj['fitted_model']
    pred = mod.predict(row.reshape(1, -1))
    print("YAY: " + str(pred))


def test_remove_credentials():
    """ Test of get user details"""
    _get_user_details()
    remove_credentials(True)


def test_endpoints():
    """ Test endpoint() function """
    endpoints()


def test_delete_endpoint():
    """ Test deleting an endpoint """
    cfid = ""
    ep = endpoints()
    try:
        cfid = ep[0]['cfid']
    except Exception as e:
        print(e)

    if cfid:
        delete_endpoint(cfid)


# Run tests
if __name__ == '__main__':
    print("Running simple functional tests of main.py")
    print("===============================")

    test_upload()
    test_remove_credentials()
    test_endpoints()
    test_delete_endpoint()

    print("===============================")
    print("All tests passed.")
