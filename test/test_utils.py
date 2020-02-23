from sclblpy import *
from sclblpy._utils import __model_supported

from sklearn import svm
from sklearn import datasets

import numpy as np
import statsmodels.api as sm


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
        print("model 2 supported UNSURE")

    if __model_supported(results):
        print("model 3 supported UNSURE")

    try:
        __model_supported({})
    except ModelSupportError as e:
        print(str(e))


# Run tests
if __name__ == '__main__':
    test_supported_model()
    print("All tests passed.")
