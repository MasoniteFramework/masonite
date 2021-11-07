"""Module for the LoadEnvironment class."""

import os
import sys
from pathlib import Path


class LoadEnvironment:
    """This class is used for loading the environment from .env and .env.* files."""

    def __init__(self, environment=None, override=True, only=None):
        """LoadEnvironment constructor.

        Keyword Arguments:
            env {string} -- An additional environment file that you want to load. (default: {None})
            override {bool} -- Whether or not the environment variables found should overwrite existing ones. (default: {False})
            only {string} -- If this is set then it will only load that environment. (default: {None})
        """
        from dotenv import load_dotenv

        self.env = load_dotenv

        if only:
            self._load_environment(only, override=override)
            return

        env_path = str(Path(".") / ".env")
        self.env(env_path, override=override)

        if os.environ.get("APP_ENV"):
            self._load_environment(os.environ.get("APP_ENV"), override=override)
        if environment:
            self._load_environment(environment, override=override)

        if "pytest" in sys.modules:
            self._load_environment("testing", override=override)

    def _load_environment(self, environment, override=False):
        """Load the environment depending on the env file.

        Arguments:
            environment {string} -- Name of the environment file to load from

        Keyword Arguments:
            override {bool} -- Whether the environment file should overwrite existing environment keys. (default: {False})
        """
        env_path = str(Path(".") / ".env.{}".format(environment))
        self.env(dotenv_path=env_path, override=override)


def env(value, default="", cast=True):
    """Helper to retrieve the value of an environment variable or returns
    a default value. In addition, if type can be inferred then the value can be casted to the
    inferred type."""
    env_var = os.getenv(value, default)

    if not cast:
        return env_var

    if env_var == "":
        env_var = default

    if isinstance(env_var, bool):
        return env_var
    elif env_var is None:
        return None
    elif env_var.isnumeric():
        return int(env_var)
    elif env_var in ("false", "False"):
        return False
    elif env_var in ("true", "True"):
        return True
    else:
        return env_var
