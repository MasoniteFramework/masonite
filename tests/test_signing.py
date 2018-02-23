from masonite.auth.Sign import Sign
from cryptography.fernet import Fernet

SECRET_KEY = Fernet.generate_key()


def test_unsigning_returns_decrypted_value_with_parameter():
    s = Sign(SECRET_KEY)
    assert s.unsign(s.sign('value')) == 'value'


def test_unsigning_returns_decrypted_value_without_parameter():
    s = Sign(SECRET_KEY)
    assert s.unsign(s.sign('value')) == 'value'


def test_unsigning_without_value():
    s = Sign(SECRET_KEY)
    s.sign('value')
    assert s.unsign() == 'value'


def test_sign_without_specifying_key():
    s = Sign()

    assert s.key == 'NCTpkICMlTXie5te9nJniMj9aVbPM6lsjeq5iDZ0dqY='
