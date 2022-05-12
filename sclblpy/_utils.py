# Utility functions (internal)
import platform
import re
import socket
import sys
import uuid


def _get_system_info(_verbose=False):
    """Gets information regarding the system of the current user.

    Used for future debugging on the toolchain to see which systems we can
    and cannot work with properly.

    Args:
        _verbose: Bool indicating whether feedback should be printed. Default False.

    Returns:
        A dict containing system information.

    Raises:
    """
    info = {}
    try:

        info['platform'] = platform.system()
        info['platform-release'] = platform.release()
        info['platform-version'] = platform.version()
        info['architecture'] = platform.machine()
        info['hostname'] = socket.gethostname()
        info['ip-address'] = socket.gethostbyname(socket.gethostname())
        info['mac-address'] = ':'.join(re.findall('..', '%012x' % uuid.getnode()))
        info['processor'] = platform.processor()
        info['python'] = sys.version
        return info
    except Exception as e:
        if _verbose:
            print("Error getting system details: " + str(e))
        return info


if __name__ == '__main__':
    print("No command line options yet for _utils.py.")
