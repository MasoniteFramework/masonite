import os

from masonite.testing import UnitTest

from config import application


class TestFramework(UnitTest):

    def test_env_file_exists(self):
        """Test should be True if .env file is present."""
        assert os.path.exists(os.path.join(application.BASE_DIRECTORY, '.env')), '.env file should exist'
