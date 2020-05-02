# Testing the upload function for all supported models.
# This might take a while..
import time
import statsmodels.api as sm
import lightgbm as lgb
# import lightning as ln

from sklearn import datasets
from sklearn import linear_model
from sklearn import tree
from sklearn import ensemble
from sklearn import svm

from xgboost import XGBClassifier
from xgboost import XGBRegressor
from xgboost import XGBRFClassifier
from xgboost import XGBRFRegressor

import numpy as np

from sclblpy import upload, _set_toolchain_URL, _set_usermanager_URL
from sclblpy import endpoints
from sclblpy import delete_endpoint

# Script settings:
from sclblpy._utils import _get_model_package, _get_model_name, _model_is_fitted
from sclblpy.main import _toggle_debug_mode, stop_print

RUN_TESTS = False  # Prevent unintended testing
DEBUG = True  # Set to debug mode; if true it will raise exceptions
PRINTING = True  # Toggle printing on and off.
TEAR_DOWN = False  # Remove all endpoints after running tests (you will be prompted)?
ADMIN_URL = "http://localhost:8008"  # Location of admin for this test
TOOLCHAIN_URL = "http://localhost:8010"  # Location of toolchain for this test
SLEEPTIME = 5  # Time in between blocks of models.


iris_data = datasets.load_iris(return_X_y=True)


# StatsModels
def test_sm_GLS():
    print("Testing SM, GLS...")
    data = sm.datasets.longley.load(as_pandas=False)
    X = sm.add_constant(data.exog)
    est = sm.GLS(data.endog, X, sigma=1)
    mod = est.fit()
    docs = {'name': "GLS test"}
    fv = X[0, :]
    upload(mod, fv, docs)


def test_sm_GLSAR():
    print("Testing SM, GLSAR...")
    X, y = iris_data
    est = sm.GLS(y, X, rho=2)
    mod = est.fit()
    docs = {'name': "GLSAR test"}
    fv = X[0, :]
    upload(mod, fv, docs)


def test_sm_OLS():
    print("Testing SM, OLS...")
    X, y = iris_data
    est = sm.OLS(y, X)
    mod = est.fit()
    docs = {'name': "OLS test"}
    fv = X[0, :]
    upload(mod, fv, docs=docs)


# def test_sm_ProcessMLE():
#     print("Testing SM, ProcessMLE...")
#     X, y = iris_data
#     est = sm.ProcessMLE(y, X)
#     mod = est.fit()
#     docs = {'name': "ProcessMLE test"}
#     fv = X[0, :]
#     upload(mod, fv, docs=docs)


def test_sm_QuantReg():
    print("Testing SM, QuantReg...")
    X, y = iris_data
    est = sm.QuantReg(y, X)
    mod = est.fit()
    docs = {'name': "QuantReg test"}
    fv = X[0, :]
    upload(mod, fv, docs=docs)


def test_sm_WLS():
    print("Testing SM, WLS...")
    Y = [1, 3, 4, 5, 2, 3, 4]
    X = range(1, 8)
    X = sm.add_constant(X)
    est = sm.WLS(Y, X, weights=list(range(1, 8)))
    mod = est.fit()
    docs = {'name': "WLS test"}
    fv = X[0, :]
    upload(mod, fv, docs)


# Sklearn
def test_sk_ARDRegression():
    print("Testing sklearn, ARDRegression...")
    mod = linear_model.ARDRegression()
    X, y = iris_data
    mod.fit(X, y)
    docs = {'name': "ARDRegression test"}
    fv = X[0, :]
    upload(mod, fv, docs)


def test_sk_BayesianRidge():
    print("Testing sklearn, BayesianRidge...")
    mod = linear_model.BayesianRidge()
    X, y = iris_data
    mod.fit(X, y)
    docs = {'name': "BayesianRidge test"}
    fv = X[0, :]
    upload(mod, fv, docs)


