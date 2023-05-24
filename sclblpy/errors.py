# Custom errors for the sclblpy package.

class LoginError(Exception):
    """ Login error """
    pass


class LogoutError(Exception):
    """ Logout error """
    pass


class RegisterError(Exception):
    """ Register error """
    pass


class PwdError(Exception):
    """ Pwd error """
    pass


class UserDetailsError(Exception):
    """ User Details error """
    pass


class JWTError(Exception):
    """ JWT Error """
    pass


class CatalogueError(Exception):
    """ Catalogue error """
    pass


class ConfigError(Exception):
    """ Config error """
    pass


class ModelError(Exception):
    """ Model error """
    pass


class DeviceError(Exception):
    """ Device error """
    pass


class GroupError(Exception):
    """ Group error """
    pass


if __name__ == '__main__':
    print("No command line options available for errors.py")
