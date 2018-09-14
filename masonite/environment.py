"""Module for the LoadEnvironment class.
"""

import os
from pathlib import Path

from dotenv import find_dotenv, load_dotenv


class LoadEnvironment:
    """This class is used for loading the environment from .env and .env.* files.
    """

    def __init__(self, env=None, override=True, only=None):
        """LoadEnvironment constructor.

        Keyword Arguments:
            env {string} -- An additional environment file that you want to load. (default: {None})
            override {bool} -- Whether or not the environment variables found should overwrite existing ones. (default: {False})
            only {string} -- If this is set then it will only load that environment. (default: {None})
        """

        if only:
            self._load_environment(only, override=override)
            return

        env_path = str(Path('.') / '.env')
        load_dotenv(env_path, override=override)

        if os.environ.get('APP_ENV'):
            self._load_environment(os.environ.get(
                'APP_ENV'), override=override)
        if env:
            self._load_environment(env, override=override)

    def _load_environment(self, env, override=False):
        """Load the environment depending on the env file.

        Arguments:
            env {string} -- Name of the environment file to load from

        Keyword Arguments:
            override {bool} -- Whether the environment file should overwrite existing environment keys. (default: {False})
        """

        env_path = str(Path('.') / '.env.{}'.format(env))
        load_dotenv(dotenv_path=env_path, override=override)
