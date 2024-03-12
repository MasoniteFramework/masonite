from ..controllers.ViewController import ViewController
from .HTTPRoute import HTTPRoute
from ..utils.collections import flatten
from ..utils.str import modularize
from ..controllers import RedirectController


class Route:
    routes = []
    compilers = {
        "int": r"(\d+)",
        "integer": r"(\d+)",
        "string": r"([a-zA-Z]+)",
        "default": r"([\w.-]+)",
        "signed": r"([\w\-=]+)",
        "any": r"(.*)",
        "uuid": r"([0-9a-fA-F]{8}\b-[0-9a-fA-F]{4}\b-[0-9a-fA-F]{4}\b-[0-9a-fA-F]{4}\b-[0-9a-fA-F]{12})",
    }
    controllers_locations = []

    def __init__(self):
        pass

    @classmethod
    def get(self, url, controller, module_location=None, **options):
        return HTTPRoute(
            url,
            controller,
            request_method=["get", "head"],
            compilers=self.compilers,
            controllers_locations=module_location or self.controllers_locations,
            **options,
        )

    @classmethod
    def post(self, url, controller, **options):
        return HTTPRoute(
            url,
            controller,
            request_method=["post"],
            compilers=self.compilers,
            controllers_locations=self.controllers_locations,
            **options,
        )

    @classmethod
    def put(self, url, controller, **options):
        return HTTPRoute(
            url,
            controller,
            request_method=["put"],
            compilers=self.compilers,
            controllers_locations=self.controllers_locations,
            **options,
        )

    @classmethod
    def patch(self, url, controller, **options):
        return HTTPRoute(
            url,
            controller,
            request_method=["patch"],
            compilers=self.compilers,
            controllers_locations=self.controllers_locations,
            **options,
        )

    @classmethod
    def delete(self, url, controller, **options):
        return HTTPRoute(
            url,
            controller,
            request_method=["delete"],
            compilers=self.compilers,
            controllers_locations=self.controllers_locations,
            **options,
        )

    @classmethod
    def options(self, url, controller, **options):
        return HTTPRoute(
            url,
            controller,
            request_method=["options"],
            compilers=self.compilers,
            controllers_locations=self.controllers_locations,
            **options,
        )

    @classmethod
    def default(self, url, controller, **options):
        return self

    @classmethod
    def redirect(self, url, new_url, **options):
        return HTTPRoute(
            url,
            RedirectController.redirect,
            request_method=["get"],
            compilers=self.compilers,
            controllers_locations=self.controllers_locations,
            controller_bindings=[new_url, options.get("status", 302)],
            **options,
        )

    @classmethod
    def view(self, url, template, data=None, **options):
        if not data:
            data = {}

        return HTTPRoute(
            url,
            ViewController.show,
            request_method=options.get("method", ["get"]),
            compilers=self.compilers,
            controllers_locations=self.controllers_locations,
            controller_bindings=[template, data],
            **options,
        )

    @classmethod
    def permanent_redirect(self, url, new_url, **options):
        return HTTPRoute(
            url,
            RedirectController.redirect,
            request_method=["get"],
            compilers=self.compilers,
            controllers_locations=self.controllers_locations,
            controller_bindings=[new_url, 301],
            **options,
        )

    @classmethod
    def match(self, request_methods, url, controller, **options):
        return HTTPRoute(
            url,
            controller,
            request_method=request_methods,
            compilers=self.compilers,
            controllers_locations=self.controllers_locations,
            **options,
        )

    @classmethod
    def group(self, *routes, **options):
        inner = []
        for route in flatten(routes):
            prefix = options.get("prefix")
            if prefix:
                if not prefix.startswith("/"):
                    prefix = "/" + prefix
                if route.url == "" or route.url == "/":
                    route.url = prefix
                else:
                    route.url = prefix + route.url

                route.compile_route_to_regex()

            if options.get("name"):
                route._name = options.get("name") + route._name

            if options.get("domain"):
                route.domain(options.get("domain"))

            if options.get("middleware"):
                middleware = route.list_middleware
                middleware = options.get("middleware", []) + middleware

                route.set_middleware(middleware)

            inner.append(route)
        self.routes = inner
        return inner

    @classmethod
    def resource(self, base_url, controller):
        return [
            self.get(f"/{base_url}", f"{controller}@index").name(f"{base_url}.index"),
            self.get(f"/{base_url}/create", f"{controller}@create").name(
                f"{base_url}.create"
            ),
            self.post(f"/{base_url}", f"{controller}@store").name(f"{base_url}.store"),
            self.get(f"/{base_url}/@id", f"{controller}@show").name(f"{base_url}.show"),
            self.get(f"/{base_url}/@id/edit", f"{controller}@edit").name(
                f"{base_url}.edit"
            ),
            self.match(
                ["put", "patch"], f"/{base_url}/@id", f"{controller}@update"
            ).name(f"{base_url}.update"),
            self.delete(f"/{base_url}/@id", f"{controller}@destroy").name(
                f"{base_url}.destroy"
            ),
        ]

    @classmethod
    def api(self, base_url, controller):
        return [
            self.get(f"/{base_url}", f"{controller}@index").name(f"{base_url}.index"),
            self.post(f"/{base_url}", f"{controller}@store").name(f"{base_url}.store"),
            self.get(f"/{base_url}/@id", f"{controller}@show").name(f"{base_url}.show"),
            self.match(
                ["put", "patch"], f"/{base_url}/@id", f"{controller}@update"
            ).name(f"{base_url}.update"),
            self.delete(f"/{base_url}/@id", f"{controller}@destroy").name(
                f"{base_url}.destroy"
            ),
        ]

    @classmethod
    def any(self, url, controller, module_location=None, **options):
        return self.match(
            ("GET", "POST", "PUT", "PATCH", "DELETE", "OPTIONS"),
            url,
            controller,
            module_location=module_location,
        )

    @classmethod
    def fallback(self, controller, module_location=None, **options):
        return HTTPRoute(
            url="@route:any",
            controller=controller,
            request_method=["get", "head"],
            compilers=self.compilers,
            controllers_locations=module_location or self.controllers_locations,
            **options,
        )

    @classmethod
    def compile(self, key, to=""):
        self.compilers.update({key: to})
        return self

    @classmethod
    def set_controller_locations(self, *controllers_locations):
        self.controllers_locations = list(map(modularize, controllers_locations))
        return self

    @classmethod
    def add_controller_locations(self, *controllers_locations):
        self.controllers_locations.extend(list(map(modularize, controllers_locations)))
        return self
