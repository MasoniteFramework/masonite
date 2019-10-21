from src.masonite.helpers import password
import unittest


class TestPassword(unittest.TestCase):

    def test_password_returns_bcrypted_password(self):
        self.assertNotEqual(password('secret'), 'secret')
        self.assertIsInstance(password('secret'), str)
