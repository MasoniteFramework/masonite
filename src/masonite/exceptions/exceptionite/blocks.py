from exceptionite.tabs import Block

from ... import __version__
from ...helpers import optional


class AppBlock(Block):
    id = "application"
    name = "Application"
    icon = "DesktopComputerIcon"
    component = "KeyValBlockWithSections"

    def build(self):
        request = self.handler.app.make("request")
        route = request.get_route()

        data = {
            "Info": {
                "Masonite version": __version__,
                "Environment": self.handler.app.environment(),
                "Debug": self.handler.app.is_debug(),
            }
        }

        # add app route data
        if route:
            data.update(
                {
                    "Route": {
                        "controller": route.controller,
                        "route_name": route._name,
                        "route_middlewares": route.get_middlewares(),
                    }
                }
            )

        # add user route data
        user = request.user()
        if user:
            data.update(
                {
                    "User": {
                        "email": optional(user).email,
                        "ID": optional(user).id,
                    }
                }
            )

        return data


class RequestBlock(Block):
    id = "request"
    name = "Request"
    icon = "SwitchHorizontalIcon"
    component = "KeyValBlockWithSections"

    def build(self):
        request = self.handler.app.make("request")
        return {
            "Parameters": {
                "Path": request.get_path(),
                "Input": request.input_bag.all_as_values() or None,
                "Request Method": request.get_request_method(),
            },
            "Headers": request.header_bag.to_dict(),
        }
