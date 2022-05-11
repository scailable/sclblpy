import time

from sclblpy._jwt import _get_user_details
from sclblpy.main import remove_credentials, upload_onnx, endpoints, delete_endpoint, _set_toolchain_URL, \
    _set_usermanager_URL, update_onnx, stop_print, _toggle_debug_mode, update_docs, run, \
    _set_taskmanager_URL, models, devices, delete_device, assignments, assign, delete_assignment, delete_model


RUN_TESTS = True  # Prevent unintended testing
DEBUG = True  # Set to debug mode; if true it will raise exceptions
PRINTING = True  # Toggle printing on and off.
ADMIN_URL = "https://usermanager.sclbl.net"  # Location of admin for this test
TOOLCHAIN_URL = "https://toolchain.sclbl.net"  # Location of toolchain for this test


def test_upload_onnx():
    """ Test the upload function (onnx)"""
    # Add docs
    docs = {}

    # ONNX
    docs['name'] = "Name of ONNX model"
    docs['documentation'] = "A long .md thing...."
    check = upload_onnx("../test/files/model.onnx", "", docs)
    assert check is True, "ONNX upload test failed."


def test_update():
    """ Test the update function (onnx)"""

    # Add and feature vector
    docs = {}
    docs['name'] = "Name of model - UPDATED"
    docs['documentation'] = "A long .md thing.... UPDATED"

    # Get an existing endpoint to update
    print(endpoints(_verbose=False, _return=True))

    # try except is a bit unusual in a test (as any fail in e.g. endpoints or the indexing will lead to the same output)
    #try:
    cfid = endpoints(_verbose=False, _return=True)[0]["cfid"]
    #except Exception as e:
    #    print("No endpoint to overwrite found")
    #    assert False is True, "No endpoint found for overwrite test."

    print("Updating: " + cfid)

    # Overwrite with valid docs:
    result = update_onnx("../test/files/model.onnx", cfid=cfid,example="", docs=docs) #
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





def test_remove_credentials():  # Also tested in JWT.
    """ Test of get user details"""
    assert type(_get_user_details()) is dict, "This should be a dict."
    assert remove_credentials(True) is True, "This should return true if removed."


def test_setting_URLs():
    """ Test url setters: """
    _set_toolchain_URL(TOOLCHAIN_URL)
    _set_usermanager_URL(ADMIN_URL)




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

    test_upload_onnx()  # upload an onnx test

    print("Wait, toolchain needs to finish....")
    time.sleep(25)
    print(" waited for 25 seconds")

    print('testing update \n\n')
    test_update()  # update an onnx test
    print('testing update docs \n\n')
    test_update_docs()  # update only docs test
    print('testing assign functions \n\n')
    test_assign_functions()  # test creating and removing assignments


    # The test below deletes the device registration, so it's commented out to keep the tests repeatable

    print('testing endpoint functions \n\n')
    print(endpoints(_return=True))
    test_endpoints_functions()  # test getting and deleting models

    #print('testing device functions \n\n')
    #test_devices_functions()  # test device get and delete


    ## MISSSING: REMOVE THE CREATED MODELS!!!

    # More obscure tests, not run by default / commented out
    #test_user_utils()
    #test_remove_credentials()
    #test_run()

    print("===============================")
    print("All tests passed.")
    exit()

