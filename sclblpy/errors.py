# Custom errors for the sclblpy package.


class LoginError(Exception):
    """ Login error """
    pass


class JWTError(Exception):
    """ JWT Error """
    pass


class ModelSupportError(Exception):
    """ Model support error """
    pass


class ModelBundleError(Exception):
    """ Model pickle / gzip error """
    pass