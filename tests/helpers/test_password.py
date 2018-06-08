from masonite.helpers import password

class TestPassword:

    def test_password_returns_bcrypted_password(self):
        assert password('secret') != 'secret'