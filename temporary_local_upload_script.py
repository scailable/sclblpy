from sklearn import linear_model
from sclblpy import upload
from sklearn import datasets

PRINT_ALL = False
iris_data = datasets.load_iris(return_X_y=True)

mod = linear_model.RidgeClassifierCV()
X, y = iris_data
mod.fit(X, y)
docs = {'name': "LinearRegression test"}
fv = X[0, :]
upload(mod, docs, feature_vector=fv, _verbose=PRINT_ALL)
print("Tested sklearn, RidgeClassifierCV...")
