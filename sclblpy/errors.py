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


class UploadModelError(Exception):
    """ Upload model error """
    pass


class RunTaskError(Exception):
    """ Run task error"""
    pass


if __name__ == '__main__':
    print("No command line options available for errors.py")