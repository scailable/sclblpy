# Utility functions (internal)
import platform
import re
import socket
import sys
import uuid

from sclblpy.errors import ModelSupportError
import sclblpy._globals as glob
import inspect
import json
import sklearn
from sklearn.utils.validation import check_is_fitted


def _check_model(obj) -> bool:
    """Checks whether a model can be uploaded to Scailable.

    Checks whether the model is both supported (i.e., in the supported models list)
    and fitted.

    Args:
        obj: a fitted model

    Returns:
        True if passes all checks

    Raises:
        ModelSupportError if not correct
    """
    try:
        _model_supported(obj)
    except ModelSupportError as e:
        raise ModelSupportError("Unable to check of model is supported. " + str(e))

    if not _model_is_fitted(obj):
        raise ModelSupportError("Model does not seem fitted yet. Run .fit() before submitting.")

    return True


def _model_supported(obj) -> bool:
    """Checks whether the supplied model is supported.

    Checks whether a supplied model is present in the list of supported models (supported.json).

    Args:
        obj: The fitted model.

    Returns:
        True if it passes all checks.

    Raises:
        ModelSupportError.

    """
    if not glob.SUPPORTED_MODELS:
        _load_supported_models()

    try:
        model_name: str = _get_model_name(obj)
        model_base: str = _get_model_package(obj)
    except:
        raise ModelSupportError("Unable to retrieve model details")

    if (model_base in glob.SUPPORTED_MODELS and
            model_name in glob.SUPPORTED_MODELS[model_base]):
        return True
    else:
        return False


def _get_model_package(obj):
    """Gets the package name of a model object.

    Args:
        obj: a fitted model object

    Returns:
        base: string denoting the name of the package (e.g., sklearn)

    Raises:
        ModelSupportError.
    """
    mod = inspect.getmodule(obj)
    try:
        base, _sep, _stem = mod.__name__.partition('.')
    except Exception as e:
        raise ModelSupportError("Unable to get package name")
    return base


def _get_model_name(obj):
    """Get the name of a model.

    Function retrieves the name of a model from a fitted model
    by accessing the __name__ property.

    Args:
        obj: A model to be checked.

    Returns:
        name: String containing the name.

    Raises:
        ModelSupportError.
    """

    try:
        name =  type(obj).__name__
    except Exception as e:
        raise ModelSupportError("Unable to get model name")

    return name


def _load_supported_models():
    """Loads the supported model list.

    Function opens and parses the file supported.json in the current
    package folder to check the supported models.

    Note: the supported models are loaded into the glob.SUPPORTED_MODELS
    dictionary to make them available to the whole package.

    Args:

    Returns:

    Raises:
        ModelSupportError.
    """
    try:
        with open(glob.CURRENT_FOLDER + "/supported.json", "r") as f:
            glob.SUPPORTED_MODELS = json.load(f)
    except FileNotFoundError:
        raise ModelSupportError("Unable to find list of supported models.")


def _model_is_fitted(estimator):
    """Checks if a model is fitted.

    Function aims to see if a passed model object has been fitted already. If not
    it returns False.

    Args:
        obj: a model to be checked.

    Returns:
        Boolean indicating whether the model is fitted yes / no

    Raises:
    """
    if hasattr(estimator, '_is_fitted'):
        return estimator._is_fitted()

    try:
        check_is_fitted(estimator)
        return True
    except sklearn.exceptions.NotFittedError:
        return False


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