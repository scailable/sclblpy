# File contains all (private) methods for jwt interaction.
import requests as req
import time
import json
import jwt
import os
from sclblpy._globals import DEBUG, SILENT, AUTH_MANAGER_URL, USER_CREDENTIALS, JWT_JSON_FILE
from sclblpy.errors import LoginError, JWTError, RegisterError, UserDetailsError, PwdError


def _check_jwt(time_refresh=120, time_renew=3600) -> bool:
    """Checks whether a valid AccessToken string is present.
    First checks whether a valid RefreshToken string is present. If so,
    checks whether the RefreshToken needs refreshing and refreshes if necessary.
    Then checks if an AccessToken exists and is valid
    Returns
        True when a valid and fresh AccessToken string is located.
    Note, if no RefreshToken string is present, or the RefreshToken string has expired,
    the function tries to prompt user for email and password and subsequently sign in.
        Args:
            time_refresh: int, seconds before an AccessToken is requested.
            time_renew: int, seconds before a RefreshToken is requested.
        Returns:
            True if an AccessToken string is present and valid. False otherwise.
    """

    now: float = time.time()
    with open(JWT_JSON_FILE) as f:
        jwt_ = json.load(f)

    # if the RefreshToken doesn't exist or expired
    if not jwt_['JWT_REFRESH_TOKEN'] or jwt_['JWT_REFRESH_EXP'] < now:
        print("Session expired")
        email: str = input("Please provide your email: ")
        password: str = input("Please provide your password: ")
        try:
            return log_in(email, password)
        except LoginError as e:
            if not SILENT:
                print("JWT error: sign in failed:" + str(e))
            if DEBUG:
                raise JWTError("Sign in failed. " + str(e))
            return False

    # if the RefreshToken exist and needs a refresh
    if jwt_['JWT_REFRESH_TOKEN'] and jwt_['JWT_REFRESH_EXP'] - now < time_renew:
        try:
            return _refresh_jwt(jwt_['JWT_REFRESH_TOKEN'], True)
        except JWTError as e:
            if not SILENT:
                print("JWT error: refresh failed:" + str(e))
            if DEBUG:
                raise JWTError("Unable to refresh JWT TOKEN. " + str(e))
            return False

    # if the Accesstoken doesn't exist or needs a refresh
    if not jwt_['JWT_ACCESS_TOKEN'] or jwt_['JWT_EXP'] - now < time_refresh:
        try:
            if _refresh_jwt(jwt_['JWT_REFRESH_TOKEN']):
                return True
            else:
                return False
        except JWTError as e:
            if not SILENT:
                print("JWT error: refresh failed:" + str(e))
            if DEBUG:
                raise JWTError("Unable to refresh JWT TOKEN. " + str(e))
            return False

    # JWT token is present and no need to refresh yet:
    if jwt_['JWT_ACCESS_TOKEN']:
        return True


