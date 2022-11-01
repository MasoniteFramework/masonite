"""Masonite Environments management."""
import os
from pathlib import Path
from typing import Any


class LoadEnvironment:
    """This class is used for loading the environment from .env and .env.* files."""

    def __init__(
        self, environment: str = None, override: bool = True, only: str = None
    ):
        """Load the environment from .env files.
        - If an environment is provided, .env.{environment} will be loaded additionally
        - If override is enabled, environment variables will overwrite existing ones
        - If only is provided, it will only the environment .env.{environment}
        """
        from dotenv import load_dotenv

        self.env = load_dotenv

        # load only .env.{only} environment file
        if only:
            self._load_environment(only, override=override)
            return

        # load base .env file
        env_path = str(Path(".") / ".env")
        self.env(env_path, override=override)

        # then load .env.{APP_ENV} if APP_ENV is defined
        if os.environ.get("APP_ENV"):
            self._load_environment(os.environ.get("APP_ENV"), override=override)

        # then load .env.{environment} if defined
        if environment:
            self._load_environment(environment, override=override)

        # then load .env.testing if running unit tests
        if "PYTEST_CURRENT_TEST" in os.environ:
            self._load_environment("testing", override=override)

    def _load_environment(self, environment: str, override: bool = False) -> None:
        """Load the environment file named .env.{environment}. If override is enabled, environment
        variables found in this file will overwrite existing ones."""
        env_path = str(Path(".") / ".env.{}".format(environment))
        self.env(dotenv_path=env_path, override=override)


def env(name: str, default: str = "", cast: bool = True) -> Any:
    """Get the environment variable with the given name or get the default provided value. If cast
    is enabled: if type can be inferred then the value will be casted to the inferred type."""

    env_var = os.getenv(name, default)
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
