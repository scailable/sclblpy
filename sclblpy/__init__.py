"""
The sclblpy package allows users to upload, monitor, and administer models and REST endpoints directly from python.
"""
# Ran on import of the package. Check version:
import sys

if sys.version_info < (3, 0):
    print('Sclblpy requires Python 3, while Python ' + str(sys.version[0] + ' was detected. Terminating... '))
    sys.exit(1)

from .main import welcome, \
    upload, upload_sklearn, upload_onnx, update, update_sklearn, update_onnx, update_docs, \
    endpoints, delete_endpoint, models, delete_model, \
    devices, delete_device, assignments, assign, delete_assignment, \
    run, remove_credentials, list_models, \
    stop_print, start_print, \
    _set_toolchain_URL, _set_usermanager_URL, _set_taskmanager_URL
from .version import __version__


