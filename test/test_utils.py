# Tests for the utils. Note, these are just simple unit
# tests, a more elaborate tests of all models is found in
# test_all_models.py.

from sclblpy._utils import _model_supported, _model_is_fitted, _get_system_info
from sclblpy.errors import ModelSupportError

from sklearn import svm
from sklearn import datasets

import numpy as np
import statsmodels.api as sm


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


def test_get_system_info():
    """ Test get system info """
    print(_get_system_info())


# Run tests
if __name__ == '__main__':
    print("Running tests of _utils.py")
    print("===============================")

    test_supported_model()
    test_model_is_fitted()
    test_get_system_info()

    print("===============================")
    print("All tests passed.")
