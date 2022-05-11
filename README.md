# sclblpy

[![PyPI Release](https://github.com/scailable/sclblpy/workflows/PyPI%20Release/badge.svg)](https://pypi.org/project/sclblpy/)


Changelog: the package is currently being refactored. As such, it is currently a stub, as Scailable has changed its focus from Scikit Learn to ONNX, Scikit Learn support has been removed.
1. Removal of support for additional packages - most importantly in the 'upload()' function which now will throw an error if `model_type` isn't onnx
2. the `run()` function is going to be replaced by a function that allows the user to test their local setup; and as such is a stub


`sclblpy` is the core python package provided by Scailable for interacting with our API. The scope of this package is (roughly):
1. upload an `.onnx` model to the admin console
2. Assign and deploy the uploaded model to a device that has previously been installed with the Scailable runtime and registered
3. (upcoming) test device deployment




Also, there will probably be breaking changes in the API in one of the upcoming releases, for more information see [our API documentation](https://docs.sclbl.net/).


`sclblpy` is only functional in combination with a valid Scailable user account.

- **Website:** [https://www.scailable.net](https://www.scailable.net)
- **Docs:**
   - On GitHub (you are here): [https://github.com/scailable/sclblpy](https://github.com/scailable/sclblpy/blob/master/README.md)
   - On pypi: [https://docs.sclbl.net/sclblpy](https://docs.sclbl.net/sclblpy)
   - API docs Scailable: [https://docs.sclbl.net](https://docs.sclbl.net)
- **Get an account:** [https://admin.sclbl.net/signup.html](https://admin.sclbl.net/signup.html) 
- **Install the AI manager:**
   - On any Linux device: [https://github.com/scailable/sclbl-tutorials/tree/master/solutions-manuals/sclbl-local-ai-manager](https://github.com/scailable/sclbl-tutorials/tree/master/solutions-manuals/sclbl-local-ai-manager)
   - On an Advantech device: [https://github.com/scailable/sclbl-tutorials/tree/master/solutions-manuals](https://github.com/scailable/sclbl-tutorials/tree/master/solutions-manuals)

## Background
The sclblpy package allows users with a valid scailable account (get one at [https://admin.sclbl.net/signup.html](https://admin.sclbl.net/signup.html)) 
to upload fitted ML / AI models to the Scailable toolchain server. This will result in:

1. The model being tested for errors on the client side.
2. The model being uploaded to Scailable, tested again, and if all test pass it will be converted to [WebAssembly](https://webassembly.org).
3. The model being made available to deploy to a preregistered (link on how to do that) device
4. (upcoming) The model being testable through test_run(example_input, device_id)

## Getting started

The following functions are likely most used:

### `sp.upload_onnx()` can be used to create model:
```python
def upload_onnx(path, example="", docs={}, email=True) -> bool:
    """upload_onnx uploads a fitted onnx model to Scailable.

    - The function first checks if the supplied path indeed references a .onnx file
    - Next, the docs are checked; if none are provided a warning is issued and a simple
    name is provided based on the model type.
    - Finally the onnx file and the supporting docs are uploaded to the toolchain.

    Note: This method prints user-feedback by default. This feedback can be suppressed by calling the
        stop_print() method.

    Args:
        path: The path referencing the onnx model location (i.e., the .onnx file location).
        example: String example input for the onnx file.
        docs: A dict{} containing the fields 'name' and 'documentation'.
        email: Bool indicating whether a confirmation email of a successful conversion should be send. Default True.

    Returns:
        False if upload failed, true otherwise

    Raises  (in debug mode):
        UploadModelError if unable to successfully bundle and upload the model.
    """
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
check = upload_onnx("PATH-TO-MODEL/FILE-NAME.onnx", "", docs, email=True)
```

Note that the file will be send to the Scailable platform; after it has been transpiled to WebAssembly you will receive an email (by default), but you can choose not to, by setting ``email=False``

## Additional functionality
Next to the main ``upload_onnx()`` function, the package also exposes the following functions to administer endpoints:

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

No `onnx` packages are
necessary for the `sclblpy` package to run.

## Notes:

* We try to stick to the naming conventions in [http://google.github.io/styleguide/pyguide.html](http://google.github.io/styleguide/pyguide.html).
* The methods `_set_toolchain_URL(string)` and `_set_usermanager_URL(string)` can be used to change the default location of
the toolchain and user-management function. These are useful when running the Scailable stack locally. Also the method `_toggle_debug_mode()` can
be used for troubleshooting (this will raise exceptions and provide a trace upon errors).
* Docs generated using `pdoc3 --force --html --output-dir docs sclblpy/main.py`
* We are actively developing our stack; we try to list changes from one version to the next as clearly as possible. If you find any errors or issues please add an issue to this repo."
If you are having trouble using the `sclblpy` package, please [submit an issue to our github](https://github.com/scailable/sclblpy/issues/new), 
we will try to fix it as quickly as possible!
