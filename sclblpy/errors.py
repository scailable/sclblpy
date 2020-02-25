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


class UserManagerError(Exception):
    """ User manager error """
    pass


class GeneratePredictionError(Exception):
    """ Prediction error """
    pass


if __name__ == '__main__':
    print("No command line options available for errors.py")