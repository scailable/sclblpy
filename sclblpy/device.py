import json
import requests as req
from sclblpy._globals import DEVICE_API_URL, SILENT, DEBUG, JWT_JSON_FILE
from sclblpy.errors import DeviceError, GroupError
from sclblpy.auth import _check_jwt


def get_device(uuid: str) -> dict:
    """Get a single device by uuid.
        Returns:
            Dictionary contains the device info
        """

    # Check if user is authenticated
    auth = _check_jwt()
    device = {}
    if auth:
        try:
            # Load JWT from file
            with open(JWT_JSON_FILE) as f:
                jwt_ = json.load(f)
            # Build URL and headers for API request
            url = f"{DEVICE_API_URL}/device/{uuid}"
            headers = {
                'Authorization': f"Bearer {jwt_['JWT_ACCESS_TOKEN']}"
            }
            # Send API request
            resp = req.get(url=url, headers=headers)
            # Raise an exception if request was unsuccessful
            resp.raise_for_status()
            if 'json' in resp.headers.get('Content-Type'):
                try:
                    # See if able to decode the JSON
                    device = resp.json()
                except ValueError:  # simplejson.decoder.JSONDecodeError
                    if not SILENT:
                        print("Unable to decode JSON error.")
                    if DEBUG:
                        raise DeviceError(device.get("Unable to decode JSON error."))
            else:
                if not SILENT:
                    print("Server at", DEVICE_API_URL, "did not return a valid JSON document.")
                if DEBUG:
                    raise DeviceError("Server at", DEVICE_API_URL, "did not return a valid JSON document.")
        except req.exceptions.RequestException as e:
            # Handle exceptions that may occur during API request
            print(f"Error occurred while fetching device: {e}")
        return device


def get_all_devices() -> dict:
    """Get all device accessible for the users' organisation.
        Returns:
            Dictionary contains all devices
        """

    # Check if user is authenticated
    auth = _check_jwt()
    devices = {}
    if auth:
        try:
            # Load JWT from file
            with open(JWT_JSON_FILE) as f:
                jwt_ = json.load(f)
            # Build URL and headers for API request
            url = f"{DEVICE_API_URL}/devices"
            headers = {
                'Authorization': f"Bearer {jwt_['JWT_ACCESS_TOKEN']}"
            }
            # Send API request
            resp = req.get(url=url, headers=headers)
            # Raise an exception if request was unsuccessful
            resp.raise_for_status()
            if 'json' in resp.headers.get('Content-Type'):
                try:
                    # See if able to decode the JSON
                    devices = resp.json()
                except ValueError:  # simplejson.decoder.JSONDecodeError
                    if not SILENT:
                        print("Unable to decode JSON error.")
                    if DEBUG:
                        raise DeviceError(devices.get("Unable to decode JSON error."))
            else:
                if not SILENT:
                    print("Server at", DEVICE_API_URL, "did not return a valid JSON document.")
                if DEBUG:
                    raise DeviceError("Server at", DEVICE_API_URL, "did not return a valid JSON document.")
        except req.exceptions.RequestException as e:
            # Handle exceptions that may occur during API request
            print(f"Error occurred while fetching organisation devices: {e}")
        return devices


