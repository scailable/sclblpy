from sklearn import linear_model
from sclblpy import upload
from sklearn import datasets
import statsmodels.api as sm
import m2cgen

PRINT_ALL = False
iris_data = datasets.load_iris(return_X_y=True)

##########################

mod = linear_model.RidgeClassifierCV()
X, y = iris_data
mod.fit(X, y)
docs = {'name': "RidgeClassifier test"}
fv = X[0, :]
upload(mod, docs, feature_vector=fv, _verbose=PRINT_ALL)
print("Tested sklearn, RidgeClassifierCV...")

##########################

mod = linear_model.BayesianRidge()
X, y = iris_data
mod.fit(X, y)
docs = {'name': "BayesianRidge test"}
fv = X[0, :]
upload(mod, docs, feature_vector=fv, _verbose=PRINT_ALL)
print("Tested sklearn, BayesianRidge...")

##########################

iris = datasets.load_iris()
X = iris.data[:, 0:2]  # we only take the first two features for visualization
y = iris.target

mod = linear_model.LogisticRegression(C=1e5)

# Create an instance of Logistic Regression Classifier and fit the data.
mod.fit(X, y)

docs = {'name': "LogisticRegression test"}
fv = X[0, :]
upload(mod, docs, feature_vector=fv, _verbose=PRINT_ALL)
print("Tested sklearn, LogisticRegression...")

#######################################################

X, y = iris_data
estimator = sm.OLS(y, X)
mod = estimator.fit()
docs = {'name': "OLS test"}
fv = X[0, :]
upload(mod, docs, feature_vector=fv, _verbose=PRINT_ALL)
print("Tested SM, OLS...")


########################################################


from xgboost import XGBRegressor

mod = XGBRegressor()
X, y = iris_data
mod.fit(X[:120], y[:120])

docs = {'name': "XGBRegressor test"}
fv = X[0, :]
upload(mod, docs, feature_vector=fv, _verbose=PRINT_ALL)
print("Tested xgboost, XGBRegressor...")

