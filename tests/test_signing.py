from masonite.auth.Sign import Sign
from cryptography.fernet import Fernet
from masonite.exceptions import InvalidSecretKey
import pytest


class TestSigning:

    def setup_method(self):
        self.secret_key = Fernet.generate_key()

    def test_unsigning_returns_decrypted_value_with_parameter(self):
        s = Sign(self.secret_key)
        assert s.unsign(s.sign('value')) == 'value'
    
    def test_unsigning_returns_decrypted_value_without_parameter(self):
        s = Sign(self.secret_key)
        assert s.unsign(s.sign('value')) == 'value'


    def test_unsigning_without_value(self):
        s = Sign(self.secret_key)
        s.sign('value')
        assert s.unsign() == 'value'


    def test_sign_without_specifying_key(self):
        s = Sign()

        assert s.key == 'NCTpkICMlTXie5te9nJniMj9aVbPM6lsjeq5iDZ0dqY='

    def test_sign_incorrect_padding(self):
        with pytest.raises(InvalidSecretKey):
            padded_secret_key = "AQAAQDhAAMAAQAAAAAAAAthAAAAJDczODFmZDM2LTNiOTYtNDVmYS04MjQ2LWRkYzJkMmViYjQ2YQ==="
            s = Sign(padded_secret_key)
            assert s.sign('value')