def add_device(name: str, registration_token: str = None, runtime: str = None, serial: str = None, type: str = None) -> bool:
    """Add device to user's organisation.
        Args:
            name: Name of the device to upload
            registration_token:
            runtime:
            serial:
            type:
        Returns:
            True if device added, False otherwise
    """

    # Check if user is authenticated
    auth = _check_jwt()
    if auth:
        try:
            # Load JWT from file
            with open(JWT_JSON_FILE) as f:
                jwt_ = json.load(f)
            # Build URL and headers for API request
            url = f"{DEVICE_API_URL}/devices"
            headers = {
                'Authorization': f"Bearer {jwt_['JWT_ACCESS_TOKEN']}"
            }
            data = {
                'Name': name,
                'RegistrationToken': registration_token,
                'Runtime': runtime,
                'Serial': serial,
                'Type': type
            }
            # Send API request
            resp = req.post(url=url, headers=headers, json=data)
            print(resp.json())
            resp.raise_for_status()
        except Exception as e:
            # Handle exceptions that may occur during API request
            if not SILENT:
                print("FATAL: Unable to carry out the request: \n" + str(e)+
                      "\nYour device has not been added.\n")
            if DEBUG:
                raise DeviceError("Unable to carry out the request: " + str(e))
            return False
        # user feedback:
        if resp.status_code == 200:
            if not SILENT:
                print("Your device was successfully added to Scailable!")
                print("You can use the '_all_devices()' function to list all your devices. \n")
            return True


def update_device(uuid: str, name: str, runtime: str = "", serial: str = "", type: str = "") -> bool:
    """Update a single device.
        Args:
            name: Name of the model to upload
            runtime:
            serial:
            type:

        Returns:
            True if device updated, False otherwise
    """

    # Check if user is authenticated
    auth = _check_jwt()
    if not auth:
        if not SILENT:
            print("FATAL: We were unable to obtain JWT authorization for your account. \n"
                  "Your device has not been updated. \n")
        if DEBUG:
            raise DeviceError("We were unable to obtain JWT authorization.")
        return False

    if auth:
        try:
            # Load JWT from file
            with open(JWT_JSON_FILE) as f:
                jwt_ = json.load(f)
            # Build URL and headers for API request
            url = f"{DEVICE_API_URL}/device/{uuid}"
            headers = {
                'Authorization': f"Bearer {jwt_['JWT_ACCESS_TOKEN']}"
            }
            data = {
                'Name': name,
                'Runtime': runtime,
                'Serial': serial,
                'Type': type
            }
            # Send API request
            resp = req.patch(url=url, headers=headers, json=data)
        except Exception as e:
            # Handle exceptions that may occur during API request
            if not SILENT:
                print("FATAL: Unable to carry out the request: \n"
                      "Your device has not been updated.\n")
            if DEBUG:
                raise DeviceError("Unable to carry out the request: " + str(e))
            return False

        # user feedback:
        if resp.status_code == 200:
            if not SILENT:
                print("Your device was successfully updated")
            return True


def assign_model_to_device(uuid: str, function_uuid: str) -> bool:
    """Assign a model to a device.
            Args:
                uuid: UUID of the device

            Returns:
                True if model assigned, False otherwise
        """

    # Check if user is authenticated
    auth = _check_jwt()
    if not auth:
        if not SILENT:
            print("FATAL: We were unable to obtain JWT authorization for your account. \n"
                  "Your model has not been assigned. \n")
        if DEBUG:
            raise DeviceError("We were unable to obtain JWT authorization.")
        return False

    if auth:
        try:
            # Load JWT from file
            with open(JWT_JSON_FILE) as f:
                jwt_ = json.load(f)
            # Build URL and headers for API request
            url = f"{DEVICE_API_URL}/device/{uuid}/functions"
            headers = {
                'Authorization': f"Bearer {jwt_['JWT_ACCESS_TOKEN']}"
            }
            data = [{'FunctionUUID': function_uuid}]

            # Send API request
            resp = req.post(url=url, headers=headers, json=data)
        except Exception as e:
            # Handle exceptions that may occur during API request
            if not SILENT:
                print("FATAL: Unable to carry out the request: \n" + str(e)+
                      "Your model has not been assigned.\n")
            if DEBUG:
                raise DeviceError("Unable to carry out the request: " + str(e))
            return False

        # user feedback:
        if resp.status_code == 200:
            if not SILENT:
                print("Your model was successfully assigned to the device " + uuid)
            return True


