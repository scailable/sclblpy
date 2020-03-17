# Global variables for the sclblpy package.
import os

PKG_NAME: str = "sclblpy_v_0.01"

USER_MANAGER_URL: str = "http://localhost:8008"  # Location of the user manager.
TOOLCHAIN_URL: str = "http://localhost:8010"  # Location of the toolchain server.

JWT_TOKEN: str = ""  # JWT token.
JWT_USER_ID: str = ""  # Scailable user id.
JWT_TIMESTAMP: float = 0.0  # Timestamp in seconds.

USER_CREDENTIALS_FOLDER: str = ""  # Location where user credentials are stored.

CURRENT_FOLDER: str = os.path.dirname(os.path.realpath(__file__))  # Folder where the module is running.
SUPPORTED_MODELS: dict = {}  # List of supported models.
BUNDLE_NAME: str = "temp_sclbl_mod_bundle.gzip"


if __name__ == '__main__':
    print("No command line options available for _globals.py.")