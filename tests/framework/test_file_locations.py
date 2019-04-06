import os
from unittest import TestCase

from config import application


class TestFileLocations(TestCase):

    def test_env_file_exists(self):
        """ Test should be True if .env file is present """
        self.assertTrue(os.path.exists(os.path.join(application.BASE_DIRECTORY, '.env')), '.env file should exist')