def _refresh_jwt(refresh_token: str, grant_type=False) -> bool:
    """Refreshes the JWT string.
    Refresh the JWT string based on an existing token.
    Args:
        Returns:
            True if refresh successful, False otherwise.
        Raises (in debug mode):
            JWTError if something is wrong with the JWT string.
    """

    try:
        result = {}
        # Build URL and headers for API request
        url: str = AUTH_MANAGER_URL + "/authenticate/refresh-token"
        data: dict = {}
        if grant_type:
            data = {
                'GrantType': "RefreshToken"
            }
        headers: dict = {
            'Authorization': f"Bearer {refresh_token}"
        }
        # Send API request
        resp: req.models.Response = req.post(url=url, headers=headers, json=data)
        if 'json' in resp.headers.get('Content-Type') and 10 < len(resp.content) < 400:
            try:
                result: dict = resp.json()
            except ValueError:
                if not SILENT:
                    print("Unable to decode JSON error.")
                if DEBUG:
                    raise JWTError(result.get("Unable to decode JSON error."))
                return False
        else:
            if not SILENT:
                print("Server at", AUTH_MANAGER_URL, "did not return a valid JSON document.")
            if DEBUG:
                raise JWTError("Server at", AUTH_MANAGER_URL, "did not return a valid JSON document.")
            return False
        if result.get("error") is not None:
            if not SILENT:
                print("JWT authentication error: The server generated an error: " + result.get("error"))
            if DEBUG:
                raise JWTError("JWT server error: " + result.get("error"))
            return False
        if grant_type:
            if result.get('RefreshToken') is not None:
                return _refresh_jwt(result.get('RefreshToken'))
            else:
                return False
        if result.get('AccessToken') is not None:
            with open(JWT_JSON_FILE) as f:
                jwt_ = json.load(f)
            decode = jwt.decode(result.get('AccessToken'), options={"verify_signature": False})
            jwt_['JWT_ACCESS_TOKEN'] = result.get("AccessToken")
            jwt_['JWT_USER_ID'] = decode.get("sub")
            jwt_['JWT_EXP'] = decode.get("exp")
            with open(JWT_JSON_FILE, 'w') as f:
                json.dump(jwt_, f)
            return True
        else:
            if not SILENT:
                print("Missing key in server JWT response.")
            if DEBUG:
                raise JWTError("Missing key in server response, server at:", AUTH_MANAGER_URL)
            return False
    except req.exceptions.RequestException as e:
        if not SILENT:
            print(f"JWT error: Unable to connect to Scailable servers. {e}")
        if DEBUG:
            raise JWTError("Unable to connect to Scailable servers.")
        return False


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

    if len(email) < 1 or len(password) < 1:
        if not SILENT:
            print("JWT error: no email and password provided.")
        if DEBUG:
            raise LoginError("No email or password provided.")
        return False

    try:
        result = {}
        # Build URL and headers for API request
        url: str = AUTH_MANAGER_URL + "/authenticate/signin"
        data: dict = {
            'Email': email,
            'Password': password
        }
        headers: dict = {
            'Content-Type': 'application/json'
        }
        # Send API request
        resp: req.models.Response = req.post(url=url, headers=headers, json=data)
        # Check if content type is JSON and at least 10 bytes long
        if 'json' in resp.headers.get('Content-Type') and 10 < len(resp.content) < 400:
            try:
                # See if able to decode the JSON
                result: dict = resp.json()
            except ValueError:
                if not SILENT:
                    print("Unable to decode JSON error.")
                if DEBUG:
                    raise LoginError(result.get("Unable to decode JSON error."))
                return False
        else:
            if not SILENT:
                print("Server at", AUTH_MANAGER_URL, "did not return a valid JSON document.")
            if DEBUG:
                raise LoginError("Server at", AUTH_MANAGER_URL, "did not return a valid JSON document.")
            return False

        if result.get("error") is not None:
            if not SILENT:
                print("JWT authentication error: The server generated an error: " + result.get("error"))
            if DEBUG:
                raise LoginError(result.get("JWT server error: " + result.get("error")))
            return False

        # If the JSON contains a RefreshToken, then ask for an AccessToken:
        if result.get('RefreshToken') is not None:
            decode = jwt.decode(result.get('RefreshToken'), options={"verify_signature": False})
            with open(JWT_JSON_FILE) as f:
                jwt_ = json.load(f)
            jwt_['JWT_REFRESH_TOKEN'] = result.get('RefreshToken')
            jwt_['JWT_REFRESH_EXP'] = decode.get("exp")
            with open(JWT_JSON_FILE, 'w') as f:
                json.dump(jwt_, f)
            os.makedirs(os.path.dirname(USER_CREDENTIALS), exist_ok=True)
            with open(USER_CREDENTIALS, "w+") as f:
                creds = {'Email': email, 'Password': password}
                json.dump(creds, f)
            return _refresh_jwt(result.get('RefreshToken'))
        else:
            # Token missing
            print(result.get('Message'))
            if not SILENT:
                print("Missing key in server JWT response.")
            if DEBUG:
                raise LoginError("Missing key in server response, server at:", AUTH_MANAGER_URL)
            return False

    except req.exceptions.RequestException as e:
        if not SILENT:
            print(f"JWT error: Unable to connect to Scailable servers. {e}")
        if DEBUG:
            raise LoginError("Unable to connect to Scailable servers.")
        return False


