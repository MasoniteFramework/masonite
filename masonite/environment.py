from dotenv import find_dotenv, load_dotenv
from pathlib import Path  # python3 only
import os

class LoadEnvironment:

    def __init__(self, env=None):
        load_dotenv(find_dotenv())
        if env:
            env_path = Path('.') / '.env.{}'.format(env)
            load_dotenv(dotenv_path=env_path)
        if os.environ.get('APP_ENV'):
            env_path = Path('.') / '.env.{}'.format(os.environ.get('APP_ENV'))
            load_dotenv(dotenv_path=env_path)
