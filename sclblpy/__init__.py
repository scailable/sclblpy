"""
The sclblpy package allows users to manage account, models and devices
"""
# Ran on import of the package. Check version:
import sys

if sys.version_info < (3, 0):
    print('Sclblpy requires Python 3, while Python ' + str(sys.version[0] + ' was detected. Terminating... '))
    sys.exit(1)

from .auth import register_, log_in, get_user_details, set_new_password, \
    password_reset, log_out

from .compute import upload_model, update_model, delete_model, \
    get_model, get_all_models, models_statistics, \
    add_catalogue, update_catalogue, delete_catalogue, get_catalogue,\
    get_all_catalogues, config_parameters

from .device import add_device, update_device, delete_device, \
    assign_model_to_device, get_device, get_all_devices, devices_statistics,\
    add_devices_to_group, delete_device_from_group, get_groups, delete_group

from .version import __version__

