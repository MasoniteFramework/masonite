"""Password Helper Module."""

import bcrypt


def password(password):
    """Bcrypt a string.

    Useful for storing passwords in a database.

    Arguments:
        password {string} -- A string like a users plain text password to be bcrypted.

    Returns:
        string -- The encrypted string.
    """
    return bytes(bcrypt.hashpw(
        bytes(password, 'utf-8'), bcrypt.gensalt()
    )).decode('utf-8')