def delete_device(uuid: str) -> bool:
    """Delete a device.
        Args:
            uuid: id of the device to delete
        Returns:
            True if device deleted, false otherwise
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
            url = f"{DEVICE_API_URL}/device/{uuid}"
            headers = {
                'Authorization': f"Bearer {jwt_['JWT_ACCESS_TOKEN']}"
            }
            # Send API request
            resp = req.delete(url=url, headers=headers)
            # Raise an exception if request was unsuccessful
            resp.raise_for_status()
            if 'json' in resp.headers.get('Content-Type'):
                try:
                    # See if able to decode the JSON
                    result: dict = resp.json()
                except ValueError:
                    if not SILENT:
                        print("Unable to decode JSON error.")
                    if DEBUG:
                        raise DeviceError(result.get("Unable to decode JSON error."))
                    return False
            else:
                if not SILENT:
                    print("Server at", DEVICE_API_URL, "did not return a valid JSON document.")
                if DEBUG:
                    raise DeviceError("Server at", DEVICE_API_URL, "did not return a valid JSON document.")
                return False
            if result.get("Message") == "Deleted":
                print('Your device was successfully deleted')
                return True

        except req.exceptions.RequestException as e:
            # Handle exceptions that may occur during API request
            print(f"Error occurred while deleting device: {e}")
            return False


def devices_statistics() -> dict:
    """Return a dict with generic statistics for devices
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
            url = f"{DEVICE_API_URL}/devices/statistics"
            headers = {
                'Authorization': f"Bearer {jwt_['JWT_ACCESS_TOKEN']}"
            }
            # Send API request
            resp = req.get(url=url, headers=headers)
            # Raise an exception if request was unsuccessful
            resp.raise_for_status()
            if 'json' in resp.headers.get('Content-Type'):
                try:
                    # See if able to decode the JSON
                    statistics = resp.json()
                except ValueError:  # simplejson.decoder.JSONDecodeError
                    if not SILENT:
                        print("Unable to decode JSON error.")
                    if DEBUG:
                        raise DeviceError(statistics.get("Unable to decode JSON error."))
            else:
                if not SILENT:
                    print("Server at", DEVICE_API_URL, "did not return a valid JSON document.")
                if DEBUG:
                    raise DeviceError("Server at", DEVICE_API_URL, "did not return a valid JSON document.")
        except req.exceptions.RequestException as e:
            # Handle exceptions that may occur during API request
            print(f"Error occurred while fetching organisation devices statistics: {e}")
        return statistics


def get_groups() -> dict:
    """Get all groups accessible for the users' organisation.
        Returns:
            Dictionary contains all groups
        """

    # Check if user is authenticated
    auth = _check_jwt()
    groups = {}
    if auth:
        try:
            # Load JWT from file
            with open(JWT_JSON_FILE) as f:
                jwt_ = json.load(f)
            # Build URL and headers for API request
            url = f"{DEVICE_API_URL}/groups"
            headers = {
                'Authorization': f"Bearer {jwt_['JWT_ACCESS_TOKEN']}"
            }
            # Send API request
            resp = req.get(url=url, headers=headers)
            # Raise an exception if request was unsuccessful
            resp.raise_for_status()
            if 'json' in resp.headers.get('Content-Type'):
                try:
                    # See if able to decode the JSON
                    groups = resp.json()
                except ValueError:  # simplejson.decoder.JSONDecodeError
                    if not SILENT:
                        print("Unable to decode JSON error.")
                    if DEBUG:
                        raise GroupError(groups.get("Unable to decode JSON error."))
            else:
                if not SILENT:
                    print("Server at", DEVICE_API_URL, "did not return a valid JSON document.")
                if DEBUG:
                    raise GroupError("Server at", DEVICE_API_URL, "did not return a valid JSON document.")
        except req.exceptions.RequestException as e:
            # Handle exceptions that may occur during API request
            print(f"Error occurred while fetching organisation groups list: {e}")
        return groups


