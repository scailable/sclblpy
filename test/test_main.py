import time

from sclblpy._bundle import _gzip_load, _gzip_delete
from sclblpy._jwt import _get_user_details
from sclblpy.main import remove_credentials, upload, endpoints, delete_endpoint, _set_toolchain_URL, \
    _set_usermanager_URL, list_models, start_print, stop_print, _toggle_debug_mode, update, update_docs, run, \
    _set_taskmanager_URL

import sclblpy._globals as glob

import numpy as np
from sklearn import svm
from sklearn import datasets

# Script settings:
RUN_TESTS = False  # Prevent unintended testing
DEBUG = True  # Set to debug mode; if true it will raise exceptions
PRINTING = True  # Toggle printing on and off.
ADMIN_URL = "http://localhost:8008"  # Location of admin for this test
TOOLCHAIN_URL = "http://localhost:8010"  # Location of toolchain for this test
TASKMANAGER_URL = "http://localhost:8080"


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


def test_update():
    """ Test the update function"""

    # Start fitting a simple model, no feature vecto
    clf = svm.SVC()
    X, y = datasets.load_iris(return_X_y=True)
    clf.fit(X, y)

    # Add and feature vector
    docs = {}
    docs['name'] = "Name of model - UPDATED"
    docs['documentation'] = "A long .md thing.... UPDATED"
    row = X[130, :]

    # Get an existing endpoint to update
    try:
        cfid = endpoints(False)[0]["cfid"]
    except Exception as e:
        print("No endpoint to overwrite found")
        assert False == True, "no endpoint found for overwrite test"

    print("Updating: " + cfid)

    # Overwrite without docs
    update(clf, row, cfid, docs={})

    # Overwrite with valid docs:
    update(clf, row, cfid, docs=docs)


def test_update_docs():
    """ Test the update docs function """

    # Get an existing endpoint to update
    try:
        cfid = endpoints(False)[0]["cfid"]
    except Exception as e:
        print("No endpoint to overwrite found")
        assert False == True, "no endpoint found for overwrite test"

    update_docs(cfid, {})

    docs = {}
    docs['name'] = "UPDATED NAME"
    update_docs(cfid, docs)

    docs['documentation'] = "UPDATED MARKDOWN"
    update_docs(cfid, docs)


def test_run():
    """ Test running an endpoint

    Note: Only works with valid existing cfid and compatible fv.
    """
    cfid = "78c48c52-944f-11ea-ade6-a4d18cd729d6"

    fv = [7.4, 2.8, 6.1, 1.9]

    result = run(cfid, fv)

    assert result is not False, "Error in running test; are the cfid and featurve_vector ok?"
    print(result)

    if result['statusCode'] == 1:
        print(result['result'])


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
    _set_usermanager_URL(ADMIN_URL)
    _set_taskmanager_URL(TASKMANAGER_URL)


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

    test_setting_URLs()
    print(glob.USER_MANAGER_URL)
    print(glob.TOOLCHAIN_URL)
    print(glob.TASK_MANAGER_URL)

    if not PRINTING:
        stop_print()

    if DEBUG:
        _toggle_debug_mode()

    print("Running simple functional tests of main.py")
    print("===============================")

    test_user_utils()

    test_remove_credentials()

    test_upload()

    print("Wait, toolchain needs to finish....")
    time.sleep(10)

    test_update()

    print("Wait, update needs to finish....")
    time.sleep(10)
    test_update_docs()

    test_remove_credentials()

    test_endpoints()
    # test_delete_endpoint()  # Uncomment to test deleting the first user endpoint.

    test_run()

    print("===============================")
    print("All tests passed.")
