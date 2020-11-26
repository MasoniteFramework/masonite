"""Maintainance Mode Middleware."""
import os
from ..response import Response
from config import application


class MaintenanceModeMiddleware:
    def __init__(self, response: Response):
        self.response = response

    def before(self):
        down = os.path.exists(
            os.path.join(application.BASE_DIRECTORY, "bootstrap/down")
        )
        if down is True:
            self.response.status(503)
