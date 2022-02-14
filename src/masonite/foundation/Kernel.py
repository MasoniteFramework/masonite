import os
from cleo import Application as CommandApplication

from .response_handler import response_handler
from .. import __version__
from ..commands import (
    TinkerCommand,
    CommandCapsule,
    KeyCommand,
    ServeCommand,
    QueueWorkCommand,
    QueueRetryCommand,
    QueueTableCommand,
    QueueFailedCommand,
    AuthCommand,
    MakePolicyCommand,
    MakeControllerCommand,
    MakeJobCommand,
    MakeMailableCommand,
    MakeProviderCommand,
    PublishPackageCommand,
    MakeTestCommand,
    DownCommand,
    UpCommand,
    MakeCommandCommand,
    MakeViewCommand,
    MakeMiddlewareCommand,
    PresetCommand,
)
from ..environment import LoadEnvironment
from ..middleware import MiddlewareCapsule
from ..routes import Router
from ..loader import Loader

from ..tests.HttpTestResponse import HttpTestResponse
from ..tests.TestResponseCapsule import TestResponseCapsule


class Kernel:
    def __init__(self, app):
        self.application = app

    def register(self):
        self.load_environment()
        self.register_framework()
        self.register_commands()
        self.register_testing()

    def load_environment(self):
        LoadEnvironment()

    def register_framework(self):
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

    def register_commands(self):
        self.application.bind(
            "commands",
            CommandCapsule(CommandApplication("Masonite", __version__)).add(
                TinkerCommand(),
                KeyCommand(),
                ServeCommand(self.application),
                QueueWorkCommand(self.application),
                QueueRetryCommand(self.application),
                QueueFailedCommand(),
                QueueTableCommand(),
                AuthCommand(self.application),
                MakePolicyCommand(self.application),
                MakeControllerCommand(self.application),
                MakeJobCommand(self.application),
                MakeMailableCommand(self.application),
                MakeProviderCommand(self.application),
                PublishPackageCommand(self.application),
                MakeTestCommand(self.application),
                DownCommand(),
                UpCommand(),
                MakeCommandCommand(self.application),
                MakeViewCommand(self.application),
                MakeMiddlewareCommand(self.application),
                PresetCommand(self.application),
            ),
        )

    def register_testing(self):
        test_response = TestResponseCapsule(HttpTestResponse)
        self.application.bind("tests.response", test_response)
