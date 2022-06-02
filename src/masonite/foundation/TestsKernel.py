from typing import TYPE_CHECKING

if TYPE_CHECKING:
    from .Application import Application

from ..tests.HttpTestResponse import HttpTestResponse
from ..tests.TestResponseCapsule import TestResponseCapsule


class TestsKernel:
    def __init__(self, app: "Application"):
        self.application = app

    def register(self) -> None:
        """Register Tests."""
        self.register_testing()

    def register_testing(self) -> None:
        test_response = TestResponseCapsule(HttpTestResponse)
        self.application.bind("tests.response", test_response)
