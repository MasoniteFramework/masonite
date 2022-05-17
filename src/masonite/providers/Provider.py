from typing import TYPE_CHECKING

if TYPE_CHECKING:
    from ..foundation import Application


class Provider:
    def __init__(self, application: "Application") -> None:
        self.application = application

    def register(self) -> None:
        pass

    def boot(self) -> None:
        pass