def delete_group(uuid: str) -> bool:
    """Delete a group.
        Args:
            uuid: id of the group to delete
        Returns:
            True if group deleted, false otherwise
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
            url = f"{DEVICE_API_URL}/group/{uuid}"
            headers = {
                'Authorization': f"Bearer {jwt_['JWT_ACCESS_TOKEN']}"
            }
            # Send API request
            resp = req.delete(url=url, headers=headers)
            # Raise an exception if request was unsuccessful
            resp.raise_for_status()
            if 'json' in resp.headers.get('Content-Type'):
                try:
                    # See if able to decode the JSON
                    result: dict = resp.json()
                except ValueError:
                    if not SILENT:
                        print("Unable to decode JSON error.")
                    if DEBUG:
                        raise GroupError(result.get("Unable to decode JSON error."))
                    return False
            else:
                if not SILENT:
                    print("Server at", DEVICE_API_URL, "did not return a valid JSON document.")
                if DEBUG:
                    raise GroupError("Server at", DEVICE_API_URL, "did not return a valid JSON document.")
                return False
            if result.get("Message") == "Deleted":
                return True

        except req.exceptions.RequestException as e:
            # Handle exceptions that may occur during API request
            print(f"Error occurred while deleting group: {e}")
            return False


def add_devices_to_group(uuid: str, devices: list) -> bool:
    """Add devices to a group.
        Args:
            uuid: Uuid of the group
            devices: List of devices to add to the group

        Returns:
            True if devices added to the group, False otherwise
    """

    # Check if user is authenticated
    auth = _check_jwt()
    if auth:
        try:
            # Load JWT from file
            with open(JWT_JSON_FILE) as f:
                jwt_ = json.load(f)
            # Build URL and headers for API request
            url = f"{DEVICE_API_URL}/group/{uuid}/devices"
            headers = {
                'Authorization': f"Bearer {jwt_['JWT_ACCESS_TOKEN']}"
            }
            data = {
                'Devices': devices
            }
            # Send API request
            resp = req.post(url=url, headers=headers, json=data)
        except Exception as e:
            # Handle exceptions that may occur during API request
            if not SILENT:
                print("FATAL: Unable to carry out the request: \n"
                      "Your device has not been added to the group.\n")
            if DEBUG:
                raise DeviceError("Unable to carry out the request: " + str(e))
            return False

        # user feedback:
        if resp.status_code == 200:
            if not SILENT:
                print("Your device was successfully added to the group " + uuid)
            return True


def delete_device_from_group(uuid_device: str, uuid_group: str) -> bool:
    """Delete a device from a group.
        Args:
            uuid_device: id of the device to delete
            uuid_group: id of the group of the device
        Returns:
            True if device deleted, false otherwise
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
            url = f"{DEVICE_API_URL}/device/{uuid_device}/group/{uuid_group}"
            headers = {
                'Authorization': f"Bearer {jwt_['JWT_ACCESS_TOKEN']}"
            }
            # Send API request
            resp = req.delete(url=url, headers=headers)
            # Raise an exception if request was unsuccessful
            resp.raise_for_status()
            if 'json' in resp.headers.get('Content-Type'):
                try:
                    # See if able to decode the JSON
                    result: dict = resp.json()
                except ValueError:
                    if not SILENT:
                        print("Unable to decode JSON error.")
                    if DEBUG:
                        raise DeviceError(result.get("Unable to decode JSON error."))
                    return False
            else:
                if not SILENT:
                    print("Server at", DEVICE_API_URL, "did not return a valid JSON document.")
                if DEBUG:
                    raise DeviceError("Server at", DEVICE_API_URL, "did not return a valid JSON document.")
                return False
            if result.get("Message") == "Ok":
                print('Your device was successfully deleted from the group.')
                return True
        except req.exceptions.RequestException as e:
            # Handle exceptions that may occur during API request
            print(f"Error occurred while deleting device from group: {e}")
            return False
