"""Starts Interactive Console Command."""
import code
import sys
from cleo import Command

from ..environment import env
from ..utils.collections import collect
from ..utils.structures import load, data_get
from ..utils.location import base_path, config_path
from ..helpers import optional, url
from ..facades import Loader


BANNER = """Masonite Python \033[92m {} \033[0m Console
This interactive console has the following things imported:
    -\033[92m app(container), \033[0m
    - Utils:\033[92m {}, \033[0m
    - Models:\033[92m {}, \033[0m

Type `exit()` to exit."""


class TinkerCommand(Command):
    """
    Run a python shell with the container pre-loaded.

    tinker
        {--i|ipython : Run a IPython shell}
    """

    def handle(self):
        from wsgi import application
        from masoniteorm.models import Model

        version = "{}.{}.{}".format(
            sys.version_info.major, sys.version_info.minor, sys.version_info.micro
        )
        models = Loader.find_all(Model, "tests/integrations/app")
        banner = BANNER.format(
            version,
            "env, optional, load, collect, url, asset, route, load, data_get, base_path, config_path",
            ",".join(models.keys()),
        )
        helpers = {
            "app": application,
            "env": env,
            "optional": optional,
            "collect": collect,
            "url": url.url,
            "asset": url.asset,
            "route": url.route,
            "load": load,
            "data_get": data_get,
            "base_path": base_path,
            "config_path": config_path,
        }
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
