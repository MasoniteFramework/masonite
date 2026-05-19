from typing import TYPE_CHECKING

from .CoreKernel import CoreKernel

if TYPE_CHECKING:
    from .Application import Application


class Kernel(CoreKernel):
    def __init__(self, app: "Application"):
        super().__init__(app)

    def register(self) -> None:
        """Register Additional Masonite features in the project"""
        super().register()
        self.register_commands()

    def register_commands(self) -> None:
        from ..commands import (
            AuthCommand,
            DownCommand,
            KeyCommand,
            MakeCommandCommand,
            MakeControllerCommand,
            MakeJobCommand,
            MakeMailableCommand,
            MakeMiddlewareCommand,
            MakePolicyCommand,
            MakeProviderCommand,
            MakeTestCommand,
            MakeViewCommand,
            PresetCommand,
            PublishPackageCommand,
            QueueFailedCommand,
            QueueRetryCommand,
            QueueTableCommand,
            QueueWorkCommand,
            ServeCommand,
            TinkerCommand,
            UpCommand,
        )

        self.application.make("commands").add(
            AuthCommand(self.application),
            DownCommand(),
            KeyCommand(),
            MakeCommandCommand(self.application),
            MakeControllerCommand(self.application),
            MakeJobCommand(self.application),
            MakeMailableCommand(self.application),
            MakeMiddlewareCommand(self.application),
            MakePolicyCommand(self.application),
            MakeProviderCommand(self.application),
            MakeTestCommand(self.application),
            MakeViewCommand(self.application),
            PresetCommand(self.application),
            PublishPackageCommand(self.application),
            QueueFailedCommand(),
            QueueRetryCommand(self.application),
            QueueTableCommand(),
            QueueWorkCommand(self.application),
            ServeCommand(self.application),
            TinkerCommand(),
            UpCommand(),
        )
