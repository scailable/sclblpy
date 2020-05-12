# Utility functions (internal)
import platform
import re
import socket
import sys
import uuid
import inspect
import json

from sklearn.utils.validation import check_is_fitted
from sklearn.exceptions import NotFittedError

from sclblpy.errors import ModelSupportError, GeneratePredictionError
import sclblpy._globals as glob


def _check_model(obj) -> bool:
    """Checks whether a model can be uploaded to Scailable.

    Checks whether the model is both supported (i.e., in the supported models list)
    and fitted. Effectively a wrapper around _model_supported() and _model_is_fitted().

    Args:
        obj: a fitted model

    Returns:
        True if passes all checks
    """
    if _model_supported(obj):
        if _model_is_fitted(obj):
            return True
        else:
            return False
    else:
        return False


def _model_supported(obj) -> bool:
    """Checks whether the supplied model is supported.

    Checks whether a supplied model is present in the list of supported models (supported_models.json).

    Args:
        obj: The fitted model.

    Returns:
        True if it passes all checks.

    Raises (in debug mode):
        ModelSupportError.
    """
    # Check if supported models are loaded:
    if not glob.SUPPORTED_MODELS:
        if not _load_supported_models():
            if glob.DEBUG:
                raise ModelSupportError("Model check error: unable to load supported models.")
            return False

    try:
        model_base: str = _get_model_package(obj)  # This returns a string OR raises an error
        # statsmodels hack for dealing with the RegressionResultsWrapper:
        if model_base == "statsmodels":
            model_name: str = _get_model_name(obj.model)
        else:
            model_name: str = _get_model_name(obj)
    except Exception as e:
        if not glob.SILENT:
            print("Model check error: Unable to retrieve model and package name.")
        if glob.DEBUG:
            raise ModelSupportError("Model check error: Unable to retrieve model and package name: " + str(e))
        return False

    if (model_base in glob.SUPPORTED_MODELS and
            model_name in glob.SUPPORTED_MODELS[model_base]):
        return True
    else:
        return False


def _get_model_package(obj) -> str:
    """Gets the package name of a model object.

    Args:
        obj: a fitted model object

    Returns:
        base: string denoting the name of the package (e.g., sklearn)

    Raises (in debug mode):
        ModelSupportError.
    """
    mod = inspect.getmodule(obj)
    try:
        base, _sep, _stem = mod.__name__.partition('.')
    except Exception as e:
        raise ModelSupportError("Model check error: Unable to retrieve package name: " + str(e))

    return base


def _get_model_name(obj) -> str:
    """Get the name of a model.

    Function retrieves the name of a model from a fitted model
    by accessing the __name__ property.

    Args:
        obj: A model to be checked.

    Returns:
        name: String containing the name.

    Raises (in debug mode):
        ModelSupportError.
    """

    try:
        name = type(obj).__name__
    except Exception as e:
        raise ModelSupportError("Model check error: Unable to retrieve model name: " + str(e))

    return name


def _load_supported_models() -> bool:
    """Loads the supported model list.

    Function opens and parses the file supported_models.json in the current
    package folder to check the supported models.

    Note: the supported models are loaded into the glob.SUPPORTED_MODELS
    dictionary to make them available to the whole package.

    Args:

    Returns:
        True if the supported models are loaded into the global SUPPORTED_MODELS, False otherwise.

    Raises (in debug mode):
        ModelSupportError.
    """
    try:
        with open(glob.MODELS_JSON, "r") as f:
            glob.SUPPORTED_MODELS = json.load(f)
    except FileNotFoundError:
        if not glob.SILENT:
            print("Model check error: Unable to find list of supported models.")
        if glob.DEBUG:
            raise ModelSupportError("Model check error: Unable to find list of supported models.")
        return False

    return True


def _model_is_fitted(obj) -> bool:
    """Checks if a model is fitted.

    Function aims to see if a passed model object has been fitted already. If not
    it returns False.

    Args:
        obj: a model to be checked.

    Returns:
        Boolean indicating whether the model is fitted yes / no

    Raises:
    """
    if hasattr(obj, '_is_fitted'):
        return obj._is_fitted()

    # statsmodels:
    if hasattr(obj, 'fittedvalues'):
        return True

    # XGboost exception
    if _get_model_package(obj) == "xgboost":
        try:
            obj.feature_importances_
            return True
        except Exception as e:  # general exception to not include xgboost
            return False

    # lightgbm exceptoin
    if _get_model_package(obj) == "lightgbm":
        try:
            obj.n_features_
            return True
        except Exception as e:  # of not possible, not fitted
            return False

    try:
        check_is_fitted(obj)
        return True
    except NotFittedError:
        return False


def _predict(mod, feature_vector):
    """Generates predictions.

    Function to generate predictions and have the ability to
    deal with different model classes.

    Args:
        mod: A saved model instance
        feature_vector: A single row used for prediction (subset of dataset)

    Returns:
        A prediction (as list)

    Raises (in debug mode):
        GeneratePredictionError if unable to generate prediction.
    """
    package = _get_model_package(mod)
    if package == "sklearn":
        try:
            result = mod.predict(feature_vector.reshape(1, -1))
            return result.tolist()
        except Exception as e:
            raise GeneratePredictionError("Model check error: Unable generate sklearn prediction: " + str(e))

    elif package == "statsmodels":
        try:
            result = mod.predict(feature_vector.reshape(1, -1))
            return result.tolist()
        except Exception as e:
            raise GeneratePredictionError("Model check error: Unable generate statsmodels prediction: " + str(e))

    elif package == "xgboost":
        try:
            result = mod.predict(feature_vector.reshape(1, -1))
            return result.tolist()
        except Exception as e:
            raise GeneratePredictionError("Model check error: Unable generate xgboost prediction: " + str(e))

    else:  # whatever else:
        try:
            result = mod.predict(feature_vector.reshape(1, -1))
            return result.tolist()
        except Exception as e:
            raise GeneratePredictionError("Model check error: Unable generate xgboost prediction: " + str(e))

    raise GeneratePredictionError("Model check error: Predictions for your model are not supported.")


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
