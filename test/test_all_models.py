# Testing the upload function for all supported models.
# This might take a while..

import time
import statsmodels.api as sm

from sklearn import datasets
from sklearn import linear_model
from sklearn import tree
from sklearn import ensemble
from sklearn import svm

from xgboost import XGBClassifier
from xgboost import XGBRegressor
from xgboost import XGBRFClassifier
from xgboost import XGBRFRegressor

from sclblpy import upload, _set_toolchain_URL, _set_admin_URL
from sclblpy import endpoints
from sclblpy import delete_endpoint

# Script settings:
RUN_TESTS = False  # Prevent unintended testing
ADMIN_URL = "http://localhost:8008"  # Location of admin for this test
TOOLCHAIN_URL = "http://localhost:8010"  # Location of toolchain for this test
PRINT_ALL = True  # Verbose output?
TEAR_DOWN = True  # Remove all endpoints?

iris_data = datasets.load_iris(return_X_y=True)

# StatsModels
# https://www.statsmodels.org/stable/examples/index.html
def test_sm_OLS():
    X, y = iris_data
    estimator = sm.OLS(y, X)
    mod = estimator.fit()
    docs = {'name': "OLS test"}
    fv = X[0, :]
    upload(mod, docs, feature_vector=fv, _verbose=PRINT_ALL)
    print("Tested SM, OLS...")


def test_sm_GLS():
    data = sm.datasets.longley.load(as_pandas=False)
    X = sm.add_constant(data.exog)
    estimator = sm.GLS(data.endog, X, sigma=1)
    mod = estimator.fit()
    docs = {'name': "GLS test"}
    fv = X[0, :]
    upload(mod, docs, feature_vector=fv, _verbose=PRINT_ALL)
    print("Tested SM, GLS...")


def test_sm_WLS():
    Y = [1, 3, 4, 5, 2, 3, 4]
    X = range(1, 8)
    X = sm.add_constant(X)
    estimator = sm.WLS(Y, X, weights=list(range(1, 8)))
    mod = estimator.fit()
    docs = {'name': "WLS test"}
    fv = X[0, :]
    upload(mod, docs, feature_vector=fv, _verbose=PRINT_ALL)
    print("Tested SM, WLS...")


# Sklearn
def test_sk_ARDRegression():
    mod = linear_model.ARDRegression()
    X, y = iris_data
    mod.fit(X, y)
    docs = {'name': "ARDRegression test"}
    fv = X[0, :]
    upload(mod, docs, feature_vector=fv, _verbose=PRINT_ALL)
    print("Tested sklearn, ARDRegression...")


def test_sk_DecisionTreeClassifier():
    mod = tree.DecisionTreeClassifier()
    X, y = iris_data
    mod.fit(X, y)
    docs = {'name': "DecisionTreeClassifier test"}
    fv = X[0, :]
    upload(mod, docs, feature_vector=fv, _verbose=PRINT_ALL)
    print("Tested sklearn, DecisionTreeClassifier...")


def test_sk_DecisionTreeRegressor():
    mod = tree.DecisionTreeRegressor()
    X, y = iris_data
    mod.fit(X, y)
    docs = {'name': "DecisionTreeClassifier test"}
    fv = X[0, :]
    upload(mod, docs, feature_vector=fv, _verbose=PRINT_ALL)
    print("Tested sklearn, DecisionTreeRegressor...")


def test_sk_ElasticNet():
    mod = linear_model.ElasticNet()
    X, y = iris_data
    mod.fit(X, y)
    docs = {'name': "ElasticNet test"}
    fv = X[0, :]
    upload(mod, docs, feature_vector=fv, _verbose=PRINT_ALL)
    print("Tested sklearn, ElasticNet...")


def test_sk_ElasticNetCV():
    mod = linear_model.ElasticNetCV()
    X, y = iris_data
    mod.fit(X, y)
    docs = {'name': "ElasticNetCV test"}
    fv = X[0, :]
    upload(mod, docs, feature_vector=fv, _verbose=PRINT_ALL)
    print("Tested sklearn, ElasticNetCV...")


