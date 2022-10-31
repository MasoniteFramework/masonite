import os

from .. import Middleware
from ...utils.location import base_path
from ...facades import View


class MaintenanceModeMiddleware(Middleware):
    def before(self, request, response):
        down = os.path.exists(base_path(".down"))
        if down is True:
            return response.view(View.render("maintenance"), status=503)
        return request

    def after(self, request, _):
        return request