def test_sk_DecisionTreeClassifier():
    print("Testing sklearn, DecisionTreeClassifier...")
    mod = tree.DecisionTreeClassifier()
    X, y = iris_data
    mod.fit(X, y)
    docs = {'name': "DecisionTreeClassifier test"}
    fv = X[0, :]
    upload(mod, fv, docs)


def test_sk_DecisionTreeRegressor():
    print("Testing sklearn, DecisionTreeRegressor...")
    mod = tree.DecisionTreeRegressor()
    X, y = iris_data
    mod.fit(X, y)
    docs = {'name': "DecisionTreeClassifier test"}
    fv = X[0, :]
    upload(mod, fv, docs)


def test_sk_ElasticNet():
    print("Testing sklearn, ElasticNet...")
    mod = linear_model.ElasticNet()
    X, y = iris_data
    mod.fit(X, y)
    docs = {'name': "ElasticNet test"}
    fv = X[0, :]
    upload(mod, fv, docs)


def test_sk_ElasticNetCV():
    print("Testing sklearn, ElasticNetCV...")
    mod = linear_model.ElasticNetCV()
    X, y = iris_data
    mod.fit(X, y)
    docs = {'name': "ElasticNetCV test"}
    fv = X[0, :]
    upload(mod, fv, docs)


def test_sk_ExtraTreeClassifier():
    print("Testing sklearn, ExtraTreeClassifier...")
    mod = tree.ExtraTreeClassifier()
    X, y = iris_data
    mod.fit(X, y)
    docs = {'name': "ExtraTreeClassifier test"}
    fv = X[0, :]
    upload(mod, fv, docs)


def test_sk_ExtraTreeRegressor():
    print("Testing sklearn, ExtraTreeRegressor...")
    mod = tree.ExtraTreeRegressor()
    X, y = iris_data
    mod.fit(X, y)
    docs = {'name': "ExtraTreeRegressor test"}
    fv = X[0, :]
    upload(mod, fv, docs)


def test_sk_ExtraTreesClassifier():
    print("Testing sklearn, Ensemble ExtraTreeClassifier...")
    mod = ensemble.ExtraTreesClassifier()
    X, y = iris_data
    mod.fit(X, y)
    docs = {'name': "ExtraTreeClassifier test"}
    fv = X[0, :]
    upload(mod, fv, docs)


def test_sk_ExtraTreesRegressor():
    print("Testing sklearn, Ensemble ExtraTreeRegressor...")
    mod = ensemble.ExtraTreesRegressor()
    X, y = iris_data
    mod.fit(X, y)
    docs = {'name': "ExtraTreeRegressor test"}
    fv = X[0, :]
    upload(mod, fv, docs)


def test_sk_HuberRegressor():
    print("Testing sklearn, HuberRegressor...")
    mod = linear_model.HuberRegressor()
    X, y = iris_data
    mod.fit(X, y)
    docs = {'name': "HuberRegressor test"}
    fv = X[0, :]
    upload(mod, fv, docs)


def test_sk_Lars():
    print("Testing sklearn, Lars...")
    mod = linear_model.Lars()
    X, y = iris_data
    mod.fit(X, y)
    docs = {'name': "Lars test"}
    fv = X[0, :]
    upload(mod, fv, docs)


def test_sk_LarsCV():
    print("Testomg sklearn, LarsCV...")
    mod = linear_model.LarsCV()
    X, y = iris_data
    mod.fit(X, y)
    docs = {'name': "LarsCV test"}
    fv = X[0, :]
    upload(mod, fv, docs)


def test_sk_Lasso():
    print("Testing sklearn, Lasso...")
    mod = linear_model.Lasso()
    X, y = iris_data
    mod.fit(X, y)
    docs = {'name': "Lasso test"}
    fv = X[0, :]
    upload(mod, fv, docs)


def test_sk_LassoCV():
    print("Testing sklearn, LassoCV...")
    mod = linear_model.LassoCV()
    X, y = iris_data
    mod.fit(X, y)
    docs = {'name': "LassoCV test"}
    fv = X[0, :]
    upload(mod, fv, docs)