def test_sk_ExtraTreeClassifier():
    mod = tree.ExtraTreeClassifier()
    X, y = iris_data
    mod.fit(X, y)
    docs = {'name': "ExtraTreeClassifier test"}
    fv = X[0, :]
    upload(mod, docs, feature_vector=fv, _verbose=PRINT_ALL)
    print("Tested sklearn, ExtraTreeClassifier...")


def test_sk_ExtraTreeRegressor():
    mod = tree.ExtraTreeRegressor()
    X, y = iris_data
    mod.fit(X, y)
    docs = {'name': "ExtraTreeRegressor test"}
    fv = X[0, :]
    upload(mod, docs, feature_vector=fv, _verbose=PRINT_ALL)
    print("Tested sklearn, ExtraTreeRegressor...")


def test_sk_ExtraTreesClassifier():
    mod = ensemble.ExtraTreesClassifier()
    X, y = iris_data
    mod.fit(X, y)
    docs = {'name': "ExtraTreeClassifier test"}
    fv = X[0, :]
    upload(mod, docs, feature_vector=fv, _verbose=PRINT_ALL)
    print("Tested sklearn, Ensemble ExtraTreeClassifier...")


def test_sk_ExtraTreesRegressor():
    mod = ensemble.ExtraTreesRegressor()
    X, y = iris_data
    mod.fit(X, y)
    docs = {'name': "ExtraTreeRegressor test"}
    fv = X[0, :]
    upload(mod, docs, feature_vector=fv, _verbose=PRINT_ALL)
    print("Tested sklearn, Ensemble ExtraTreeRegressor...")


def test_sk_HuberRegressor():
    mod = linear_model.HuberRegressor()
    X, y = iris_data
    mod.fit(X, y)
    docs = {'name': "HuberRegressor test"}
    fv = X[0, :]
    upload(mod, docs, feature_vector=fv, _verbose=PRINT_ALL)
    print("Tested sklearn, HuberRegressor...")


def test_sk_Lars():
    mod = linear_model.Lars()
    X, y = iris_data
    mod.fit(X, y)
    docs = {'name': "Lars test"}
    fv = X[0, :]
    upload(mod, docs, feature_vector=fv, _verbose=PRINT_ALL)
    print("Tested sklearn, Lars...")


def test_sk_LarsCV():
    mod = linear_model.LarsCV()
    X, y = iris_data
    mod.fit(X, y)
    docs = {'name': "LarsCV test"}
    fv = X[0, :]
    upload(mod, docs, feature_vector=fv, _verbose=PRINT_ALL)
    print("Tested sklearn, LarsCV...")


def test_sk_Lasso():
    mod = linear_model.Lasso()
    X, y = iris_data
    mod.fit(X, y)
    docs = {'name': "Lasso test"}
    fv = X[0, :]
    upload(mod, docs, feature_vector=fv, _verbose=PRINT_ALL)
    print("Tested sklearn, Lasso...")


def test_sk_LassoCV():
    mod = linear_model.LassoCV()
    X, y = iris_data
    mod.fit(X, y)
    docs = {'name': "LassoCV test"}
    fv = X[0, :]
    upload(mod, docs, feature_vector=fv, _verbose=PRINT_ALL)
    print("Tested sklearn, LassoCV...")


def test_sk_LassoLars():
    mod = linear_model.LassoLars()
    X, y = iris_data
    mod.fit(X, y)
    docs = {'name': "LassoLars test"}
    fv = X[0, :]
    upload(mod, docs, feature_vector=fv, _verbose=PRINT_ALL)
    print("Tested sklearn, LassoLars...")


def test_sk_LassoLarsCV():
    mod = linear_model.LassoLarsCV()
    X, y = iris_data
    mod.fit(X, y)
    docs = {'name': "LassoLarsCV test"}
    fv = X[0, :]
    upload(mod, docs, feature_vector=fv, _verbose=PRINT_ALL)
    print("Tested sklearn, LassoLarsCV...")


