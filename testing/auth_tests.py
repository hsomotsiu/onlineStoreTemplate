from authentication.auth_tools import hash_password, reset_password
from app import login

def test_hash_password_generates_salt():
    """
    Tests that the hash_password function generates a salt when one is not provided.
    salt: encoding pass

    args:
        - None

    returns:
        - error_report: a tuple containing a boolean and a string, 
          where the boolean is True if the test passed and False if it failed, 
          and the string is the error report.
    """
    salt, _ = hash_password("password")
    if salt is None:
        error = f"Error in test_hash_password_salt_generation: Salt was not generated.\n  - Actual: {salt}"
        return False, error
    else:
        return True, "Salt was generated."


def test_salt_length():
    """
    Tests that the salt is 32 characters long. Change this test if you change the salt length.

    args:
        - None

    returns:
        - error_report: a tuple containing a boolean and a string, 
          where the boolean is True if the test passed and False if it failed, 
          and the string is the error report.
    """

    salt, _ = hash_password("password")
    if len(salt) != 32:
        error = f"Error in test_salt_length: Salt is not 32 characters long.\n  - Actual: {len(salt)}"
        return False, error
    else:
        return True, "Salt is 32 characters long."


def test_hash_password_returns_given_salt():
    """
    Tests that the hash_password function returns the given salt when one is provided.

    args:
        - None

    returns:
        - error_report: a tuple containing a boolean and a string, 
          where the boolean is True if the test passed and False if it failed, 
          and the string is the error report.
    """

    first_salt, _ = hash_password("password")
    second_salt, _ = hash_password("password", first_salt)

    if first_salt != second_salt:
        error = f"Error in test_hash_password_returns_given_salt: Salt was not returned.\n  - Actual: {second_salt}"
        return False, error
    else:
        return True, "Salt was returned correctly."


def test_hash_password_uses_given_salt():
    """
    Tests that the hash_password function returns different hashes when given the same password and salt.

    args:
        - None

    returns:
        - error_report: a tuple containing a boolean and a string, 
          where the boolean is True if the test passed and False if it failed, 
          and the string is the error report.
    """

    salt, first_hash = hash_password("password")
    _, second_hash = hash_password("password", salt)

    if first_hash != second_hash:
        error = f"Error in test_hash_password_returns_different_hashes: Hashes are not the same.\n  - Expected: {first_hash}\n  - Actual: {second_hash}"
        return False, error
    else:
        return True, "Hashes are different."


def test_reset_password_generates_new_password():
    """
    Tests that the reset_password function generates a new password hash and salt.

    args:
        - None

    returns:
        - error_report: a tuple containing a boolean and a string,
          where the boolean is True if the test passed and False if it failed,
          and the string is the error report.
    """
    old_salt, old_hash = hash_password("old_password")
    new_salt, new_hash = reset_password("old_password", old_salt)

    if old_hash == new_hash:
        error = f"Error in test_reset_password_generates_new_password: Password hash was not changed.\n  - Old Hash: {old_hash}\n  - New Hash: {new_hash}"
        return False, error
    else:
        return True, "Password hash was changed."
    


def test_login_as_admin():
    """
    Tests the login function using the admin credentials.

    args:
        - None

    returns:
        - error_report: a tuple containing a boolean and a string,
          where the boolean is True if the test passed and False if it failed,
          and the string is the error report.
    """
    admin_username = "admin"
    admin_password = "admin"

    # Hash the admin password and store it for comparison
    admin_salt, admin_hash = hash_password(admin_password)

    # Simulate login attempt
    login_successful = login(admin_username, admin_password, admin_salt, admin_hash)

    if not login_successful:
        error = "Error in test_login_as_admin: Admin login failed."
        return False, error
    else:
        return True, "Admin login succeeded."