def test_sk_LassoLars():
    print("Testing sklearn, LassoLars...")
    mod = linear_model.LassoLars()
    X, y = iris_data
    mod.fit(X, y)
    docs = {'name': "LassoLars test"}
    fv = X[0, :]
    upload(mod, fv, docs)


def test_sk_LassoLarsCV():
    print("Testing sklearn, LassoLarsCV...")
    mod = linear_model.LassoLarsCV()
    X, y = iris_data
    mod.fit(X, y)
    docs = {'name': "LassoLarsCV test"}
    fv = X[0, :]
    upload(mod, fv, docs)


def test_sk_LassoLarsIC():
    print("Testing sklearn, LassoLarsIC...")
    mod = linear_model.LassoLarsIC()
    X, y = iris_data
    mod.fit(X, y)
    docs = {'name': "LassoLarsIC test"}
    fv = X[0, :]
    upload(mod, fv, docs)


def test_sk_LinearRegression():
    print("Testing sklearn, LinearRegression...")
    mod = linear_model.LinearRegression()
    X, y = iris_data
    mod.fit(X, y)
    docs = {'name': "LinearRegression test"}
    fv = X[0, :]
    upload(mod, fv, docs)


def test_sk_LinearSVC():
    print("Testing sklearn, LinearSVC...")
    mod = svm.LinearSVC(max_iter=10000)  # Needs more iterations to converge
    X, y = iris_data
    mod.fit(X, y)
    docs = {'name': "LinearSVC test"}
    fv = X[0, :]
    upload(mod, fv, docs)



def test_sk_LinearSVR():
    print("Testing sklearn, LinearSVR...")
    mod = svm.LinearSVR()
    X, y = iris_data
    mod.fit(X, y)
    docs = {'name': "LinearSVR test"}
    fv = X[0, :]
    upload(mod, fv, docs)


def test_sk_LogisticRegression():
    print("Testing sklearn, LogisticRegression...")
    mod = linear_model.LogisticRegression(max_iter=1000)
    X, y = iris_data
    ybin = np.where(y <= 1, 0, 1)
    mod.fit(X, ybin)
    docs = {'name': "LogisticRegression test"}
    fv = X[0, :]
    upload(mod, fv, docs)


def test_sk_LogisticRegressionCV():
    print("Testing sklearn, LogisticRegressionCV...")
    mod = linear_model.LogisticRegressionCV(max_iter=1000)
    X, y = iris_data
    ybin = np.where(y <= 1, 0, 1)
    mod.fit(X, ybin)
    docs = {'name': "LogisticRegressionCV test"}
    fv = X[0, :]
    upload(mod, fv, docs)


def test_sk_NuSCV():
    print("Testing sklearn, NuSCV...")
    mod = svm.NuSVC()
    X, y = iris_data
    mod.fit(X, y)
    docs = {'name': "NuSCV test"}
    fv = X[0, :]
    upload(mod, fv, docs)


def test_sk_NuSVR():
    print("Testing sklearn, NuSVR...")
    mod = svm.NuSVR()
    X, y = iris_data
    mod.fit(X, y)
    docs = {'name': "NuSVR test"}
    fv = X[0, :]
    upload(mod, fv, docs)


def test_sk_OrthogonalMatchingPursuit():
    print("Testing sklearn, OrthogonalMatchingPursuit...")
    mod = linear_model.OrthogonalMatchingPursuit()
    X, y = iris_data
    mod.fit(X, y)
    docs = {'name': "OrthogonalMatchingPursuit test"}
    fv = X[0, :]
    upload(mod, fv, docs)


def test_sk_OrthogonalMatchingPursuitCV():
    print("Testing sklearn, OrthogonalMatchingPursuitCV...")
    mod = linear_model.OrthogonalMatchingPursuitCV()
    X, y = iris_data
    mod.fit(X, y)
    docs = {'name': "OrthogonalMatchingPursuitCV test"}
    fv = X[0, :]
    upload(mod, fv, docs)


