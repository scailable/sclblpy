import json
import requests as req
from sclblpy._globals import COMPUTE_API_URL, SILENT, DEBUG, JWT_JSON_FILE
from sclblpy.errors import ModelError, CatalogueError, ConfigError
import os
from sclblpy.auth import _check_jwt


def get_all_models() -> list:
    """
    Returns all models accessible to the users' organisation.
    """

    # Check if user is authenticated
    auth = _check_jwt()
    models = []
    if auth:
        try:
            # Load JWT from file
            with open(JWT_JSON_FILE) as f:
                jwt_ = json.load(f)
            # Build URL and headers for API request
            url = f"{COMPUTE_API_URL}/functions"
            headers = {
                'Authorization': f"Bearer {jwt_['JWT_ACCESS_TOKEN']}"
            }
            # Send API request
            resp = req.get(url=url, headers=headers)
            # Raise an exception if request was unsuccessful
            resp.raise_for_status()
            # Check if response is in JSON format
            if 'json' in resp.headers.get('Content-Type'):
                try:
                    # See if able to decode the JSON
                    models = resp.json()
                except ValueError:  # simplejson.decoder.JSONDecodeError
                    if not SILENT:
                        print("Unable to decode JSON error.")
                    if DEBUG:
                        raise ModelError(models.get("Unable to decode JSON error."))
            else:
                if not SILENT:
                    print("Server at", COMPUTE_API_URL, "did not return a valid JSON document.")
                if DEBUG:
                    raise ModelError("Server at", COMPUTE_API_URL, "did not return a valid JSON document.")
        except req.exceptions.RequestException as e:
            # Handle exceptions that may occur during API request
            print(f"Error occurred while fetching organisation functions: {e}")
        return models


def get_model(uuid: str) -> dict:
    """
    Returns: get model's details by uuid
    """

    # Check if user is authenticated
    auth = _check_jwt()
    if auth:
        details = {}
        try:
            # Load JWT from file
            with open(JWT_JSON_FILE) as f:
                jwt_ = json.load(f)
            # Build URL and headers for API request
            url = f"{COMPUTE_API_URL}/function/{uuid}"
            headers = {
                'Authorization': f"Bearer {jwt_['JWT_ACCESS_TOKEN']}"
            }
            # Send API request
            resp = req.get(url=url, headers=headers)
            # Raise an exception if request was unsuccessful
            resp.raise_for_status()
            # Check if response is in JSON format
            if 'json' in resp.headers.get('Content-Type'):
                try:
                    # See if able to decode the JSON
                    details = resp.json()
                except ValueError:  # simplejson.decoder.JSONDecodeError
                    if not SILENT:
                        print("Unable to decode JSON error.")
                    if DEBUG:
                        raise ModelError(details.get("Unable to decode JSON error."))
            else:
                if not SILENT:
                    print("Server at", COMPUTE_API_URL, "did not return a valid JSON document.")
                if DEBUG:
                    raise ModelError("Server at", COMPUTE_API_URL, "did not return a valid JSON document.")
        except req.exceptions.RequestException as e:
            # Handle exceptions that may occur during API request
            print(f"Error occurred while fetching model's details: {e}")
        return details


