# Global variables for the sclblpy package.
import os
from sclblpy.appdirs import AppDirs

# servers:
USER_MANAGER_URL: str = "https://admin.sclbl.net"  # Location of the user manager.
TOOLCHAIN_URL: str = "https://toolchain.sclbl.net"  # Location of the toolchain server.

# control printing:
SILENT: bool = False  # Suppress all printing.

# Storage locations:
dirs = AppDirs("sclblpy", "sclbl")
USER_CREDENTIALS: str = dirs.user_config_dir + "/.creds.json"  # User credentials
GZIP_BUNDLE: str = dirs.user_data_dir + "/model_bundle.gzip"  # Model bundle
MODELS_JSON: str = os.path.dirname(os.path.realpath(__file__)) + "/supported_models.json"  # Supported models

# JWT necessities:
JWT_TOKEN: str = ""  # JWT token.
JWT_USER_ID: str = ""  # Scailable user id.
JWT_TIMESTAMP: float = 0.0  # Timestamp in seconds.

# Available models:
SUPPORTED_MODELS: dict = {}  # List of supported models.


if __name__ == '__main__':
    print("No command line options available for _globals.py.")