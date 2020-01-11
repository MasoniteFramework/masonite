import unittest

from cryptography.fernet import Fernet

from src.masonite.auth.Sign import Sign
from src.masonite.exceptions import InvalidSecretKey


class TestSigning(unittest.TestCase):

    def setUp(self):
        self.secret_key = Fernet.generate_key()
        self.signed = Sign(self.secret_key)

    def test_unsigning_returns_decrypted_value_with_parameter(self):
        self.assertEqual(self.signed.unsign(self.signed.sign('value')), 'value')

    def test_unsigning_returns_decrypted_value_without_parameter(self):
        self.assertEqual(self.signed.unsign(self.signed.sign('value')), 'value')

    def test_unsigning_without_value(self):
        self.signed.sign('value')
        self.assertEqual(self.signed.unsign(), 'value')

    def test_sign_incorrect_padding(self):
        with self.assertRaises(InvalidSecretKey):
            padded_secret_key = "AQAAQDhAAMAAQYS04MjQ2LWRkYzJkMmViYjQ2YQ==="
            assert Sign(padded_secret_key).sign('value')
