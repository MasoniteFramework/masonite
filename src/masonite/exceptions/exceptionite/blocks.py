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
                        "Controller": route.controller,
                        "Name": route._name,
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


def recursive_serializer(data):
    # TODO: add get_serialize/serialize
    if isinstance(data, (int, bool, str, bytes)):
        return data
    elif isinstance(data, (list, tuple)):
        return [recursive_serializer(item) for item in data]
    elif isinstance(data, dict):
        return {key: recursive_serializer(val) for key, val in data.items()}
    elif callable(data):
        return str(data)
    else:
        return str(data)


class ConfigBlock(Block):
    id = "config"
    name = "Configuration"
    icon = "CogIcon"
    component = "KeyValBlockWithSections"

    def build(self):
        data = {}
        for section, config_data in self.handler.app.make("config").all().items():
            section_name = section.title()
            data[section_name] = recursive_serializer(config_data)
        return data
