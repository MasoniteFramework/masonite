import os
from typing import TYPE_CHECKING

if TYPE_CHECKING:
    from .Application import Application


class CoreKernel:
    def __init__(self, app: "Application"):
        self.application = app
        self.register_core()

    def register_core(self) -> None:
        """Register core Masonite features in the project."""
        self.load_environment()
        self.register_framework()
        self.register_command_capsule()

    def load_environment(self) -> None:
        """Load environment variables into the application."""
        from ..environment import LoadEnvironment
        LoadEnvironment()

    def register_framework(self) -> None:
        """Register Core Fraamework requirements"""
        from .response_handler import response_handler
        from ..middleware import MiddlewareCapsule
        from ..routes import Router
        from ..loader import Loader

        self.application.set_response_handler(response_handler)
        self.application.use_storage_path(
            os.path.join(self.application.base_path, "storage")
        )
        self.application.bind("middleware", MiddlewareCapsule())
        self.application.bind(
            "router",
            Router(),
        )
        self.application.bind("loader", Loader())

    def register_command_capsule(self) -> None:
        """Register the 'commands' binding in the application."""
        from cleo import Application as CommandApplication
        from ..commands import CommandCapsule
        from .. import __version__

        self.application.bind(
            "commands",
            CommandCapsule(CommandApplication("Masonite", __version__))
        )