def upload_model(name: str, documentation: str, input_driver: str, output_driver: str = "",
                 input_driver_details: dict = {}, output_driver_details: dict = {},
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

    # Check if file exists:
    if not path.endswith('.onnx'):
        if not SILENT:
            print("FATAL: You did not specify a .onnx path. \n")
        if DEBUG:
            raise ModelError("We were unable to open the specified onnx file (no .onnx extension).")

    if not documentation:
        documentation = "-- EMPTY --"
        print(
            "WARNING: You did not provide any documentation for your model. We will simply use " + documentation + " as its documentation")
    if not name:
        name = os.path.splitext(os.path.basename(path))[0]
        print("WARNING: You did not provide any name for your model. We will simply use " + name + " as its name")

    # Check if user is authenticated
    auth = _check_jwt()
    if not auth:
        if not SILENT:
            print("FATAL: We were unable to obtain JWT authorization for your account. \n"
                  "Your model has not been uploaded. \n")
        if DEBUG:
            raise ModelError("We were unable to obtain JWT authorization.")
        return False

    if auth:
        try:
            # Load JWT from file
            with open(JWT_JSON_FILE) as f:
                jwt_ = json.load(f)
            # Build URL and headers for API request
            url = f"{COMPUTE_API_URL}/functions"
            headers = {
                'Authorization': f"Bearer {jwt_['JWT_ACCESS_TOKEN']}"
            }
            data = {
                'Name': name,
                'Alias': alias,
                'Documentation': documentation,
                'InputDriver': input_driver,
                'InputDriverDetails': input_driver_details,
                'OutputDriver': output_driver,
                'OutputDriverDetails': output_driver_details,
                'SourceName': source_name,
                'SourceUrl': source_url
            }
            files = {
                'data': (None, json.dumps(data)),
                'file': (os.path.basename(path), open(path, 'rb'), 'application/octet-stream')
            }
            # Send API request
            resp = req.post(url=url, headers=headers, files=files)
        except Exception as e:
            # Handle exceptions that may occur during API request
            if not SILENT:
                print("FATAL: Unable to carry out the upload request: \n"
                      "Your model has not been uploaded.\n" + str(e))
            if DEBUG:
                raise ModelError("Unable to carry out the upload request: " + str(e))
            return False

        # user feedback:
        if resp.status_code == 200:
            if not SILENT:
                print("Your ONNX file was successfully uploaded to Scailable!")
                print("NOTE: After transpiling, we will send you an email and your model will be available at "
                      "https://admin.sclbl.net.")
                print(
                    "Or, alternatively, you can use the '_functions_list()' function to list all your uploaded "
                    "models. \n")
            return True


def update_model(uuid: str, name: str, documentation: str, input_driver: str, output_driver: str,
                 input_driver_details: dict = {}, output_driver_details: dict = {},
                 alias: str = "", path: str = "", source_name=None, source_url=None) -> bool:
    """Update a single model.
        Args:
            name:
            documentation:
            input_driver:
            input_driver_details:
            output_driver:
            output_driver_details:
            alias:
            path:
            source_name:
            source_url:

        Returns:
            True if model updated, False otherwise
    """

    if not path.endswith('.onnx'):
        if not SILENT:
            print("FATAL: You did not specify a .onnx path. \n")
        if DEBUG:
            raise ModelError("We were unable to open the specified onnx file (no .onnx extension).")

    if not documentation:
        doc = "-- EMPTY --"
        print("WARNING: You did not provide any documentation. We will simply use " + doc + " as its documentation")
    if not name:
        name = os.path.splitext(os.path.basename(path))[0]
        print("WARNING: You did not provide any name. We will simply use " + name + " as its name")

    # Check if user is authenticated
    auth = _check_jwt()
    if not auth:
        if not SILENT:
            print("FATAL: We were unable to obtain JWT authorization for your account. \n"
                  "Your model has not been updated. \n")
        if DEBUG:
            raise ModelError("We were unable to obtain JWT authorization.")
        return False

    if auth:
        try:
            # Load JWT from file
            with open(JWT_JSON_FILE) as f:
                jwt_ = json.load(f)
            # Build URL and headers for API request
            url = f"{COMPUTE_API_URL}/function/{uuid}"
            headers = {
                'Authorization': f"Bearer {jwt_['JWT_ACCESS_TOKEN']}"
            }
            data = {
                'Name': name,
                'Alias': alias,
                'Documentation': documentation,
                'InputDriver': input_driver,
                'InputDriverDetails': input_driver_details,
                'OutputDriver': output_driver,
                'OutputDriverDetails': output_driver_details,
                'SourceName': source_name,
                'SourceUrl': source_url
            }
            files = {
                'data': (None, json.dumps(data)),
                'file': (os.path.basename(path), open(path, 'rb'), 'application/octet-stream')
            }
            # Send API request
            resp = req.patch(url=url, headers=headers, files=files)
            resp.raise_for_status()
        except Exception as e:
            # Handle exceptions that may occur during API request
            if not SILENT:
                print("FATAL: Unable to carry out the request: " + str(e) +
                      "\n Your model has not been updated.\n")
            if DEBUG:
                raise ModelError("Unable to carry out the request: " + str(e))
            return False

        # user feedback:
        if resp.status_code == 200:
            if not SILENT:
                print("Your model was successfully updated")
            return True


def delete_model(uuid: str) -> bool:
    """Delete a model.
        Args:
            uuid: id of the model to delete
        Returns:
            True if model deleted, false otherwise
        """
    # Check if user is authenticated
    auth = _check_jwt()
    result = {}
    if auth:
        try:
            # Load JWT from file
            with open(JWT_JSON_FILE) as f:
                jwt_ = json.load(f)
            # Build URL and headers for API request
            url = f"{COMPUTE_API_URL}/function/{uuid}"
            headers = {
                'Authorization': f"Bearer {jwt_['JWT_ACCESS_TOKEN']}"
            }
            # Send API request
            resp = req.delete(url=url, headers=headers)
            resp.raise_for_status()
            if 'json' in resp.headers.get('Content-Type'):
                try:
                    # See if able to decode the JSON
                    result: dict = resp.json()
                except ValueError:  # simplejson.decoder.JSONDecodeError
                    if not SILENT:
                        print("Unable to decode JSON error.")
                    if DEBUG:
                        raise ModelError(result.get("Unable to decode JSON error."))
                    return False
            else:
                if not SILENT:
                    print("Server at", COMPUTE_API_URL, "did not return a valid JSON document.")
                if DEBUG:
                    raise ModelError("Server at", COMPUTE_API_URL, "did not return a valid JSON document.")
                return False
            if result.get("Message") == "Done":
                return True
        except req.exceptions.RequestException as e:
            # Handle exceptions that may occur during API request
            print(f"Error occurred while deleting model: {e}")
        return False


def add_catalogue(name: str) -> bool:
    """Add catalogue to user's organisation.
        Args:
            name: Name of the catalogue to add
        Returns:
            True if catalogue added, False otherwise
    """

    # Check if user is authenticated
    auth = _check_jwt()
    if auth:
        try:
            # Load JWT from file
            with open(JWT_JSON_FILE) as f:
                jwt_ = json.load(f)
            # Build URL and headers for API request
            url = f"{COMPUTE_API_URL}/catalogues"
            headers = {
                'Authorization': f"Bearer {jwt_['JWT_ACCESS_TOKEN']}"
            }
            data = {
                'Name': name,
            }
            # Send API request
            resp = req.post(url=url, headers=headers, json=data)
        except Exception as e:
            # Handle exceptions that may occur during API request
            if not SILENT:
                print("FATAL: Unable to carry out the request: \n"
                      "Your catalogue has not been added.\n")
            if DEBUG:
                raise CatalogueError("Unable to carry out the request: " + str(e))
            return False
        # user feedback:
        if resp.status_code == 200:
            if not SILENT:
                print("Your catalogue was successfully added to Scailable!")
                print("You can use the '_get_all_catalogues' function to list all your catalogues. \n")
            return True


def update_catalogue(uuid: str, name: str) -> bool:
    """Update a model catalogue.
        Args:
            uuid: UUID of the catalogue to update
            name: New name
        Returns:
            True if catalogue updated, False otherwise
    """

    # Check if user is authenticated
    auth = _check_jwt()
    if auth:
        try:
            # Load JWT from file
            with open(JWT_JSON_FILE) as f:
                jwt_ = json.load(f)
            # Build URL and headers for API request
            url = f"{COMPUTE_API_URL}/catalogue/{uuid}"
            headers = {
                'Authorization': f"Bearer {jwt_['JWT_ACCESS_TOKEN']}"
            }
            data = {
                'Name': name,
            }
            # Send API request
            resp = req.patch(url=url, headers=headers, json=data)
        except Exception as e:
            # Handle exceptions that may occur during API request
            if not SILENT:
                print("FATAL: Unable to carry out the request: " + str(e) +
                      "\n Your catalogue has not been updated.\n")
            if DEBUG:
                raise CatalogueError("Unable to carry out the request: " + str(e))
            return False
        # user feedback:
        if resp.status_code == 200:
            if not SILENT:
                print("Your catalogue was successfully updated to Scailable!")
            return True


def delete_catalogue(uuid: str) -> bool:
    """Delete a catalogue.
        Args:
            uuid: id of the catalogue to delete
        Returns:
            True if catalogue deleted, false otherwise
        """
    # Check if user is authenticated
    auth = _check_jwt()
    result = {}
    if auth:
        try:
            # Load JWT from file
            with open(JWT_JSON_FILE) as f:
                jwt_ = json.load(f)
            # Build URL and headers for API request
            url = f"{COMPUTE_API_URL}/catalogue/{uuid}"
            headers = {
                'Authorization': f"Bearer {jwt_['JWT_ACCESS_TOKEN']}"
            }
            # Send API request
            resp = req.delete(url=url, headers=headers)
            resp.raise_for_status()
            if 'json' in resp.headers.get('Content-Type'):
                try:
                    # See if able to decode the JSON
                    result: dict = resp.json()
                except ValueError:  # simplejson.decoder.JSONDecodeError
                    if not SILENT:
                        print("Unable to decode JSON error.")
                    if DEBUG:
                        raise ModelError(result.get("Unable to decode JSON error."))
                    return False
            else:
                if not SILENT:
                    print("Server at", COMPUTE_API_URL, "did not return a valid JSON document.")
                if DEBUG:
                    raise ModelError("Server at", COMPUTE_API_URL, "did not return a valid JSON document.")
                return False
            if result.get("Message") == "Done":
                print("Your catalogue was successfully deleted")
                return True
        except req.exceptions.RequestException as e:
            # Handle exceptions that may occur during API request
            print(f"Error occurred while deleting model: {e}")
        return False


def get_catalogue(uuid: str) -> dict:
    """Get catalogue's information
    Args:
        uuid: A string (the id of the catalogue)
    Returns:
        Dictionary contains the catalogue's information
    """

    # Check if user is authenticated
    auth = _check_jwt()
    if auth:
        catalogue = {}
        try:
            # Load JWT from file
            with open(JWT_JSON_FILE) as f:
                jwt_ = json.load(f)
            # Build URL and headers for API request
            url = f"{COMPUTE_API_URL}/catalogue/{uuid}"
            headers = {
                'Authorization': f"Bearer {jwt_['JWT_ACCESS_TOKEN']}"
            }
            # Send API request
            resp = req.get(url=url, headers=headers)
            # Raise an exception if request was unsuccessful
            resp.raise_for_status()
            # Check if response is in JSON format and extract catalogue data
            if 'json' in resp.headers.get('Content-Type'):
                try:
                    # See if able to decode the JSON
                    catalogue = resp.json()
                except ValueError:  # simplejson.decoder.JSONDecodeError
                    if not SILENT:
                        print("Unable to decode JSON error.")
                    if DEBUG:
                        raise CatalogueError(catalogue.get("Unable to decode JSON error."))
            else:
                if not SILENT:
                    print("Server at", COMPUTE_API_URL, "did not return a valid JSON document.")
                if DEBUG:
                    raise CatalogueError("Server at", COMPUTE_API_URL, "did not return a valid JSON document.")
        except req.exceptions.RequestException as e:
            # Handle exceptions that may occur during API request
            print(f"Error occurred while fetching user catalogue: {e}")
        return catalogue


def get_all_catalogues() -> dict:
    """Get all catalogues accessible for the users' organisation.
    Returns:
        Dictionary contains all catalogues
    """

    # Check if user is authenticated
    auth = _check_jwt()
    catalogues = {}
    if auth:
        try:
            # Load JWT from file
            with open(JWT_JSON_FILE) as f:
                jwt_ = json.load(f)
            # Build URL and headers for API request
            url = f"{COMPUTE_API_URL}/catalogues"
            headers = {
                'Authorization': f"Bearer {jwt_['JWT_ACCESS_TOKEN']}"
            }
            # Send API request
            resp = req.get(url=url, headers=headers)
            # Raise an exception if request was unsuccessful
            resp.raise_for_status()
            # Check if response is in JSON format and extract catalogue data
            if 'json' in resp.headers.get('Content-Type'):
                try:
                    # See if able to decode the JSON
                    catalogues = resp.json()
                except ValueError:  # simplejson.decoder.JSONDecodeError
                    if not SILENT:
                        print("Unable to decode JSON error.")
                    if DEBUG:
                        raise CatalogueError(catalogues.get("Unable to decode JSON error."))
            else:
                if not SILENT:
                    print("Server at", COMPUTE_API_URL, "did not return a valid JSON document.")
                if DEBUG:
                    raise CatalogueError("Server at", COMPUTE_API_URL, "did not return a valid JSON document.")
        except req.exceptions.RequestException as e:
            # Handle exceptions that may occur during API request
            print(f"Error occurred while fetching user catalogue: {e}")
        return catalogues


def models_statistics() -> dict:
    """Returns a dict with models statistics
        """
    # Check if user is authenticated
    auth = _check_jwt()
    statistics = {}
    if auth:
        try:
            # Load JWT from file
            with open(JWT_JSON_FILE) as f:
                jwt_ = json.load(f)
            # Build URL and headers for API request
            url = f"{COMPUTE_API_URL}/functions/statistics"
            headers = {
                'Authorization': f"Bearer {jwt_['JWT_ACCESS_TOKEN']}"
            }
            # Send API request
            resp = req.get(url=url, headers=headers)
            resp.raise_for_status()
            if 'json' in resp.headers.get('Content-Type'):
                try:
                    # See if able to decode the JSON
                    statistics: dict = resp.json()
                except ValueError:  # simplejson.decoder.JSONDecodeError
                    if not SILENT:
                        print("Unable to decode JSON error.")
                    if DEBUG:
                        raise ModelError(statistics.get("Unable to decode JSON error."))
        except req.exceptions.RequestException as e:
            # Handle exceptions that may occur during API request
            print(f"Error occurred while fetching organisation models statistics: {e}")
        return statistics


def config_parameters() -> dict:
    """
    Return: configured parameters for service.
    """

    # Check if user is authenticated
    auth = _check_jwt()
    if auth:
        config = {}
        try:
            # Load JWT from file
            with open(JWT_JSON_FILE) as f:
                jwt_ = json.load(f)
            # Build URL and headers for API request
            url = f"{COMPUTE_API_URL}/configuration"
            headers = {
                'Authorization': f"Bearer {jwt_['JWT_ACCESS_TOKEN']}"
            }
            # Send API request
            resp = req.get(url=url, headers=headers)
            # Raise an exception if request was unsuccessful
            resp.raise_for_status()
            # Check if response is in JSON format and extract config parameters
            if 'json' in resp.headers.get('Content-Type'):
                try:
                    # See if able to decode the JSON
                    config = resp.json()
                except ValueError:  # simplejson.decoder.JSONDecodeError
                    if not SILENT:
                        print("Unable to decode JSON error.")
                    if DEBUG:
                        raise ConfigError(config.get("Unable to decode JSON error."))
            else:
                if not SILENT:
                    print("Server at", COMPUTE_API_URL, "did not return a valid JSON document.")
                if DEBUG:
                    raise ConfigError("Server at", COMPUTE_API_URL, "did not return a valid JSON document.")
        except req.exceptions.RequestException as e:
            # Handle exceptions that may occur during API request
            print(f"Error occurred while getting configured parameters for service {e}")
        return config