def test_sk_PassiveAggressiveClassifier():
    print("Testing sklearn, PassiveAggressiveClassifier...")
    mod = linear_model.PassiveAggressiveClassifier()
    X, y = iris_data
    mod.fit(X, y)
    docs = {'name': "PassiveAggressiveClassifier test"}
    fv = X[0, :]
    upload(mod, fv, docs)


def test_sk_PassiveAggressiveRegressor():
    print("Testing sklearn, PassiveAggressiveRegressor...")
    mod = linear_model.PassiveAggressiveRegressor()
    X, y = iris_data
    mod.fit(X, y)
    docs = {'name': "PassiveAggressiveRegressor test"}
    fv = X[0, :]
    upload(mod, fv, docs)


def test_sk_Perceptron():
    print("Testing sklearn, Perceptron...")
    mod = linear_model.Perceptron()
    X, y = iris_data
    mod.fit(X, y)
    docs = {'name': "Perceptron test"}
    fv = X[0, :]
    upload(mod, fv, docs)


def test_sk_RandomForestClassifier():
    print("Testing sklearn, RandomForestClassifier...")
    mod = ensemble.RandomForestClassifier()
    X, y = iris_data
    mod.fit(X, y)
    docs = {'name': "RandomForestClassifier test"}
    fv = X[0, :]
    upload(mod, fv, docs)


def test_sk_RandomForestRegressor():
    print("Testing sklearn, RandomForestRegressor...")
    mod = ensemble.RandomForestRegressor()
    X, y = iris_data
    mod.fit(X, y)
    docs = {'name': "RandomForestRegressor test"}
    fv = X[0, :]
    upload(mod, fv, docs)


def test_sk_RANSACRegressor():
    print("Testing sklearn, RANSACRegressor...")
    mod = linear_model.RANSACRegressor()
    X, y = iris_data
    mod.fit(X, y)
    docs = {'name': "RANSACRegressor test"}
    fv = X[0, :]
    upload(mod, fv, docs)


def test_sk_Ridge():
    print("Testing sklearn, Ridge...")
    mod = linear_model.Ridge()
    X, y = iris_data
    mod.fit(X, y)
    docs = {'name': "Ridge test"}
    fv = X[0, :]
    upload(mod, fv, docs)

def test_sk_RidgeClassifier():
    print("Testing sklearn, RidgeClassifier...")
    mod = linear_model.RidgeClassifier()
    X, y = iris_data
    mod.fit(X, y)
    docs = {'name': "RidgeClassifier test"}
    fv = X[0, :]
    upload(mod, fv, docs)


def test_sk_RidgeClassifierCV():
    print("Testing sklearn, RidgeClassifierCV...")
    mod = linear_model.RidgeClassifierCV()
    X, y = iris_data
    mod.fit(X, y)
    docs = {'name': "RidgeClassifierCV test"}
    fv = X[0, :]
    upload(mod, fv, docs)


def test_sk_RidgeCV():
    mod = linear_model.RidgeCV()
    X, y = iris_data
    mod.fit(X, y)
    docs = {'name': "RidgeCV test"}
    fv = X[0, :]
    upload(mod, fv, docs)
    print("Tested sklearn, RidgeCV...")


def test_sk_SGDClassifier():
    mod = linear_model.SGDClassifier()
    X, y = iris_data
    mod.fit(X, y)
    docs = {'name': "SGDClassifier test"}
    fv = X[0, :]
    upload(mod, fv, docs)
    print("Tested sklearn, SGDClassifier...")


def test_sk_SGDRegressor():
    mod = linear_model.SGDRegressor()
    X, y = iris_data
    mod.fit(X, y)
    docs = {'name': "SGDRegressor test"}
    fv = X[0, :]
    upload(mod, fv, docs)
    print("Tested sklearn, SGDRegressor...")


