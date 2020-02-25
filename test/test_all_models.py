# Testing the upload function for all supported models.
# This might take a while..
import numpy as np

import statsmodels.api as sm

from sklearn import datasets
from sklearn import svm

from sclblpy import upload
from sclblpy._utils import _get_model_name, _get_model_package, _model_supported, _model_is_fitted

# Verbose?
PRINT_ALL = True


# StatsModels
def test_sm_ols():
    X, y = datasets.load_iris(return_X_y=True)
    mod = sm.OLS(y, X)
    mod.fit()
    docs = {'name': "SVC test"}
    fv = X[0, :]
    upload(mod, docs, feature_vector=fv, _verbose=PRINT_ALL)



# Sklearn
def test_sk_svc():
    mod = svm.SVC()
    X, y = datasets.load_iris(return_X_y=True)
    mod.fit(X, y)
    docs = {'name': "SVC test"}
    fv = X[0, :]
    upload(mod, docs, feature_vector=fv, _verbose=PRINT_ALL)


if __name__ == '__main__':
    print("Running tests off all supported models. This might take some time")
    print("===============================")

    print("# Statsmodels:")
    test_sm_ols()

    print("# SciKit Learn:")
    test_sk_svc()

    print("===============================")
    print("All tests passed.")