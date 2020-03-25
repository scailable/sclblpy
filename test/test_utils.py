# Tests for the utils. Note, these are just simple unit
# tests, a more elaborate tests of all models is found in
# test_all_models.py.
from sclblpy._utils import _model_supported, _model_is_fitted, _get_system_info, _predict
from sclblpy.errors import ModelSupportError

from sklearn import svm
from sklearn import datasets
from xgboost import XGBRegressor
import numpy as np
import statsmodels.api as sm

# Script settings:
RUN_TESTS = False  # Prevent unintended testing

def test_supported_model():
    """Check whether or not a model is supported."""

    # First, try a sklearn svm:
    clf = svm.SVC()
    X, y = datasets.load_iris(return_X_y=True)
    clf.fit(X, y)

    assert _model_supported(clf) == True, "Model should be supported."

    # Try a statsmodels model:
    nsample = 100
    x = np.linspace(0, 10, 100)
    X = np.column_stack((x, x ** 2))
    beta = np.array([1, 0.1, 10])
    e = np.random.normal(size=nsample)
    X = sm.add_constant(X)
    y = np.dot(X, beta) + e

    model = sm.OLS(y, X)
    results = model.fit()

    assert _model_supported(model) == True, "Model should be supported."

    if _model_supported(results):
        print("model 3 supported NOT CORRECT")

    try:
        _model_supported({})
    except ModelSupportError as e:
        print(str(e))

    # XG boost model:
    xgb = XGBRegressor()
    assert _model_supported(xgb) == True, "This one should be ok"


def test_model_is_fitted():
    """ Test model is fitted() function """
    clf = svm.SVC()
    X, y = datasets.load_iris(return_X_y=True)
    assert _model_is_fitted(clf) == False, "Should not be fitted."
    clf.fit(X, y)
    assert _model_is_fitted(clf) == True, "Should be fitted."

    model = sm.OLS(y, X)
    assert _model_is_fitted(model) == False, "Should not be fitted."
    model.fit()
    assert _model_is_fitted(model) == True, "Should be fitted."

    # XG boost model:
    xgb = XGBRegressor()
    assert _model_is_fitted(xgb) == False, "Model should not be fitted"
    xgb.fit(X, y)
    assert _model_is_fitted(xgb) == True, "This one should be fitted"


def test_predict():
    clf = svm.SVC()
    X, y = datasets.load_iris(return_X_y=True)
    clf.fit(X, y)
    assert _predict(clf, X[0, :]) == [0], "Wrong sklearn prediction"
    model = sm.OLS(y, X)
    assert _predict(model, X[0, :]) == [-0.07861540851180868], "Wrong statsmodels prediction"
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

    print("Running tests of _utils.py")
    print("===============================")

    test_supported_model()
    test_model_is_fitted()
    test_get_system_info()
    test_predict()

    print("===============================")
    print("All tests passed.")