def test_sk_LassoLarsIC():
    mod = linear_model.LassoLarsIC()
    X, y = iris_data
    mod.fit(X, y)
    docs = {'name': "LassoLarsIC test"}
    fv = X[0, :]
    upload(mod, docs, feature_vector=fv, _verbose=PRINT_ALL)
    print("Tested sklearn, LassoLarsIC...")


def test_sk_LinearRegression():
    mod = linear_model.LinearRegression()
    X, y = iris_data
    mod.fit(X, y)
    docs = {'name': "LinearRegression test"}
    fv = X[0, :]
    upload(mod, docs, feature_vector=fv, _verbose=PRINT_ALL)
    print("Tested sklearn, LinearRegression...")


def test_sk_LinearSVC():
    mod = svm.LinearSVC(max_iter=10000)  # Needs more iterations to converge
    X, y = iris_data
    mod.fit(X, y)
    docs = {'name': "LinearSVC test"}
    fv = X[0, :]
    upload(mod, docs, feature_vector=fv, _verbose=PRINT_ALL)
    print("Tested sklearn, LinearSVC...")


def test_sk_LinearSVR():
    mod = svm.LinearSVR(max_iter=100000)  # Needs way more iterations to converge
    X, y = iris_data
    mod.fit(X, y)
    docs = {'name': "LinearSVR test"}
    fv = X[0, :]
    upload(mod, docs, feature_vector=fv, _verbose=PRINT_ALL)
    print("Tested sklearn, LinearSVR...")


def test_sk_NuSCV():
    mod = svm.NuSVC(max_iter=10000)  # Needs more iterations to converge
    X, y = iris_data
    mod.fit(X, y)
    docs = {'name': "NuSCV test"}
    fv = X[0, :]
    upload(mod, docs, feature_vector=fv, _verbose=PRINT_ALL)
    print("Tested sklearn, NuSCV...")


def test_sk_NuSVR():
    mod = svm.NuSVR(max_iter=10000)  # Needs more iterations to converge
    X, y = iris_data
    mod.fit(X, y)
    docs = {'name': "NuSVR test"}
    fv = X[0, :]
    upload(mod, docs, feature_vector=fv, _verbose=PRINT_ALL)
    print("Tested sklearn, NuSVR...")


def test_sk_OrthogonalMatchingPursuit():
    mod = linear_model.OrthogonalMatchingPursuit()
    X, y = iris_data
    mod.fit(X, y)
    docs = {'name': "OrthogonalMatchingPursuit test"}
    fv = X[0, :]
    upload(mod, docs, feature_vector=fv, _verbose=PRINT_ALL)
    print("Tested sklearn, OrthogonalMatchingPursuit...")


def test_sk_OrthogonalMatchingPursuitCV():
    mod = linear_model.OrthogonalMatchingPursuitCV()
    X, y = iris_data
    mod.fit(X, y)
    docs = {'name': "OrthogonalMatchingPursuitCV test"}
    fv = X[0, :]
    upload(mod, docs, feature_vector=fv, _verbose=PRINT_ALL)
    print("Tested sklearn, OrthogonalMatchingPursuitCV...")


def test_sk_PassiveAggressiveClassifier():
    mod = linear_model.PassiveAggressiveClassifier()
    X, y = iris_data
    mod.fit(X, y)
    docs = {'name': "PassiveAggressiveClassifier test"}
    fv = X[0, :]
    upload(mod, docs, feature_vector=fv, _verbose=PRINT_ALL)
    print("Tested sklearn, PassiveAggressiveClassifier...")


