# Global variables for the sclblpy package.
import os
from sclblpy.appdirs import AppDirs

# servers:
USER_MANAGER_URL: str = "https://usermanager.sclbl.net:8008"  # Location of the user manager.
TOOLCHAIN_URL: str = "https://toolchain.sclbl.net:8010"  # Location of the toolchain server.
TASK_MANAGER_URL: str = "https://taskmanager.sclbl.net:8080"  # Location of the taskmanager.

# control printing:
SILENT: bool = False  # Boolean indicating whether user feedback should be suppressed.
DEBUG: bool = False  # Boolean indicating whether using the package in debug mode; if so, it will raise exceptions.

# Storage locations:
dirs = AppDirs("sclblpy", "sclbl")
USER_CREDENTIALS: str = dirs.user_config_dir + "/.creds.json"  # Location of json file to store user credentials
GZIP_BUNDLE: str = dirs.user_data_dir + "/model_bundle.gzip"  # Location where a save model is (temporarily) stored
MODELS_JSON: str = os.path.dirname(os.path.realpath(__file__)) + "/supported_models.json"  # Location of the json with supported models

# JWT necessities:
JWT_TOKEN: str = ""  # JWT token.
JWT_USER_ID: str = ""  # Scailable user id.
JWT_TIMESTAMP: float = 0.0  # Timestamp in seconds.

# Available models:
SUPPORTED_MODELS: dict = {}  # List of supported models.


if __name__ == '__main__':
    print("No command line options available for _globals.py.")