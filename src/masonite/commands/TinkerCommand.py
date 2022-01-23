"""Starts Interactive Console Command."""
import os
import code
import sys
import pendulum

from ..environment import env
from ..configuration import config
from ..utils.collections import collect
from ..utils.structures import load, data_get
from ..utils.location import base_path, config_path, models_path
from ..helpers import optional, url
from ..facades import Loader
from .. import __version__
from .Command import Command


BANNER = """ -------------------------------
| Masonite Python \033[92m{}\033[0m Console |
 -------------------------------
Masonite Version: \033[92m{}\033[0m,
Environment: \033[92m{}\033[0m,
Debug Mode: \033[92m{}\033[0m,
This interactive console has the following things imported:
    -\033[92m app (container), \033[0m
    - Utils:\033[92m {} \033[0m
    - Models:\033[92m {} \033[0m

Type `exit()` to exit."""


class TinkerCommand(Command):
    """
    Run a python shell with the container pre-loaded.

    tinker
        {--i|ipython : Run a IPython shell}
        {--d|directory=? : Override the directory to auto-load models from}
    """

    def handle(self):
        from wsgi import application
        from masoniteorm.models import Model

        python_version = "{}.{}.{}".format(
            sys.version_info.major, sys.version_info.minor, sys.version_info.micro
        )
        models_directory = self.option("directory") or models_path()
        models = Loader.find_all(Model, models_directory)
        helpers = {
            "app": application,
            "env": env,
            "pendulum": pendulum,
            "optional": optional,
            "collect": collect,
            "url": url.url,
            "asset": url.asset,
            "route": url.route,
            "load": load,
            "config": config,
            "data_get": data_get,
            "base_path": base_path,
            "config_path": config_path,
        }
        banner = BANNER.format(
            python_version,
            __version__,
            os.getenv("APP_ENV"),
            "on" if application.is_debug() else "off",
            ", ".join(list(helpers.keys())[1:]),
            ", ".join(models.keys()),
        )
        context = {**helpers, **models}

        if self.option("ipython"):
            try:
                import IPython
            except ImportError:
                raise ModuleNotFoundError(
                    "Could not find the 'IPython' library. Run 'pip install ipython' to fix this."
                )
            from traitlets.config import Config

            c = Config()
            c.TerminalInteractiveShell.banner1 = banner
            IPython.start_ipython(argv=[], user_ns=context, config=c)
        else:
            console = code.InteractiveConsole(context)
            try:
                import readline
            except ImportError:
                pass
            # When not using IPython, PYTHONSTARTUP is not used by default, so load any
            # scripts defined in this var at startup
            startup_file = os.environ.get("PYTHONSTARTUP")
            if startup_file:
                if os.path.isfile(startup_file):
                    with open(startup_file, "r") as f:
                        compiled_code = code.compile_command(
                            f.read(), startup_file, "exec"
                        )
                        console.runcode(compiled_code)
            console.interact(banner, exitmsg="Goodbye !")