def test_sk_PassiveAggressiveRegressor():
    mod = linear_model.PassiveAggressiveRegressor()
    X, y = iris_data
    mod.fit(X, y)
    docs = {'name': "PassiveAggressiveRegressor test"}
    fv = X[0, :]
    upload(mod, docs, feature_vector=fv, _verbose=PRINT_ALL)
    print("Tested sklearn, PassiveAggressiveRegressor...")


def test_sk_RandomForestClassifier():
    mod = ensemble.RandomForestClassifier()
    X, y = iris_data
    mod.fit(X, y)
    docs = {'name': "RandomForestClassifier test"}
    fv = X[0, :]
    upload(mod, docs, feature_vector=fv, _verbose=PRINT_ALL)
    print("Tested sklearn, RandomForestClassifier...")


def test_sk_RandomForestRegressor():
    mod = ensemble.RandomForestRegressor()
    X, y = iris_data
    mod.fit(X, y)
    docs = {'name': "RandomForestRegressor test"}
    fv = X[0, :]
    upload(mod, docs, feature_vector=fv, _verbose=PRINT_ALL)
    print("Tested sklearn, RandomForestRegressor...")


def test_sk_RANSACRegressor():
    mod = linear_model.RANSACRegressor()
    X, y = iris_data
    mod.fit(X, y)
    docs = {'name': "RANSACRegressor test"}
    fv = X[0, :]
    upload(mod, docs, feature_vector=fv, _verbose=PRINT_ALL)
    print("Tested sklearn, RANSACRegressor...")


def test_sk_Ridge():
    mod = linear_model.Ridge()
    X, y = iris_data
    mod.fit(X, y)
    docs = {'name': "Ridge test"}
    fv = X[0, :]
    upload(mod, docs, feature_vector=fv, _verbose=PRINT_ALL)
    print("Tested sklearn, Ridge...")


def test_sk_RidgeCV():
    mod = linear_model.RidgeCV()
    X, y = iris_data
    mod.fit(X, y)
    docs = {'name': "RidgeCV test"}
    fv = X[0, :]
    upload(mod, docs, feature_vector=fv, _verbose=PRINT_ALL)
    print("Tested sklearn, RidgeCV...")


def test_sk_SGDClassifier():
    mod = linear_model.SGDClassifier()
    X, y = iris_data
    mod.fit(X, y)
    docs = {'name': "SGDClassifier test"}
    fv = X[0, :]
    upload(mod, docs, feature_vector=fv, _verbose=PRINT_ALL)
    print("Tested sklearn, SGDClassifier...")


def test_sk_SGDRegressor():
    mod = linear_model.SGDRegressor()
    X, y = iris_data
    mod.fit(X, y)
    docs = {'name': "SGDRegressor test"}
    fv = X[0, :]
    upload(mod, docs, feature_vector=fv, _verbose=PRINT_ALL)
    print("Tested sklearn, SGDRegressor...")


def test_sk_SVC():
    mod = svm.SVC()
    X, y = iris_data
    mod.fit(X, y)
    docs = {'name': "SVC test"}
    fv = X[0, :]
    upload(mod, docs, feature_vector=fv, _verbose=PRINT_ALL)
    print("Tested sklearn, SVC...")


def test_sk_SVR():
    mod = svm.SVR()
    X, y = iris_data
    mod.fit(X, y)
    docs = {'name': "SVR test"}
    fv = X[0, :]
    upload(mod, docs, feature_vector=fv, _verbose=PRINT_ALL)
    print("Tested sklearn, SVR...")


def test_sk_TheilSenRegressor():
    mod = linear_model.TheilSenRegressor()
    X, y = iris_data
    mod.fit(X, y)
    docs = {'name': "TheilSenRegressor test"}
    fv = X[0, :]
    upload(mod, docs, feature_vector=fv, _verbose=PRINT_ALL)
    print("Tested sklearn, TheilSenRegressor...")


# XGBoost package
def test_xg_XGBClassifier():
    mod = XGBClassifier()
    X, y = iris_data
    mod.fit(X, y)
    docs = {'name': "XGBClassifier test"}
    fv = X[0, :]
    upload(mod, docs, feature_vector=fv, _verbose=PRINT_ALL)
    print("Tested xgboost, XGBClassifier...")


