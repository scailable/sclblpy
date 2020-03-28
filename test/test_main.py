from sclblpy._bundle import _gzip_load, _gzip_delete
from sclblpy._jwt import _get_user_details
from sclblpy.main import remove_credentials, upload, endpoints, delete_endpoint, _set_toolchain_URL, _set_admin_URL, \
    list_models, start_print, stop_print, _toggle_debug_mode

import numpy as np
from sklearn import svm
from sklearn import datasets

# Script settings:
RUN_TESTS = False  # Prevent unintended testing
DEBUG = False  # Set to debug mode; if true it will raise exceptions
PRINTING = True  # Toggle printing on and off.
ADMIN_URL = "http://localhost:8008"  # Location of admin for this test
TOOLCHAIN_URL = "http://localhost:8010"  # Location of toolchain for this test


def test_upload():
    """ Test the upload function"""

    # Start fitting a simple model, no feature vecto
    clf = svm.SVC()
    X, y = datasets.load_iris(return_X_y=True)
    clf.fit(X, y)
    assert upload(clf, np.empty(0)) is False, "No valid feature vector."

    # Add docs
    docs = {}
    docs['name'] = "Name of model"
    docs['documentation'] = "A long .md thing...."
    assert upload(clf, np.empty(0), docs=docs) is False, "No valid feature vector."

    # Valid
    row = X[130, :]
    assert upload(clf, row, docs=docs) is True, "This should be valid."

    # Test saving and loading:
    upload(clf, row, docs=docs, _keep=True)
    obj = _gzip_load()
    _gzip_delete()
    mod = obj['fitted_model']
    pred = mod.predict(row.reshape(1, -1))
    assert pred == [2], "Prediction is not correct."


def test_remove_credentials():
    """ Test of get user details"""
    assert type(_get_user_details()) is dict, "This should be a dict."
    assert remove_credentials(True) is True, "This should return true if removed."


def test_endpoints():
    """ Test endpoint() function """
    assert isinstance(endpoints(), list) is True, "Endpoints should be a list"


def test_delete_endpoint():
    """ Test deleting an endpoint """
    cfid = ""
    ep = endpoints()

    try:
        cfid = ep[0]['cfid']
    except Exception as e:
        # Effectively there was no endpoint...
        print("No endpoints to remove; test not run.")

    if cfid:
        assert delete_endpoint(cfid) is True, "Should be able to delete an endpoint."


def test_setting_URLs():
    """ Test url setters: """
    _set_toolchain_URL(TOOLCHAIN_URL)
    _set_admin_URL(ADMIN_URL)


def test_user_utils():
    start_print()
    list_models()
    stop_print()
    list_models()
    start_print()


# Run tests
if __name__ == '__main__':

    if not RUN_TESTS:
        print("Not running tests.")
        exit()

    if not PRINTING:
        stop_print()

    if DEBUG:
        _toggle_debug_mode()

    print("Running simple functional tests of main.py")
    print("===============================")

    test_user_utils()
    test_setting_URLs()

    test_upload()
    test_remove_credentials()

    test_endpoints()
    # test_delete_endpoint()  # Uncomment to test deleting the first user endpoint.


    print("===============================")
    print("All tests passed.")
