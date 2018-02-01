import os
import sys

from config import application

def test_env_file_exists():
    ''' Test should be True if .env file is present '''
    assert os.path.exists(os.path.join(application.BASE_DIRECTORY, '.env')), '.env file should exist'
