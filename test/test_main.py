import os
import time

from sclblpy._bundle import _gzip_load, _gzip_delete
from sclblpy._jwt import _get_user_details
from sclblpy.main import remove_credentials, upload, endpoints, delete_endpoint, _set_toolchain_URL, \
    _set_usermanager_URL, list_models, start_print, stop_print, _toggle_debug_mode, update, update_docs, run, \
    _set_taskmanager_URL, models, devices, delete_device, assignments, assign, delete_assignment, delete_model

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
    """ Test the upload function (sklearn and onnx"""

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
    assert upload(clf, row, docs=docs) is True, "SKlearn upload test failed."

    # ONNX
    docs['name'] = "Name of ONNX model"
    docs['documentation'] = "A long .md thing...."
    check = upload("../test/files/model.onnx", "", docs, model_type="onnx")
    assert check is True, "ONNX upload test failed."


def test_update():
    """ Test the update function (sklearn & onnx"""

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
        cfid = endpoints(_verbose=False, _return=True)[0]["cfid"]
    except Exception as e:
        print("No endpoint to overwrite found")
        assert False is True, "No endpoint found for overwrite test."

    print("Updating: " + cfid)

    # Overwrite without docs
    result = update(clf, row, cfid, docs={})
    assert result is True, "Sklearn update failed."

    # Get another endpoint to update
    try:
        cfid = endpoints(_verbose=False, _return=True)[1]["cfid"]
    except Exception as e:
        print("No endpoint to overwrite found 2")
        assert False == True, "no endpoint found for overwrite test 2"

    print("Updating: " + cfid)

    # Overwrite with valid docs:
    result = update("../test/files/model.onnx", "", cfid, docs=docs, model_type="onnx")
    assert result is True, "ONNX update failed."


def test_update_docs():
    """ Test the update docs function """

    # Get an existing endpoint to update
    try:
        cfid = endpoints(_verbose=False, _return=True)[0]["cfid"]
    except Exception as e:
        print("No endpoint to overwrite found for docs update")
        assert False == True, "no endpoint found for overwrite test for docs update"

    result = update_docs(cfid, {})
    assert result is False, "Docs should not be updated with empty."

    docs = {'name': "UPDATED DOCS NAME", 'documentation': "The updated docs."}
    result = update_docs(cfid, docs)
    assert result is True, "Update of docs failed."


def test_assign_functions():
    """ test create, get, delete for assignments """
    # Get existing devices
    try:
        d = devices(_return=True, _verbose=False)[0]
    except Exception as e:
        print("No devices found to test assignments")
        assert False == True, "No devices found; this test fails if no devices are registered."

    try:
        m = models(_return=True, _verbose=False)[0]
    except Exception as e:
        print("No models found to test assignments")
        assert False == True, "No models found; this test fails if no models are present."

    result = assign(m['cfid'], d['did'], d['rid'])
    assert result is True, "Failed to create assignment."

    ass_list = assignments(_return=True)
    assert isinstance(ass_list, list) is True, "The assignments should be a list"
    assert (len(ass_list) > 0) is True, "There should be at least one assignment"

    count = len(ass_list)
    try:
        aid = ass_list[0]['aid']
    except Exception as e:
        print("Unable to find assignment ID.")
        assert False == True, "Unable to find assignment ID."

    # check delete:
    result = delete_assignment(aid)
    assert result is True, "Failed to delete assignment."

    # check counts:
    ass_list2 = assignments(_return=True)
    count2 = len(ass_list2)
    assert (count2 == (count-1)) is True, "The deleted assignment count is not correct."


def test_endpoints_functions():
    """ Test endpoint() and models() function """
    assert isinstance(endpoints(_return=True), list) is True, "Endpoints should be a list"
    assert isinstance(models(_return=True), list) is True, "Models should be a list"

    # delete_endpoint
    cfid = ""
    ep = endpoints(_return=True)
    try:
        cfid = ep[0]['cfid']
    except Exception as e:
        # Effectively there was no endpoint...
        print("No endpoints to remove; test not run.")

    if cfid:
        assert delete_endpoint(cfid) is True, "Should be able to delete an endpoint."

    # delete model
    ep = endpoints(_return=True)
    try:
        cfid = ep[0]['cfid']
    except Exception as e:
        # Effectively there was no model...
        print("No endpoints to remove; test not run.")

    if cfid:
        assert delete_model(cfid) is True, "Should be able to delete a model."


def test_devices_functions():
    """ test get, delete for devices """

    # Get existing devices
    device_list = devices(_return=True)
    assert isinstance(device_list, list) is True, "The devices should be a list."
    assert (len(device_list) > 0) is True, "There should be at least one device for this test to run."

    count = len(device_list)
    try:
        did = device_list[0]['did']
    except Exception as e:
        print("Unable to find device ID.")
        assert False == True, "Unable to find device ID."

    # check delete:
    result = delete_device(did)
    assert result is True, "Failed to delete device."

    # check counts:
    device_list2 = devices(_return=True)
    count2 = len(device_list2)
    assert (count2 == (count-1)) is True, "The deleted device count is not correct."


# More obscure tests / please read docstrings and make sure settings are correct.
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


def test_remove_credentials():  # Also tested in JWT.
    """ Test of get user details"""
    assert type(_get_user_details()) is dict, "This should be a dict."
    assert remove_credentials(True) is True, "This should return true if removed."


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

    # Set target urls (and effectively test).
    test_setting_URLs()

    if not PRINTING:
        stop_print()  # serves as test and works.

    if DEBUG:
        _toggle_debug_mode()  # serves as test

    print("Running simple functional tests of main.py")
    print("===============================")

    test_upload()  # upload sklearn and onnx test

    print("Wait, toolchain needs to finish....")
    time.sleep(10)

    test_update()  # update sklearn and onnx test
    test_update_docs()  # update only docs test
    test_assign_functions()  # test creating and removing assignments
    test_endpoints_functions()  # test getting and deleting models
    test_devices_functions()  # test device get and delete

    # More obscure tests, not run by default / commented out
    #test_user_utils()
    #test_remove_credentials()
    #test_run()

    print("===============================")
    print("All tests passed.")
    exit()
