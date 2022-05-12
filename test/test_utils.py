# Tests for the utils. Note, these are just simple unit
# tests, a more elaborate tests of all models is found in
# test_all_models.py.
import sys

from sclblpy._utils import _get_system_info
from sclblpy.main import _toggle_debug_mode, stop_print


# Script settings:
RUN_TESTS = 1  # Prevent unintended testing
DEBUG = 1  # Set to debug mode; if true it will raise exceptions
PRINTING = 1  # Toggle printing on and off.

def test_get_system_info():
    """ Test get system info """
    print(_get_system_info())


# Run tests
if __name__ == '__main__':

    if not RUN_TESTS:
        print("Not running tests.")
        exit()

    if not PRINTING:
        stop_print()

    if DEBUG:
        _toggle_debug_mode()

    print("Running tests of _utils.py")
    print("===============================")

    test_get_system_info()

    print("===============================")
    print("All tests passed.")