def get_user_details() -> dict:
    """get the user information
        Returns:
            Dictionary contains the user information
    """
    # Check if user is authenticated
    auth = _check_jwt()
    if auth:
        details = {}
        try:
            # Load JWT from file
            with open(JWT_JSON_FILE) as f:
                jwt_ = json.load(f)
            uuid = jwt_['JWT_USER_ID']
            # Build URL and headers for API request
            url = f"{AUTH_MANAGER_URL}/user/{uuid}"
            headers = {
                'Authorization': f"Bearer {jwt_['JWT_ACCESS_TOKEN']}"
            }
            # Send API request
            resp = req.get(url=url, headers=headers)
            if 'json' in resp.headers.get('Content-Type'):
                try:
                    # See if able to decode the JSON
                    details = resp.json()
                except ValueError:  # simplejson.decoder.JSONDecodeError
                    if not SILENT:
                        print("Unable to decode JSON error.")
                    if DEBUG:
                        raise UserDetailsError(details.get("Unable to decode JSON error."))
        except req.exceptions.RequestException as e:
            print(f"Error occurred while fetching user details: {e}")
        return details


def log_out() -> bool:
    """Log the user out .
        Returns:
            True if the user is successfully logged out
    """

    # Check if user is authenticated
    auth = _check_jwt()
    if auth:
        # Load JWT from file
        with open(JWT_JSON_FILE) as f:
            jwt_ = json.load(f)
        # Build URL and headers for API request
        url = f"{AUTH_MANAGER_URL}/authenticate/signout"
        headers = {
            'Authorization': f"Bearer {jwt_['JWT_ACCESS_TOKEN']}"
        }
        # Send API request
        resp: req.models.Response = req.post(url=url, headers=headers)
        if resp.status_code == 200:
            return True
        else:
            return False


