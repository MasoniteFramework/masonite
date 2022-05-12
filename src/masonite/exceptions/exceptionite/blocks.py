from exceptionite import Block

from ... import __version__
from ...helpers import optional
from ...utils.str import get_controller_name


def recursive_serializer(data):
    if isinstance(data, (int, bool, str, bytes)):
        return data
    elif isinstance(data, (list, tuple)):
        return [recursive_serializer(item) for item in data]
    elif isinstance(data, dict):
        return {key: recursive_serializer(val) for key, val in data.items()}
    elif callable(data):
        return str(data)
    elif hasattr(data, "serialize"):
        return data.serialize()
    else:
        return str(data)


class AppBlock(Block):
    id = "application"
    name = "Application"
    icon = "DesktopComputerIcon"
    has_sections = True

    def build(self):
        request = self.handler.app.make("request")
        route = request.get_route()

        data = {
            "Info": {
                "Masonite Version": __version__,
                "Environment": self.handler.app.environment(),
                "Debug": self.handler.app.is_debug(),
            }
        }

        # add app route data
        if route:
            data.update(
                {
                    "Route": {
                        "Controller": get_controller_name(route.controller),
                        "Name": route.get_name(),
                        "Middlewares": route.get_middlewares(),
                    }
                }
            )

        # add user route data
        user = request.user()
        if user:
            data.update(
                {
                    "User": {
                        "E-mail": optional(user).email,
                        "ID": optional(user).id,
                    }
                }
            )

        return data


class RequestBlock(Block):
    id = "request"
    name = "Request"
    icon = "SwitchHorizontalIcon"
    has_sections = True

    def build(self):
        request = self.handler.app.make("request")
        # serialize inputs (e.g. in case of file)
        inputs = {}
        for name, value in request.all().items():
            inputs[name] = recursive_serializer(value)
        return {
            "Parameters": {
                "Path": request.get_path(),
                "Input": inputs or None,
                "Request Method": request.get_request_method(),
            },
            "Headers": request.header_bag.to_dict(),
        }


class ConfigBlock(Block):
    id = "config"
    name = "Configuration"
    icon = "CogIcon"
    has_sections = True

    def build(self):
        data = {}
        for section, config_data in self.handler.app.make("config").all().items():
            section_name = section.title()
            data[section_name] = recursive_serializer(config_data)
        return data
