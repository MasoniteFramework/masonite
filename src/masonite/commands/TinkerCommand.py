"""Starts Interactive Console Command."""
import code
import sys
import pendulum
from cleo import Command

from ..environment import env
from ..configuration import config
from ..utils.collections import collect
from ..utils.structures import load, data_get
from ..utils.location import base_path, config_path
from ..helpers import optional, url
from ..facades import Loader


BANNER = """Masonite Python \033[92m {} \033[0m Console
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
        {--d|directory=app/models : Directory to auto-load models from}
    """

    def handle(self):
        from wsgi import application
        from masoniteorm.models import Model

        version = "{}.{}.{}".format(
            sys.version_info.major, sys.version_info.minor, sys.version_info.micro
        )
        models = Loader.find_all(Model, self.option("directory"))
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
            version,
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
            code.interact(banner=banner, local=context)
