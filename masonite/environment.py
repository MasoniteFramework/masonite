from dotenv import find_dotenv, load_dotenv
from pathlib import Path 
import os

class LoadEnvironment:

    def __init__(self, env=None, override=False, only=None):
        if only:
            self._load_environment(only, override=override)
            return

        env_path = str(Path('.') / '.env')
        load_dotenv(env_path, override=override)

        if os.environ.get('APP_ENV'):
            self._load_environment(os.environ.get('APP_ENV'), override=override)
        if env:
            self._load_environment(env, override=override)

    def _load_environment(self, env, override=False):
        env_path = str(Path('.') / '.env.{}'.format(env))
        load_dotenv(dotenv_path=env_path, override=override)
