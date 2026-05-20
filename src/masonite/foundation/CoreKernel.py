from typing import TYPE_CHECKING

if TYPE_CHECKING:
    from .Application import Application


class CoreKernel:
    def __init__(self, app: "Application"):
        self.application = app
        self._register_core()

    def register(self) -> None:
        pass

    def _register_core(self) -> None:
        """Register core Masonite features in the project."""
        self._register_framework()
        self._register_capsules()

    def _register_framework(self) -> None:
        """Register Core Framework requirements"""
        import os
        from .response_handler import response_handler
        from ..environment import LoadEnvironment

        LoadEnvironment()
        self.application.set_response_handler(response_handler)
        self.application.use_storage_path(
            os.path.join(self.application.base_path, "storage")
        )

    def _register_capsules(self) -> None:
        """Register the minimum required capsules."""
        from cleo import Application as CommandApplication
        from .. import __version__
        from ..commands.CommandCapsule import CommandCapsule
        from ..middleware import MiddlewareCapsule
        from ..loader import Loader
        from ..routes import Router

        self.application.bind("middleware", MiddlewareCapsule())
        self.application.bind("loader", Loader())
        self.application.bind("router", Router())
        self.application.bind(
            "commands",
            CommandCapsule(CommandApplication("Masonite", __version__))
        )
