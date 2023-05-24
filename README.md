# sclblpy

`sclblpy` is the core python package provided by Scailable for interacting with our API. 

`sclblpy` is only functional in combination with a valid Scailable user account.

- **Website:** [https://www.scailable.net](https://www.scailable.net)
- **Docs:**
   - On GitHub (you are here): [https://github.com/scailable/sclblpy](https://github.com/scailable/sclblpy/blob/master/README.md)
   - API docs Scailable: [https://docs.sclbl.net](https://docs.sclbl.net)

The scope of this package is:

## Manage scailable account (auth.py)
1. Create an account in the scailable plateform
2. Sign in to an existing account
3. Reset password or set a new password
4. Get account information

## Manage models (compute.py)
1. Upload an `.onnx` model to the Scailable
2. Update an existing model
3. Delete a model
4. Get model's details
5. Get all the models accessible to your organisation.
6. Add a catalogue (set of models) to your organisation
7. Update an existing catalogue
8. Delete a catalogue
9. Get catalogue's details
10. Get all the catalogues accessible for your organisation.
11. Get the configured parameters for service
12. Get statistics of all models for your organisation

## Manage devices (device.py)
1. Add a device to your organisation
2. Update a device
3. Get device's details
4. Assign a model to a device
5. Delete a device
6. Get devices statistics
7. Get all devices accessible for your organisation
8. Get all groups accessible for your organisation
9. Delete a group
10. Add a device to a group
11. Delete a device from a group


## Getting started

### Get a Scailable account

To create a Scailable account you can use `register_()` function or sign up at [https://admin.sclbl.net/register](https://admin.sclbl.net/register) 
```python

def register_(name: str, company: str, email: str, password: str, job_title: str,
               phone_number: str, newsletter_optIn: bool = True, accept_eula: bool = True) -> bool:
    """Performs the sign-up of a user.
    The function register performs a sign-up of a new user.
    It returns a boolean value indicating whether the sign-up was successful.
        Args:
            name: A string (name of the user)
            company: A string (name of the user's company)
            email: A string (email)
            password: A string (password)
            job_title: A string (job of the user)
            phone_number: A string (user's phone number)
            newsletter_optIn: Bool (whether to add this email address to the newsletter)
            accept_eula: Bool (Agreement to the EULA)

        Returns:
            True if sign-up is successful.
   """
```

You already have a Scailable account? then you can sign in to your account using `log_in` function.
```python
def log_in(email: str, password: str) -> bool:
    """Performs the sign in of a user.
        The function _log_in performs a log in of a user based
        on the email (str) and password (str). It returns
        a boolean value indicating whether the log in was successful.
        Args:
            email: A string (email) to log in the user
            password: A string (password) for login
        Returns:
            True if sign in is successful.
    """
```

The following functionalities are likely most used:

### Upload an `onnx` model

To upload your models to Scailable, you can use `_upload_model`. (only models with onnx format are accepted)

```python
def upload_model(name: str, documentation: str, input_driver: str = "", input_driver_details: dict = {},
                  output_driver: str = "", output_driver_details: dict = {},
                  alias: str = "", path: str = "", source_name=None, source_url=None) -> bool:
    """_upload_model uploads a fitted onnx model to Scailable.

        - The function first checks if the supplied path indeed references a .onnx file
        - Next the onnx file and the supporting docs are uploaded.

        Args:
            name: Name of the model to upload
            input_driver:
            input_driver_details:
            output_driver:
            output_driver_details:
            alias: Alias of the model
            documentation: Documentation of the model
            path: The path referencing the onnx model location (i.e., the .onnx file location).
            source_name:
            source_url:
        Returns:
            False if upload failed, True otherwise
    """
```

### Add a device

To add a device to Scailable, you can use `add_device`.
```python
def add_device(name: str, registration_token: str = "", runtime: str = "", serial: str = "", type: str = "") -> bool:
    """Add device to user's organisation.
        Args:
            name: Name of the model to upload
            registration_token:
            runtime:
            serial:
            type:
        Returns:
            True if device added, False otherwise
    """
```

### Assign a model to a device

To assign a model to your device, you can use `_assign_model_to_device`.
```python
def assign_model_to_device(uuid: str, function_uuid: str) -> bool:
    """Assign a model to a device.
            Args:
                uuid: UUID of the device

            Returns:
                True if model assigned, False otherwise
        """
```





