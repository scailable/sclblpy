"""
The sclblpy package allows users to upload, monitor, and administer models and REST endpoints directly from python.
"""
from .main import upload, update, update_docs, endpoints, delete_endpoint, remove_credentials, list_models, stop_print, \
    start_print, _set_toolchain_URL, _set_usermanager_URL
from .version import __version__

