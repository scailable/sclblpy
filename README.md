# sclblpy

[![PyPI Release](https://github.com/scailable/sclblpy/workflows/PyPI%20Release/badge.svg)](https://pypi.org/project/sclblpy/)


DISCLAIMER: Sclblpy is undergoing changes, most notably we will focus on .onnx from now on, meaning sklearn and similar packages are no longer supported as well as the removal of the `run()` function.
Expect unstable APIs!
If you're the maintainer of a project and run into problems, feel free to send us a message at support@scailable.net

`sclblpy` is the core python package provided by Scailable for interacting with our API. The scope of this package is (roughly):
1. upload an `.onnx` model to the admin console
2. Assign and deploy the uploaded model to a device that has previously been installed with the Scailable runtime and registered
3. (upcoming) test device deployment


NOTE: the package is currently undergoing a major rework. We try to keep the below up to date, but some features might be stubs. 
Most relevant is the removal of support for Scikit learn in favor of focussing fully on ONNX.

Also, there will probably be breaking changes in the API in one of the upcoming releases.


`sclblpy` is only functional in combination with a valid Scailable user account.

- **Website:** [https://www.scailable.net](https://www.scailable.net)
- **Docs:**
   - On github (you are here): [https://github.com/scailable/sclblpy](https://github.com/scailable/sclblpy/blob/master/README.md)
   - On pypi: [https://docs.sclbl.net/sclblpy](https://docs.sclbl.net/sclblpy)
   - API docs Scailable: [https://docs.sclbl.net](https://docs.sclbl.net)
- **Get an account:** [https://admin.sclbl.net/signup.html](https://admin.sclbl.net/signup.html) 
- **Install the AI manager:**
   - Locally: [https://github.com/scailable/sclbl-tutorials/tree/master/solutions-manuals/sclbl-local-ai-manager](https://github.com/scailable/sclbl-tutorials/tree/master/solutions-manuals/sclbl-local-ai-manager)
   - On an advantech device: [https://github.com/scailable/sclbl-tutorials/tree/master/solutions-manuals](https://github.com/scailable/sclbl-tutorials/tree/master/solutions-manuals)

## Background
The sclblpy package allows users with a valid scailable account (get one at [https://admin.sclbl.net/signup.html](https://admin.sclbl.net/signup.html)) 
to upload fitted ML / AI models to the Scailable toolchain server. This will result in:

1. The model being tested for errors on the client side.
2. The model being uploaded to Scailable, tested again, and if all test pass it will be converted to [WebAssembly](https://webassembly.org).
3. The model being made available to deploy to a pre-regsitered (link on how to do that) device
4. (upcoming) The model being testable through test_run(example_input, device_id)

## Getting started

The following functions are likely most used:

### `sp.upload()` can be used to create model:
```python
def upload(mod, features, docs={}, email=True, _keep=False) -> bool:
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

## Supported `.onnx` files

We currently support `ONNX` version 1.8 (and below) in full. However, if you encounter any problems
converting `.onnx` files please let us know.

## Dependencies

sclblpy needs python 3, and has been tested on python `> 3.7`. Furthermore, dependent on usage, sclblpy will import
the following packages:

* `numpy`
* `requests`
* `uuid`
* `sklearn` (legacy, to be removed in future updates)

No `onnx` packages are
neccesary for the `sclblpy` package to run.

## Notes:

* We try to stick to the naming conventions in [http://google.github.io/styleguide/pyguide.html](http://google.github.io/styleguide/pyguide.html).
* The methods `_set_toolchain_URL(string)` and `_set_usermanager_URL(string)` can be used to change the default location of
the toolchain and user-management function. These are useful when running the Scailable stack locally. Also the method `_toggle_debug_mode()` can
be used for troubleshooting (this will raise exceptions and provide a trace upon errors).
* Docs generated using `pdoc --html --html-dir docs sclblpy/main.py`

If you are having trouble using the `sclblpy` package, please [submit an issue to our github](https://github.com/scailable/sclblpy/issues/new), 
we will try to fix it as quickly as possible!
