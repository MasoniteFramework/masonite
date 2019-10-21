from masonite.auth import Sign


def sign(value):
    """Shortcut for Sign class.

    Arguments:
        value {string} -- The value that is going to be encrypted

    Returns:
        string -- The string value after encryption.
    """
    return Sign().sign(value)


def encrypt(value):
    """Shortcut for Sign class sign method.

    Arguments:
        value {string} -- The value that is going to be encrypted

    Returns:
        string -- The string value after encryption.
    """
    return sign(value)


def unsign(value):
    """Shortcut for Sign class unsign method.

    Arguments:
        value {string} -- The value that is going to be decrypted

    Returns:
        string -- The string value after decryption.
    """
    return Sign().unsign(value)


def decrypt(value):
    """Shortcut for Sign class unsign method.

    Arguments:
        value {string} -- The value that is going to be decrypted

    Returns:
        string -- The string value after decryption.
    """
    return unsign(value)
