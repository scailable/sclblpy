"""
The sclblpy package allows users to upload, monitor, and administer models and REST endpoints directly from python.
"""
# Ran on import of the package. Check version:
import sys

if sys.version_info < (3, 0):
    print('Sclblpy requires Python 3, while Python ' + str(sys.version[0] + ' was detected. Terminating... '))
    sys.exit(1)

from .main import upload, upload_sklearn, upload_onnx, update, update_sklearn, update_onnx, update_docs, \
    endpoints, delete_endpoint, models, delete_model, \
    devices, assignments, assign, \
    run, remove_credentials, list_models, \
    stop_print, start_print, \
    _set_toolchain_URL, _set_usermanager_URL, _set_taskmanager_URL
from .version import __version__

# Simple welcome message:
print("\n*** Thanks for importing sclblpy! ***")
print("You can use the 'upload()' function to upload your models.")
print("To inspect your currently uploaded models, use `endpoints()`.")
print("Check the docs at https://pypi.org/project/sclblpy/ for more info. \n")

