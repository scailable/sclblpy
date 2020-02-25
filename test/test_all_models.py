# Testing the upload function for all supported models.
# This might take a while..
# Note: these are first function tests, not extensive simulations of each type of model.
#    ... effectively they can be seen as "syntax" test.
import statsmodels.api as sm

from sklearn import datasets
from sklearn import linear_model
from sklearn import svm

from sclblpy import upload

# Verbose?
PRINT_ALL = False


# StatsModels
# https://www.statsmodels.org/stable/examples/index.html
def test_sm_ols():
    X, y = datasets.load_iris(return_X_y=True)
    mod = sm.OLS(y, X)
    mod.fit()
    docs = {'name': "OLS test"}
    fv = X[0, :]
    upload(mod, docs, feature_vector=fv, _verbose=PRINT_ALL)
    print("Tested SM, OLS...")


def test_sm_gls():
    data = sm.datasets.longley.load(as_pandas=False)
    X = sm.add_constant(data.exog)
    mod = sm.GLS(data.endog, X, sigma=1)
    mod.fit()
    docs = {'name': "GLS test"}
    fv = X[0, :]
    upload(mod, docs, feature_vector=fv, _verbose=PRINT_ALL)
    print("Tested SM, GLS...")


def test_sm_wls():
    Y = [1, 3, 4, 5, 2, 3, 4]
    X = range(1, 8)
    X = sm.add_constant(X)
    mod = sm.WLS(Y, X, weights=list(range(1, 8)))
    mod.fit()
    docs = {'name': "WLS test"}
    fv = X[0, :]
    upload(mod, docs, feature_vector=fv, _verbose=PRINT_ALL)
    print("Tested SM, WLS...")


# Sklearn
def test_sk_ardregression():
    mod = linear_model.ARDRegression()
    X, y = datasets.load_iris(return_X_y=True)
    mod.fit(X, y)
    docs = {'name': "ARDRegression test"}
    fv = X[0, :]
    upload(mod, docs, feature_vector=fv, _verbose=PRINT_ALL)
    print("Tested sklearn, ARDRegression...")


def test_sk_bayesianridge():
    mod = linear_model.BayesianRidge()
    X, y = datasets.load_iris(return_X_y=True)
    mod.fit(X, y)
    docs = {'name': "BayesianRidge test"}
    fv = X[0, :]
    upload(mod, docs, feature_vector=fv, _verbose=PRINT_ALL)
    print("Tested sklearn, BayesianRidge...")


# tree.DecisionTreeClassifier
# tree.DecisionTreeRegressor
# linear_model.ElasticNet
# linear_model.ElasticNetCV
# tree.ExtraTreeClassifier
# tree.ExtraTreeRegressor
# ensemble.ExtraTreesClassifier
# ensemble.ExtraTreesRegressor
# linear_model.HuberRegression
# linear_model.Lars
# linear_model.LarsCV
# linear_model.Lasso
# linear_model.LassoCV
# linear_model.LassoLars
# linear_model.LassoLarsCV
# linear_model.LassoLarsIC
# linear_model.LinearRegression
# svm.LinearSVC
# svm.LinearSVR
# svm.NuSCV
# svm.NuSVR
# linear_model.OrthogonalMatchingPursuit
# linear_model.OrthogonalMatchingPursuitCV
# linear_model.PassiveAggressiveClassifier
# linear_model.PassiveAggressiveRegressor
# ensemble.RandomForestClassifier
# ensemble.RandomForestRegressor
# linear_model.RANSACRegressor
# linear_model.Ridge
# linear_model.RidgeCV
# linear_model.SGDClassifier
# linear_model.SGDRegressor


def test_sk_svc():
    mod = svm.SVC()
    X, y = datasets.load_iris(return_X_y=True)
    mod.fit(X, y)
    docs = {'name': "SVC test"}
    fv = X[0, :]
    upload(mod, docs, feature_vector=fv, _verbose=PRINT_ALL)
    print("Tested sklearn, SVC...")

# svm.SVR
# linear_model.TheilSenRegressor
# tree.XGBClassifier
# tree.XGBRegressor
# tree.XGBRFClassifier
# tree.XGBRFRegressor




if __name__ == '__main__':
    print("Running tests off all supported models. This might take some time")
    print("===============================")

    print("# Statsmodels:")
    test_sm_ols()
    test_sm_gls()
    test_sm_wls()

    print("# SciKit Learn:")
    test_sk_ardregression()
    test_sk_bayesianridge()
    test_sk_svc()

    print("===============================")
    print("All tests passed.")