def test_sk_SVC():
    mod = svm.SVC()
    X, y = iris_data
    mod.fit(X, y)
    docs = {'name': "SVC test"}
    fv = X[0, :]
    upload(mod, fv, docs)
    print("Tested sklearn, SVC...")


def test_sk_SVR():
    mod = svm.SVR()
    X, y = iris_data
    mod.fit(X, y)
    docs = {'name': "SVR test"}
    fv = X[0, :]
    upload(mod, fv, docs)
    print("Tested sklearn, SVR...")


def test_sk_TheilSenRegressor():
    mod = linear_model.TheilSenRegressor()
    X, y = iris_data
    mod.fit(X, y)
    docs = {'name': "TheilSenRegressor test"}
    fv = X[0, :]
    upload(mod, fv, docs)
    print("Tested sklearn, TheilSenRegressor...")


# XGBoost package
def test_xg_XGBClassifier():
    print("Testing xgboost, XGBClassifier...")
    mod = XGBClassifier()
    X, y = iris_data
    mod.fit(X, y)
    docs = {'name': "XGBClassifier test"}
    fv = X[0, :]
    upload(mod, fv, docs)


def test_xg_XGBRegressor():
    print("Testing xgboost, XGBRegressor...")
    mod = XGBRegressor()
    X, y = iris_data
    mod.fit(X, y)
    docs = {'name': "XGBRegressor test"}
    fv = X[0, :]
    upload(mod, fv, docs)


def test_xg_XGBRFClassifier():
    print("Testing xgboost, XGBRFClassifier...")
    # Note, only works with binary outcomes!
    mod = XGBRFClassifier()
    X, y = iris_data
    ybin = np.where(y <= 1, 0, 1)
    mod.fit(X, ybin)
    docs = {'name': "XGBRFClassifier test"}
    fv = X[0, :]
    upload(mod, fv, docs)


def test_xg_XGBRFRegressor():
    print("Testing xgboost, XGBRFRegressor...")
    mod = XGBRFRegressor()
    X, y = iris_data
    mod.fit(X, y)
    docs = {'name': "XGBRFRegressor test"}
    fv = X[0, :]
    upload(mod, fv, docs)


# lightgbm package
def test_lgb_LGBMClassifier():
    print("Testing lightgbm, LGBMClassifier...")
    mod = lgb.LGBMClassifier()
    X, y = iris_data
    mod.fit(X, y)
    docs = {'name': "LGBMClassifier test"}
    fv = X[0, :]
    upload(mod, fv, docs)


def test_lgb_LGBMRegressor():
    print("Testing lightgbm, LGBMRegressor...")
    mod = lgb.LGBMRegressor()
    X, y = iris_data
    mod.fit(X, y)
    docs = {'name': "LGBMRegressor test"}
    fv = X[0, :]
    upload(mod, fv, docs)


# lightning
def test_lgb_AdaGradClassifier():
    print("Testing lightning, AdaGradClassifier...")
    mod = lgb.AdaGradClassifier()
    X, y = iris_data
    mod.fit(X, y)
    docs = {'name': "AdaGradClassifier test"}
    fv = X[0, :]
    upload(mod, fv, docs)


def test_lgb_AdaGradRegressor():
    print("Testing lightning, AdaGradRegressor...")
    mod = lgb.AdaGradRegressor()
    X, y = iris_data
    mod.fit(X, y)
    docs = {'name': "AdaGradRegressor test"}
    fv = X[0, :]
    upload(mod, fv, docs)


def test_lgb_CDClassifier():
    print("Testing lightning, CDClassifier...")
    mod = lgb.CDClassifier()
    X, y = iris_data
    mod.fit(X, y)
    docs = {'name': "CDClassifier test"}
    fv = X[0, :]
    upload(mod, fv, docs)


