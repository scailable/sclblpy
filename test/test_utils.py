from sclblpy import *
from sclblpy._utils import __model_supported, __model_is_fitted

from sklearn import svm
from sklearn import datasets

import numpy as np
import statsmodels.api as sm

from sclblpy.errors import ModelSupportError


def test_supported_model():
    """Check whether or not a model is supported."""
    print("checking model supported function")

    # First, try a sklearn svm:
    clf = svm.SVC()
    X, y = datasets.load_iris(return_X_y=True)
    clf.fit(X, y)

    if __model_supported(clf):
        print("model 1 supported: CORRECT")

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

    if __model_supported(model):
        print("model 2 supported CORRECT")

    if __model_supported(results):
        print("model 3 supported NOT CORRECT")

    try:
        __model_supported({})
    except ModelSupportError as e:
        print(str(e))


def test_model_is_fitted():
    """ Test model is fitted() function """
    clf = svm.SVC()
    X, y = datasets.load_iris(return_X_y=True)

    print(X.shape)

    print(__model_is_fitted(clf))
    clf.fit(X, y)
    print(__model_is_fitted(clf))

    print(clf.shape_fit_)


# Run tests
if __name__ == '__main__':
    print("Running tests of _utils.py")
    test_supported_model()
    test_model_is_fitted()
    print("All tests passed.")
