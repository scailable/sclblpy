# Utility functions (internal)
from sclblpy.errors import ModelSupportError
import sclblpy._globals as glob
import inspect
import json
import sklearn
from sklearn.utils.validation import check_is_fitted


def __check_model(obj) -> bool:
    """Checks whether a model can be uploaded to Scailable

    Args:
        obj: a fitted model

    Returns:
        True if passes all checks

    Raises:
        ModelSupportError if not correct
    """
    try:
        __model_supported(obj)
    except ModelSupportError as e:
        raise ModelSupportError("Unable to check of model is supported. " + str(e))

    if not __model_is_fitted(obj):
        raise ModelSupportError("Model does not seem fitted yet. Run .fit() before submitting.")

    return True


def __model_supported(obj) -> bool:
    """Checks whether the supplied model is supported.

    """
    if not glob.SUPPORTED_MODELS:
        __load_supported_models()

    try:
        model_name: str = __get_model_name(obj)
        model_base: str = __get_model_package(obj)
    except:
        raise ModelSupportError("Unable to retrieve model details")

    if (model_base in glob.SUPPORTED_MODELS and
            model_name in glob.SUPPORTED_MODELS[model_base]):
        return True
    else:
        return False


def __get_model_package(obj):
    """Gets the package name of a model object.

    Args:
        obj: a fitted model object
    """
    mod = inspect.getmodule(obj)
    base, _sep, _stem = mod.__name__.partition('.')
    return base


def __get_model_name(obj):
    return type(obj).__name__


def __load_supported_models():
    #global glob.SUPPORTED_MODELS
    try:
        with open(glob.CURRENT_FOLDER + "/supported.json", "r") as f:
            glob.SUPPORTED_MODELS = json.load(f)
    except FileNotFoundError:
        raise ModelSupportError("Unable to find list of supported models.")


def __model_is_fitted(estimator):
    if hasattr(estimator, '_is_fitted'):
        return estimator._is_fitted()

    try:
        check_is_fitted(estimator)
        return True
    except sklearn.exceptions.NotFittedError:
        return False
