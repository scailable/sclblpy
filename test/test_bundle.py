# Simple unit tests for _bundly.py
from sclblpy._bundle import _gzip_save, _gzip_load, _gzip_delete

# Script settings:
from sclblpy.main import _toggle_debug_mode, stop_print

RUN_TESTS = False  # Prevent unintended testing
DEBUG = False  # Set to debug mode; if true it will raise exceptions
PRINTING = False  # Toggle printing on and off.

def test_gzip_save():
    """Test gzip save. """
    obj = {}
    obj["model_fit"] = "adfsdlafalskdf"
    obj["example"] = "model"

    # Test w. print
    _gzip_save(obj)


def test_gzip_load():
    """Test gzip load"""
    obj = _gzip_load()
    assert obj["example"] == "model", "Should be true"


def test_gzip_delete():
    _gzip_delete()


# Run tests:
if __name__ == '__main__':

    if not RUN_TESTS:
        print("Not running tests.")
        exit()

    if not PRINTING:
        stop_print()

    if DEBUG:
        _toggle_debug_mode()

    print("Running tests of _bundle.py")
    print("===============================")

    test_gzip_save()  # save model testing
    test_gzip_load()  # load model + print contents
    test_gzip_delete()  # delete the model
    test_gzip_delete()  # delete again

    print("===============================")
    print("All tests passed.")