def test_xg_XGBRegressor():
    mod = XGBRegressor()
    X, y = iris_data
    mod.fit(X, y)
    docs = {'name': "XGBRegressor test"}
    fv = X[0, :]
    upload(mod, docs, feature_vector=fv, _verbose=PRINT_ALL)
    print("Tested xgboost, XGBRegressor...")


def test_xg_XGBRFClassifier():
    mod = XGBRFClassifier()
    X, y = iris_data
    mod.fit(X, y)
    docs = {'name': "XGBRFClassifier test"}
    fv = X[0, :]
    upload(mod, docs, feature_vector=fv, _verbose=PRINT_ALL)
    print("Tested xgboost, XGBRFClassifier...")


def test_xg_XGBRFRegressor():
    mod = XGBRFRegressor()
    X, y = iris_data
    mod.fit(X, y)
    docs = {'name': "XGBRFXGBRFRegressorClassifier test"}
    fv = X[0, :]
    upload(mod, docs, feature_vector=fv, _verbose=PRINT_ALL)
    print("Tested xgboost, XGBRFRegressor...")


if __name__ == '__main__':

    if not RUN_TESTS:
        print("Not running tests.")
        exit()

    # Set correct endpoints
    _set_toolchain_URL(TOOLCHAIN_URL)
    _set_admin_URL(ADMIN_URL)

    print("Running tests off all supported models. This might take some time")
    print("===============================")

    print("# Statsmodels:")
    test_sm_OLS()
    test_sm_GLS()
    test_sm_WLS()
    #
    time.sleep(1)
    print("# SciKit Learn:")
    test_sk_ARDRegression()
    test_sk_DecisionTreeClassifier()
    test_sk_DecisionTreeRegressor()
    test_sk_ElasticNet()

    time.sleep(1)
    test_sk_ElasticNetCV()
    test_sk_ExtraTreeClassifier()
    test_sk_ExtraTreeRegressor()
    test_sk_ExtraTreesClassifier()
    test_sk_ExtraTreesRegressor()

    time.sleep(1)
    test_sk_HuberRegressor()
    test_sk_Lars()
    test_sk_LarsCV()
    test_sk_Lasso()
    test_sk_LassoCV()

    time.sleep(1)
    test_sk_LassoLars()
    test_sk_LassoLarsCV()
    test_sk_LassoLarsIC()
    test_sk_LinearRegression()
    test_sk_LinearSVC()

    time.sleep(1)
    test_sk_LinearSVR()
    test_sk_NuSCV()
    test_sk_NuSVR()
    test_sk_OrthogonalMatchingPursuit()
    test_sk_OrthogonalMatchingPursuitCV()

    time.sleep(1)
    test_sk_PassiveAggressiveClassifier()
    test_sk_PassiveAggressiveRegressor()
    test_sk_RandomForestClassifier()
    test_sk_RandomForestClassifier()
    test_sk_RANSACRegressor()

    time.sleep(1)
    test_sk_Ridge()
    test_sk_RidgeCV()
    test_sk_SGDClassifier()
    test_sk_SGDRegressor()
    test_sk_SVC()

    time.sleep(1)
    test_sk_SVR()
    test_sk_TheilSenRegressor()

    time.sleep(1)
    print("# XGBoost Learn:")
    test_xg_XGBRegressor()
    test_xg_XGBClassifier()
    test_xg_XGBRFClassifier()
    test_xg_XGBRFRegressor()

    print("===============================")
    print("All tests passed.")

    if TEAR_DOWN:
        endpoints = endpoints()
        # Loop with pause and remove...
        for key in endpoints:
            print('Delete: {}, cfid: {}.'.format(key['name'], key['cfid']))
            delete_endpoint(key['cfid'])
            time.sleep(.5)

    print("===============================")
    print("Done.")
