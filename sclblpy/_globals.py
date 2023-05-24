# Global variables for the sclblpy package.
import os
from sclblpy._appdirs import AppDirs
# servers:
AUTH_MANAGER_URL = "https://api.sclbl.net/auth"
COMPUTE_API_URL = "https://api.sclbl.net/cpt"
DEVICE_API_URL = "https://api.sclbl.net/dev"

# control printing:
SILENT: bool = False  # Boolean indicating whether user feedback should be suppressed.
DEBUG: bool = False  # Boolean indicating whether using the package in debug mode; if so, it will raise exceptions.

# Storage locations:
dirs = AppDirs("sclblpy", "sclbl")
USER_CREDENTIALS: str = dirs.user_config_dir + "/.creds.json"  # Location of json file to store user credentials

package_dir = os.path.dirname(os.path.abspath(__file__))
JWT_JSON_FILE = os.path.join(package_dir, "glob.json")

if __name__ == '__main__':
    print("No command line options available for _globals.py.")
