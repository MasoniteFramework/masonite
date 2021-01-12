"""A StatusProvider Service Provider."""

import json

from ..helpers import config
from ..provider import ServiceProvider
from ..response import Response


class ServerErrorExceptionHook:
    def load(self, app):
        from config import application

        if application.DEBUG:
            return

        response = app.make(Response)

        response.status(500)
        if app.make("ViewClass").exists("errors/500"):
            rendered_view = app.make("View")("errors/500")
        else:
            rendered_view = app.make("View")(
                config(
                    "application.templates.statuscode", "/masonite/snippets/statuscode"
                ),
                {"code": "500 Internal Server Error"},
            )

        response.view(rendered_view)


class StatusCodeProvider(ServiceProvider):
    def register(self):
        self.app.bind("ServiceErrorExceptionHook", ServerErrorExceptionHook())

    def boot(self):
        request = self.app.make("Request")
        response = self.app.make(Response)
        if response.is_status(200):
            return

        if response.get_status() in (500, 405, 404):
            if "application/json" in request.header("Content-Type"):
                # Returns json response when we want the client to receive a json response
                body = json.loads(self.app.make("Response").decode("utf-8"))
                json_response = {
                    "error": {"status": response.get_status(), "body": body}
                }
                response.view(json_response, status=response.get_status())
            else:
                # Returns html response when json is not explicitly specified
                if self.app.make("ViewClass").exists(
                    "errors/{}".format(response.get_status())
                ):
                    rendered_view = self.app.make("View")(
                        "errors/{}".format(response.get_status())
                    )
                else:
                    rendered_view = self.app.make("View")(
                        config(
                            "application.templates.statuscode",
                            "/masonite/snippets/statuscode",
                        ),
                        {"code": response.get_status_code()},
                    )

                response.view(rendered_view, status=response.get_status())