def register_(name: str, company: str, email: str, password: str, job_title: str = None,
              phone_number: str = None, newsletter_opt_in: bool = True, accept_eula: bool = True) -> bool:
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
            newsletter_opt_in: Bool (whether to add this email address to the newsletter)
            accept_eula: Bool (Agreement to the EULA)

        Returns:
            True if sign-up is successful.
   """
    # Build URL and headers for API request
    url: str = AUTH_MANAGER_URL + "/user"
    data: dict = {
        'Email': email,
        'Password': password,
        'Name': name,
        'Company': company,
        'PhoneNumber': phone_number,
        'JobTitle': job_title,
        'NewsletterOptIn': newsletter_opt_in,
        'AcceptEULA': accept_eula
    }
    headers: dict = {
        'Content-Type': 'application/json'
    }
    result = {}
    # Try connecting to server:
    try:
        # Send API request
        resp: req.models.Response = req.post(url=url, headers=headers, json=data)
        # Check if content type is JSON
        if 'json' in resp.headers.get('Content-Type'):
            try:
                # See if able to decode the JSON
                result: dict = resp.json()
            except ValueError:
                if not SILENT:
                    print("Unable to decode JSON error.")
                if DEBUG:
                    raise RegisterError(result.get("Unable to decode JSON error."))
                return False
        else:
            if not SILENT:
                print("Server at", AUTH_MANAGER_URL, "did not return a valid JSON document.")
            if DEBUG:
                raise RegisterError("Server at", AUTH_MANAGER_URL, "did not return a valid JSON document.")
            return False

        if result.get("error") is not None:
            if not SILENT:
                print("JWT authentication error: The server generated an error: " + result.get("error"))
            if DEBUG:
                raise RegisterError(result.get("JWT server error: " + result.get("error")))
            return False

        # If a JSON contains a token, all is ok:
        if result.get('RefreshToken') is not None:
            os.makedirs(os.path.dirname(USER_CREDENTIALS), exist_ok=True)  # create the folder if it does not exist.
            with open(USER_CREDENTIALS, "w+") as f:
                creds = {'Email': email, 'Password': password}
                json.dump(creds, f)
            _refresh_jwt(result.get('RefreshToken'))
            return True
        else:
            # Token missing
            print(result.get('Message'))
            if not SILENT:
                print("Missing key in server JWT response.")
            if DEBUG:
                raise RegisterError("Missing key in server response, server at:", AUTH_MANAGER_URL)
            return False

    except req.exceptions.RequestException as e:
        if not SILENT:
            print(f"JWT error: Unable to connect to Scailable servers. {e}")
        if DEBUG:
            raise RegisterError("Unable to connect to Scailable servers.")
        return False


def set_new_password(current_password: str, new_password: str) -> bool:
    """Set a new password for user account
    Args:
        current_password: A string (the current account's password)
        new_password: A string (the new password to set)
    Returns:
        True if the password is strong, False otherwise
    """

    auth = _check_jwt()
    result = {}
    if auth:
        try:
            with open(USER_CREDENTIALS, "r") as f:
                credentials = json.load(f)
                password = credentials['Password']
        except FileNotFoundError:
            pass
        if password == current_password:
            with open(JWT_JSON_FILE) as f:
                jwt_ = json.load(f)
            url = f"{AUTH_MANAGER_URL}/authenticate/update-password"
            headers = {
                'Content-Type': 'application/json',
                'Authorization': f"Bearer {jwt_['JWT_ACCESS_TOKEN']}"
            }
            data = {
                'CurrentPassword': current_password,
                'NewPassword': new_password
            }
            try:
                resp: req.models.Response = req.post(url=url, headers=headers, json=data)

                # Check if content type is JSON
                if 'json' in resp.headers.get('Content-Type'):
                    try:
                        # See if able to decode the JSON
                        result: dict = resp.json()
                    except ValueError:
                        if not SILENT:
                            print("Unable to decode JSON error.")
                        if DEBUG:
                            raise PwdError(result.get("Unable to decode JSON error."))
                        return False
                else:
                    if not SILENT:
                        print("Server at", AUTH_MANAGER_URL, "did not return a valid JSON document.")
                    if DEBUG:
                        raise PwdError("Server at", AUTH_MANAGER_URL, "did not return a valid JSON document.")
                    return False
                # If the JSON contains a message that the password has been reset
                if result.get('Message') == 'Your password has been reset!':
                    with open(USER_CREDENTIALS, "w+") as f:
                        creds = {'Password': new_password}
                        json.dump(creds, f)
                    return True
            except req.exceptions.RequestException as e:
                if not SILENT:
                    print(f"JWT error: Unable to connect to Scailable servers. {e}")
                if DEBUG:
                    raise PwdError("Unable to connect to Scailable servers.")
                return False
        else:
            if not SILENT:
                print("Incorrect password.")
                return False
    else:
        return False


def password_reset(email: str) -> bool:
    """Send a password-reset email.
    Args:
        email: A string
    Returns:
        True if the password-reset email is sent
    """

    result = {}
    try:
        # Build URL and headers for API request
        url = f"{AUTH_MANAGER_URL}/authenticate/forgot-password"
        headers = {
            'Content-Type': 'application/json'
        }
        data = {
            'Email': email,
        }
        # Send API request
        resp: req.models.Response = req.post(url=url, headers=headers, json=data)
        # Check if content type is JSON
        if 'json' in resp.headers.get('Content-Type'):
            try:
                # See if able to decode the JSON
                result: dict = resp.json()
            except ValueError:  # simplejson.decoder.JSONDecodeError
                if not SILENT:
                    print("Unable to decode JSON error.")
                if DEBUG:
                    raise PwdError(result.get("Unable to decode JSON error."))
                return False
        else:
            if not SILENT:
                print("Server at", AUTH_MANAGER_URL, "did not return a valid JSON document.")
            if DEBUG:
                raise PwdError("Server at", AUTH_MANAGER_URL, "did not return a valid JSON document.")
            return False
        # If the JSON contains a message that the password-reset is sent:
        if result.get('Message') == 'Password sent if user exists.':
            return True
    except req.exceptions.RequestException as e:
        if not SILENT:
            print(f"JWT error: Unable to connect to Scailable servers. {e}")
        if DEBUG:
            raise PwdError("Unable to connect to Scailable servers.")
        return False


if __name__ == '__main__':
    print("No command line options for auth.py.")
