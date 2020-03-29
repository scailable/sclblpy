# Tests for the utils. Note, these are just simple unit
# tests, a more elaborate tests of all models is found in
# test_all_models.py.
import sys

from sclblpy._utils import _model_supported, _model_is_fitted, _get_system_info, _predict
from sclblpy.main import _toggle_debug_mode, stop_print

from sklearn import svm
from sklearn import datasets
from xgboost import XGBRegressor
import numpy as np
import statsmodels.api as sm

# Script settings:
RUN_TESTS = False  # Prevent unintended testing
DEBUG = False  # Set to debug mode; if true it will raise exceptions
PRINTING = True  # Toggle printing on and off.


def test_supported_model():
    """Check whether or not a model is supported."""

    # First, try a sklearn svm:
    clf = svm.SVC()
    X, y = datasets.load_iris(return_X_y=True)
    clf.fit(X, y)
    assert _model_supported(clf) is True, "sklearn model should be supported."

    # Try a statsmodels model:
    nsample = 100
    x = np.linspace(0, 10, nsample)
    X = np.column_stack((x, x ** 2))
    beta = np.array([1, 0.1, 10])
    e = np.random.normal(size=nsample)
    X = sm.add_constant(X)
    y = np.dot(X, beta) + e
    est = sm.OLS(y, X)
    mod = est.fit()  # Robin wants the result object
    assert _model_supported(mod) is True, "statsmodel model should be supported."

    # Empty model
    mod = {}
    assert _model_supported(mod) is False, "Empty model should not be supported."

    # XG boost model:
    xgb = XGBRegressor()
    assert _model_supported(xgb) is True, "xgboost model should be supported."


def test_model_is_fitted():
    """ Test model is fitted() function """
    clf = svm.SVC()
    X, y = datasets.load_iris(return_X_y=True)
    assert _model_is_fitted(clf) is False, "Should not be fitted."
    clf.fit(X, y)
    assert _model_is_fitted(clf) is True, "Should be fitted."

    est = sm.OLS(y, X)
    assert _model_is_fitted(est) is False, "Should not be fitted."
    mod = est.fit()
    assert _model_is_fitted(mod) is True, "Should be fitted."

    # XG boost model:
    xgb = XGBRegressor()
    assert _model_is_fitted(xgb) is False, "Model should not be fitted"
    xgb.fit(X, y)
    assert _model_is_fitted(xgb) is True, "This one should be fitted"


def test_predict():

    # sklearn
    clf = svm.SVC()
    X, y = datasets.load_iris(return_X_y=True)
    clf.fit(X, y)
    assert _predict(clf, X[0, :]) == [0], "Wrong sklearn prediction"

    # statsmodels
    est = sm.OLS(y, X)
    mod = est.fit()
    assert _predict(mod, X[0, :]) == [-0.07861540851180868], "Wrong statsmodels prediction"

    # xgboost
    xgb = XGBRegressor()
    xgb.fit(X, y)
    assert _predict(xgb, X[0, :]) == [1.1295080184936523e-05], "Wrong XGB prediction"


def test_get_system_info():
    """ Test get system info """
    print(_get_system_info())


# Run tests
if __name__ == '__main__':

    if not RUN_TESTS:
        print("Not running tests.")
        exit()

    if not PRINTING:
        stop_print()

    if DEBUG:
        _toggle_debug_mode()

    print("Running tests of _utils.py")
    print("===============================")

    test_supported_model()
    test_model_is_fitted()
    test_get_system_info()
    test_predict()

    print("===============================")
    print("All tests passed.")
