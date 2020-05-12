# sclblpy

[![PyPI Release](https://github.com/scailable/sclblpy/workflows/PyPI%20Release/badge.svg)](https://pypi.org/project/sclblpy/)

sclblpy is the core python package provided by Scailable to convert models fit in python to WebAssembly and
open them up as a REST endpoint. 

sclblpy is only functional in combination with a valid Scailable user account.

- **Website:** [https://www.scailable.net](https://www.scailable.net)
- **Docs:** [https://docs.sclbl.net/sclblpy](https://docs.sclbl.net/sclblpy)
- **Get an account:** [https://admin.sclbl.net](https://admin.sclbl.net/signup.html)
- **Source:** [https://github.com/scailable/sclblpy/](https://github.com/scailable/sclblpy/)
- **Getting started:** [https://github.com/scailable/sclbl-tutorials/tree/master/sclbl-101-getting-started](https://github.com/scailable/sclbl-tutorials/tree/master/sclbl-101-getting-started)

## Background
The sclblpy package allows users with a valid scailable account (see [https://admin.sclbl.net](https://admin.sclbl.net))
to upload fitted ML / AI models to the Scailable toolchain server. This will result in:

1. The model being tested on the client side.
2. The model being uploaded to Scailable, tested again, and if all test pass it will be converted to [WebAssembly](https://webassembly.org).
3. The model being made available as an easy to access REST endpoint.

## Getting started
After installing the package using `pip install sclblpy` you can easily fit a ML / AI model using your preferred tools and
upload it to our toolchains. The following code block provides a simple example:

````
# Neccesary imports:
import sclblpy as sp

from sklearn import svm
from sklearn import datasets

# Start fitting a simple model:
clf = svm.SVC()
X, y = datasets.load_iris(return_X_y=True)
clf.fit(X, y)

# Create an example feature vector (required):
row = X[130, :]

# Create documentation (optional, but useful):
docs = {}
docs['name'] = "My first fitted model"
docs['documentation'] = "Any documentation you would like to provide."

# Upload the model:
sp.upload(clf, row, docs=docs)
````

The call to `sp.upload()` will upload the fitted model, after running a number of local tests, to the 
Scailable toolchain server and create an associated REST endpoint. Limited user feedback will be printed to show progress,
and you will receive an email at the email address associated with your account when the conversion is fully completed (which might take a few minutes).
This email also contains further details regarding the usage of your created endpoint.

Note that upon first upload you will be prompted to provide your Scailable username and password; you can choose to
store the provided credentials locally to enable easy login on subsequently uploads. (users can signup for an account at
 [https://admin.sclbl.net](https://admin.sclbl.net/signup.html)).
 
## Examples
> These examples are merely intended to show the desired syntax for the various packages; we do not intend to fit models
> that actually have a good predictive performance in these examples.

Currently we support uploading `sklearn`, `statsmodels`, and `xgboost` models (run `sp.list_models()` to print an overview of all supported models). 
Here we provide an example for each of these.

### sklearn: the elastic net

The [elastic net](https://web.stanford.edu/~hastie/Papers/elasticnet.pdf) provides a flexible regularized model that is 
useful for many supervised learning tasks.

````
import sclblpy as sp
from sklearn import linear_model  # Import linear_model
from sklearn import datasets  # Import sklearn datasets

iris_data = datasets.load_iris(return_X_y=True)
X, y = iris_data

mod = linear_model.ElasticNet()  # Instantiate the model

mod.fit(X, y)  # Fit the model

fv = X[0, :]  # An example feature vector
docs = {'name': "ElasticNet example model", 'documentation' : "Documentation for this model."}

sp.upload(mod, fv, docs)

````

### statsmodels: OLS regression

The statsmodels package provides a number of regression models with flexible error functions. We provide a simple OLS
example:

```` 
import sclblpy as sp

import statsmodels.api as sm  # Import statsmodels
from sklearn import datasets  # Import sklearn datasets

iris_data = datasets.load_iris(return_X_y=True)
X, y = iris_data

est = sm.OLS(y, X)  # Specify the model
mod = est.fit()  # Fit the model; note that we send the fitted model to scailable

fv = X[0, :]  # An example feature vector
docs = {'name': "OLS example model"}

sp.upload(mod, fv, docs=docs)
````

### xgboost: tree boosting

The xgboost package provides flexibly tree boosting models (see [xgboost](https://dl.acm.org/doi/abs/10.1145/2939672.2939785)).
This model often performs very well "off the shelf" for many supervised learning tasks.

```` 
import sclblpy as sp

from xgboost import XGBClassifier  # Import xgboost classifier
from sklearn import datasets  # Import sklearn datasets

iris_data = datasets.load_iris(return_X_y=True)
X, y = iris_data

mod = XGBClassifier()  # Instantiate the model
mod.fit(X, y)  # Fit the model

fv = X[0, :]  # An example feature vector
docs = {'name': "XGBoost example model"}

sp.upload(mod, fv, docs=docs)
````

## Additional functionality
Next to the main ``upload()`` function, the package also exposes the following functions to administer endpoints:

````
# List all endpoints owned by the current user:
sp.endpoints()

# Remove an endpoint:
sp.delete_endpoint(cfid)  # Where cfid is the compute function id

# Update an existing endpoint:
sp.update(mod, fv, cfid, docs)  # Where cfid is the compute function id

# Update an existing ednpoint without updating the docs:
sp.update(mod, fv, cfid) 

# Update only the docs of an existing endpoint:
sp.update_docs(cfid, docs)
````

Additionally, the following methods are available:

````
# List all models currently supported by our toolchains:
sp.list_models()  

# Prevent any user feedback from being printed:
sp.stop_print()  

# Turn user feedback back on:
sp.start_print()  

# Remove locally stored user credentials:
sp.remove_credentials()

````

## Running an uploaded model
After uploading a model to Scailable using the `sclblpy` package, you might also
want to use `python` to consume the model. You will find example `python` code to consume
your created endpiont in your [Scailable admin](https://admin.sclbl.net) which you can directly
copy-paste into your python project. But, if you want it even easier you can also
add the following to your code:

````python
from sclblpy import run

cfid = "e93d0176-90f8-11ea-b602-9600004e79cc"  # This is the integer sum demo.
fv = [1,2,3,4,5]
result = run(cfid, fv)

print(result) # Prints the full result from the Scailable server.
````


## Supported models

The list of models supported by the current version of the `sclblpy` package can always be retrieved 
using the `list_models()` function. Here we provide an overview:

Package | Model | Tested (05052020) | Note 
--- | --- | --- | --- 
lightgbm | LGBMClassifier | ok |  
lightgbm | LGBMRegressor | ok |  
sklearn | ARDRegression | ok |  
sklearn | BayesianRidge | ok |  
sklearn | DecisionTreeClassifier | ok |  
sklearn | DecisionTreeRegressor | ok |  
sklearn | ElasticNet | ok |  
sklearn | ElasticNetCV | ok |  
sklearn | ExtraTreeClassifier | ok |  
sklearn | ExtraTreeRegresso | ok |  
sklearn | ExtraTreesClassifier | ok |  
sklearn | ExtraTreesRegressor | ok |  
sklearn | HuberRegressor | ok |  
sklearn | Lars | ok |  
sklearn | LarsCV | ok |  
sklearn | Lasso | ok |  
sklearn | LassoCV | ok |  
sklearn | LassoLars | ok |  
sklearn | LassoLarsCV | ok |  
sklearn | LassoLarsIC | ok |  
sklearn | LinearRegression | ok |  
sklearn | LinearSVC | ok |  
sklearn | LinearSVR | ok |  
sklearn | LogisticRegression | ok |  
sklearn | LogisticRegressionCV | ok |  
sklearn | NuSVC | ok |  
sklearn | NuSVR | ok |  
sklearn | OrthogonalMatchingPursuit | ok |  
sklearn | OrthogonalMatchingPursuitCV | ok |  
sklearn | PassiveAggressiveClassifier | ok |  
sklearn | PassiveAggressiveRegressor | ok |  
sklearn | Perceptron | ok |  
sklearn | RandomForestClassifier | ok |  
sklearn | RandomForestRegressor | ok |  
sklearn | RANSACRegressor | ok |  
sklearn | Ridge | ok |  
sklearn | RidgeClassifier | ok |  
sklearn | RidgeClassifierCV | ok |  
sklearn | RidgeCV | ok |  
sklearn | SGDClassifier | ok |  
sklearn | SGDRegressor | ok |  
sklearn | SVC | ok |  
sklearn | SVR | ok |  
sklearn | TheilSenRegressor | ok |  
statsmodels | Generalized Least Squares (GLS) | ok |  
statsmodels | Generalized Least Squares with AR Errors (GLSAR) | ok |  
statsmodels | Ordinary Least Squares (OLS) | ok |  
statsmodels | Quantile Regression (QuantReg) | ok |  
statsmodels | Weighted Least Squares (WLS) | ok |  
xgboost | XGBClassifier | ok |  
xgboost | XGBRegressor | ok |  
xgboost | XGBRFClassifier | ok | Binary only
xgboost | XGBRFRegressor | ok |  

## Dependencies

sclblpy needs python 3, and has been tested on python `> 3.7`. Furthermore, dependent on usage, sclblpy will import
the following packages:

* `numpy`
* `requests`
* `uuid`
* `sklearn`

The `statsmodels` and `xgboost` packages are imported when used.

## Notes:

* We try to stick to the naming conventions in [http://google.github.io/styleguide/pyguide.html](http://google.github.io/styleguide/pyguide.html).
* The methods `_set_toolchain_URL(string)` and `_set_usermanager_URL(string)` can be used to change the default location of
the toolchain and user-management function. These are useful when running the Scailable stack locally. Also the method `_toggle_debug_mode()` can
be used for troubleshooting (this will raise exceptions and provide a trace upon errors).
* Docs generated using `pdoc --html --html-dir docs sclblpy/main.py`

If you are having trouble using the `sclblpy` package, please [submit an issue to our github](https://github.com/scailable/sclblpy/issues/new), 
we will try to fix it as quickly as possible!