def test_lgb_CDRegressor():
    print("Testing lightning, CDRegressor...")
    mod = lgb.CDRegressor()
    X, y = iris_data
    mod.fit(X, y)
    docs = {'name': "CDRegressor test"}
    fv = X[0, :]
    upload(mod, fv, docs)


def test_lgb_FistaClassifier():
    print("Testing lightning, FistaClassifier...")
    mod = lgb.FistaClassifier()
    X, y = iris_data
    mod.fit(X, y)
    docs = {'name': "FistaClassifier test"}
    fv = X[0, :]
    upload(mod, fv, docs)


def test_lgb_FistaRegressor():
    print("Testing lightning, FistaRegressor...")
    mod = lgb.FistaRegressor()
    X, y = iris_data
    mod.fit(X, y)
    docs = {'name': "FistaRegressor test"}
    fv = X[0, :]
    upload(mod, fv, docs)


# lightning (not supported
def test_lgb_KernelSVC():
    print("Testing lightning, KernelSVC...")
    mod = ln.KernelSVC()
    X, y = iris_data
    mod.fit(X, y)
    docs = {'name': "KernelSVC test"}
    fv = X[0, :]
    upload(mod, fv, docs)

def test_lgb_SAGAClassifier():
    print("Testing lightning, SAGAClassifier...")
    mod = lgb.SAGAClassifier()
    X, y = iris_data
    mod.fit(X, y)
    docs = {'name': "SAGAClassifier test"}
    fv = X[0, :]
    upload(mod, fv, docs)


def test_lgb_SAGARegressor():
    print("Testing lightgbm, SAGARegressor...")
    mod = lgb.SAGARegressor()
    X, y = iris_data
    mod.fit(X, y)
    docs = {'name': "SAGARegressor test"}
    fv = X[0, :]
    upload(mod, fv, docs)


def test_lgb_SAGClassifier():
    print("Testing lightning, SAGClassifier...")
    mod = lgb.SAGClassifier()
    X, y = iris_data
    mod.fit(X, y)
    docs = {'name': "SAGClassifier test"}
    fv = X[0, :]
    upload(mod, fv, docs)


def test_lgb_SAGRegressor():
    print("Testing lightning, SAGRegressor...")
    mod = lgb.SAGRegressor()
    X, y = iris_data
    mod.fit(X, y)
    docs = {'name': "SAGRegressor test"}
    fv = X[0, :]
    upload(mod, fv, docs)


def test_lgb_SDCAClassifier():
    print("Testing lightgbm, SDCAClassifier...")
    mod = lgb.SDCAClassifier()
    X, y = iris_data
    mod.fit(X, y)
    docs = {'name': "SDCAClassifier test"}
    fv = X[0, :]
    upload(mod, fv, docs)


def test_lgb_SDCARegressor():
    print("Testing lightning, SDCARegressor...")
    mod = lgb.SDCAClassifier()
    X, y = iris_data
    mod.fit(X, y)
    docs = {'name': "SDCARegressor test"}
    fv = X[0, :]
    upload(mod, fv, docs)





