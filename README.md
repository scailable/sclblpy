# sclblpy

[![PyPI Release](https://github.com/scailable/sclblpy/workflows/PyPI%20Release/badge.svg)](https://pypi.org/project/sclblpy/)

`sclblpy` is the core python package provided by Scailable to convert models fit in python to WebAssembly and
open them up as a REST endpoint.

Currently the package supports the upload of fitted `sklearn` model objects, and it supports uploading `.onnx` models
(by specifying a path to the `.onnx` file). The package can also be used to manage assignments of models to 
registered devices. 

`sclblpy` is only functional in combination with a valid Scailable user account.

- **Website:** [https://www.scailable.net](https://www.scailable.net)
- **Docs:**
   - On github: [https://github.com/scailable/sclblpy](https://github.com/scailable/sclblpy/blob/master/README.md)
   - On pypi: [https://docs.sclbl.net/sclblpy](https://docs.sclbl.net/sclblpy)
   - API docs Scailable: [https://docs.sclbl.net](https://docs.sclbl.net)
- **Get an account:** [https://www.scailable.net](https://www.scailable.net?access-code=sclblpy-installation)
- **Source:** [https://github.com/scailable/sclblpy/](https://github.com/scailable/sclblpy/)
- **Getting started:** [https://github.com/scailable/sclbl-tutorials/tree/master/sclbl-101-getting-started](https://github.com/scailable/sclbl-tutorials/tree/master/sclbl-101-getting-started)

## Background
The sclblpy package allows users with a valid scailable account (apply for one at [https://www.scailable.net](https://www.scailable.net))
to upload fitted ML / AI models to the Scailable toolchain server. This will result in:

1. The model being tested on the client side.
2. The model being uploaded to Scailable, tested again, and if all test pass it will be converted to [WebAssembly](https://webassembly.org).
3. The model being made available as an easy to access REST endpoint.

## Getting started

The following functions are likely most used:

### `sp.upload()` can be used to create model:
```python
def upload(mod, features, docs={}, email=True, model_type="sklearn", _keep=False) -> bool:
    """upload uploads a trained AI/ML model to Scailable.

    The upload function is the main workhorse of the sclblpy package but effectively provides a
    wrapper to choose between the
     - upload_sklearn(mod, feature_vector, docs={}, email=True, _keep=False)
     - upload_onnx(path, docs={}, email=True)
    functions.

    The function checks the type, and if type = "sklearn" (default) calls the upload_sklearn() function.
    If type = "onnx" it calls the upload_onnx() function.

    Args:
        mod: The model to be uploaded (type="sklearn" OR the path to the stored ONNX file (type="onnx").
        features:
            - An example feature_vector for your model (type="sklearn" only).
            (i.e., the first row of your training data X obtained using row = X[0,:])
            - The input str (binary) to the onnx model (type="onnx" only). Can be an empty string.
        docs: A dict{} containing the fields 'name' and 'documentation'.
        email: Bool indicating whether a confirmation email of a successful conversion should be send. Default True.
        model_type: String indicating the type of model. Currently with options "sklearn" or "onnx". Default "sklearn"
        _keep: Bool indicating whether the .gzipped file should be retained (type="sklearn" only). Default False.

    Returns:
        False if upload failed, true otherwise"""
```
`sp.models()` lists all created models, and `sp.delete_model()` can be used to delete a model. Finally, `sp.update()` can be used to
overwrite / update an existing model.

### `sp.assign()` can be used to assign a model to a device:
```python
def assign(cfid, did, rid, _verbose=True):
    """ Assign a model to a device.

    Using the global JWT string this function assigns a model (using its cfid) to a device (using its did).

    Args:
        cfid: String identifying the model / compute-function
        did: String identifying the device
        rid: String identifying the registration ID of the device (not, run "devices"

    Returns:
        Boolean indicating whether the assignment was successful.
    """
``` 
`sp.assignments()` can be used to list current assignments, whereas `sp.delete_assignment()` can be used to delete an assignment. 

## A simple example using `sklearn`
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

# Create an example feature vector (required for sklearn models):
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
 [https://www.scailable.net](https://www.scailable.net?access-code=sclblpy-installation)).

 
### More `sklearn` examples
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

## A simple `.onnx` example

The following code can be used to upload a stored `.onnx` model:
```python

# Add docs
docs = {}
docs['name'] = "Name of ONNX model"
docs['documentation'] = "A long .md thing...."
check = sp.upload("PATH-TO-MODEL/FILE-NAME.onnx", "", docs, model_type="onnx")
```

Note that the file will be send to the Scailable platform; after it has been transpiled to WebAssembly you will receive 
(by default) and email.

## Additional functionality
Next to the main ``upload()`` function, the package also exposes the following functions to administer endpoints:

````
# List all models owned by the current user:
sp.models()

# Remove an endpoint:
sp.delete_models(cfid)  # Where cfid is the compute function id

# Update an existing endpoint:
sp.update(mod, fv, cfid, docs)  # Where cfid is the compute function id

# Update an existing ednpoint without updating the docs:
sp.update(mod, fv, cfid) 

# Update only the docs of an existing endpoint:
sp.update_docs(cfid, docs)

# See all devices:
sp.devices(offset=0, limit=20, _verbose=True, _return=False)

# Delete device:
sp.delete_device(did)

# See all assignments:
sp.assignments(offset=0, limit=20, _verbose=True, _return=False)

# Create an assignment:
sp.assign(cfid, did, rid, _verbose=True)

# Remove an assignment:
sp.delete_assignment(aid) 
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


## Supported `sklearn` models

The list of models supported by the current version of the `sclblpy` package can always be retrieved 
using the `list_models()` function. Here we provide an overview:

Package | Model | Tested (19-06-2020) | Note 
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

## Supported `.onnx` files

We currently support `ONNX` version 1.8 (and below) in full. However, if you encounter any problems
converting `.onnx` files please let us know.

## Dependencies

sclblpy needs python 3, and has been tested on python `> 3.7`. Furthermore, dependent on usage, sclblpy will import
the following packages:

* `numpy`
* `requests`
* `uuid`
* `sklearn`

The `statsmodels` and `xgboost` packages are imported when used. No `onnx` packages are
neccesary for the `sclblpy` package to run.

## Notes:

* We try to stick to the naming conventions in [http://google.github.io/styleguide/pyguide.html](http://google.github.io/styleguide/pyguide.html).
* The methods `_set_toolchain_URL(string)` and `_set_usermanager_URL(string)` can be used to change the default location of
the toolchain and user-management function. These are useful when running the Scailable stack locally. Also the method `_toggle_debug_mode()` can
be used for troubleshooting (this will raise exceptions and provide a trace upon errors).
* Docs generated using `pdoc --html --html-dir docs sclblpy/main.py`

If you are having trouble using the `sclblpy` package, please [submit an issue to our github](https://github.com/scailable/sclblpy/issues/new), 
we will try to fix it as quickly as possible!
