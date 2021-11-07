"""Cryptographic Signing Module."""
import binascii

from cryptography.fernet import Fernet, InvalidToken as CryptographyInvalidToken

from ..exceptions import InvalidSecretKey, InvalidToken


class Sign:
    """Cryptographic signing class."""

    def __init__(self, key=None):
        """Sign constructor.

        Keyword Arguments:
            key {string} -- The secret key to use. If nothing is passed it then it will use
                            the secret key from the config file. (default: {None})

        Raises:
            InvalidSecretKey -- Thrown if the secret key does not exist.
        """
        if key:
            self.key = key
        else:
            from wsgi import application

            self.key = application.make("key")

        if not self.key:
            raise InvalidSecretKey(
                "The encryption key passed in is: None. Be sure there is a secret key present in your .env file or your config/application.py file."
            )

        self.encryption = None

    def sign(self, value):
        """Sign a value using the secret key.

        Arguments:
            value {string} -- The value to be encrypted.

        Returns:
            string -- Returns the encrypted value.

        Raises:
            InvalidSecretKey -- Thrown if the secret key has incorrect padding.
        """
        try:
            f = Fernet(self.key)
        except (binascii.Error, ValueError):
            raise InvalidSecretKey(
                "You have passed an invalid secret key of: {}. Make sure you have correctly added your secret key.".format(
                    self.key
                )
            )

        self.encryption = f.encrypt(bytes(str(value), "utf-8"))
        return self.encryption.decode("utf-8")

    def unsign(self, value=None):
        """Unsign the value using the secret key.

        Keyword Arguments:
            value {string} -- The value to be unencrypted. (default: {None})

        Returns:
            string -- Returns the unencrypted value.
        """
        f = Fernet(self.key)

        if not value:
            return f.decrypt(self.encryption).decode("utf-8")
        try:
            return f.decrypt(bytes(str(value), "utf-8")).decode("utf-8")
        except CryptographyInvalidToken as e:
            raise InvalidToken("Invalid Cryptographic Token") from e