if __name__ == '__main__':

    if not RUN_TESTS:
        print("Not running tests.")
        exit()

    if not PRINTING:
        stop_print()

    if DEBUG:
        _toggle_debug_mode()

    # Remove:
    # remove_credentials()

    # Set correct endpoints
    _set_toolchain_URL(TOOLCHAIN_URL)
    _set_usermanager_URL(ADMIN_URL)

    print("Running tests off all supported models. This might take some time")
    print("===============================")

    print("# Statsmodels:")
    test_sm_GLS()
    test_sm_GLSAR()
    test_sm_OLS()
    test_sm_QuantReg()
    test_sm_WLS()

    # time.sleep(SLEEPTIME)
    print("# SciKit Learn:")
    test_sk_ARDRegression()
    test_sk_BayesianRidge()
    test_sk_DecisionTreeClassifier()
    test_sk_DecisionTreeRegressor()
    test_sk_ElasticNet()

    time.sleep(SLEEPTIME)
    test_sk_ElasticNetCV()
    test_sk_ExtraTreeClassifier()
    test_sk_ExtraTreeRegressor()
    test_sk_ExtraTreesClassifier()
    test_sk_ExtraTreesRegressor()

    time.sleep(SLEEPTIME)
    test_sk_HuberRegressor()
    test_sk_Lars()
    test_sk_LarsCV()
    test_sk_Lasso()
    test_sk_LassoCV()

    time.sleep(SLEEPTIME)
    test_sk_LassoLars()
    test_sk_LassoLarsCV()
    test_sk_LassoLarsIC()
    test_sk_LinearRegression()
    test_sk_LinearSVC()

    time.sleep(SLEEPTIME)
    test_sk_LinearSVR()
    test_sk_LogisticRegression()
    test_sk_LogisticRegressionCV()
    test_sk_NuSCV()
    test_sk_NuSVR()
    test_sk_OrthogonalMatchingPursuit()
    test_sk_OrthogonalMatchingPursuitCV()

    time.sleep(SLEEPTIME)
    test_sk_PassiveAggressiveClassifier()
    test_sk_PassiveAggressiveRegressor()
    test_sk_Perceptron()
    test_sk_RandomForestClassifier()
    test_sk_RandomForestRegressor()
    test_sk_RANSACRegressor()

    time.sleep(SLEEPTIME)
    test_sk_Ridge()
    test_sk_RidgeCV()
    test_sk_RidgeClassifier()
    test_sk_RidgeClassifierCV()
    test_sk_SGDClassifier()

    time.sleep(SLEEPTIME)
    test_sk_SGDRegressor()
    test_sk_SVC()
    test_sk_SVR()
    test_sk_TheilSenRegressor()

    time.sleep(SLEEPTIME)
    print("# XGBoost:")
    test_xg_XGBRegressor()
    test_xg_XGBClassifier()
    test_xg_XGBRFClassifier()
    test_xg_XGBRFRegressor()

    time.sleep(SLEEPTIME)
    print("# lightgbm:")
    test_lgb_LGBMClassifier()
    test_lgb_LGBMRegressor()

    if False:  # Lightning not supported.
        time.sleep(SLEEPTIME)

        # Add to supported_models.json
        # "lightning": [
        #     "AdaGradClassifier",
        #     "AdaGradRegressor",
        #     "CDClassifier",
        #     "CDRegressor",
        #     "FistaClassifier",
        #     "FistaRegressor",
        #     "KernelSVC",
        #     "LGBMClassifier",
        #     "LGBMRegressor",
        #     "SAGAClassifier",
        #     "SAGARegressor",
        #     "SAGClassifier",
        #     "SAGRegressor",
        #     "SDCAClassifier",
        #     "SDCARegressor"
        # ]

        print("# lightning:")
        test_lgb_AdaGradClassifier()
        test_lgb_AdaGradRegressor()
        test_lgb_CDClassifier()
        test_lgb_CDRegressor()
        test_lgb_FistaClassifier()
        test_lgb_FistaRegressor()
        test_lgb_KernelSVC()
        test_lgb_SAGAClassifier()
        test_lgb_SAGARegressor()
        test_lgb_SAGClassifier()
        test_lgb_SAGRegressor()
        test_lgb_SDCAClassifier()
        test_lgb_SDCARegressor()


    print("===============================")
    print("All tests passed.")

    if TEAR_DOWN:

        while True:
            query = input('Are you sure you would like to remove all endpoints? (y/n) ')
            answ = query[0].lower()
            if query == '' or not answ in ['y', 'n']:
                print('Please answer with yes or no')
            else:
                break

        if answ == 'y':
            endpoints = endpoints()
            # Loop with pause and remove...
            for key in endpoints:
                print('Delete: {}, cfid: {}.'.format(key['name'], key['cfid']))
                delete_endpoint(key['cfid'])
                time.sleep(.5)

    print("===============================")
    print("Done.")
