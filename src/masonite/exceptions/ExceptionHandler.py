from exceptionite.errors import Handler, StackOverflowIntegration, SolutionsIntegration

from .JsonHandler import JsonHandler


class ExceptionHandler:
    def __init__(self, application, driver_config=None):
        self.application = application
        self.drivers = {}
        self.driver_config = driver_config or {}
        self.options = {}

    def set_options(self, options):
        self.options = options
        return self

    def add_driver(self, name, driver):
        self.drivers.update({name: driver})

    def set_configuration(self, config):
        self.driver_config = config
        return self

    def get_driver(self, name=None):
        if name is None:
            return self.drivers[self.driver_config.get("default")]
        return self.drivers[name]

    def get_config_options(self, driver=None):
        if driver is None:
            return self.driver_config[self.driver_config.get("default")]

        return self.driver_config.get(driver, {})

    def handle(self, exception):
        response = self.application.make("response")
        request = self.application.make("request")

        self.application.make("event").fire(
            f"masonite.exception.{exception.__class__.__name__}", exception
        )

        if self.application.has(f"{exception.__class__.__name__}Handler"):
            return self.application.make(
                f"{exception.__class__.__name__}Handler"
            ).handle(exception)

        if "application/json" in str(request.header("Accept")):
            return response.view(JsonHandler(exception).render(), status=500)

        if not self.application.is_debug():
            # for HTTP error codes (500, 404, 403...) a specific page should be displayed
            if hasattr(exception, "is_http_exception"):
                return self.application.make("HttpExceptionHandler").handle(exception)
            # if a renderable exception is raised let it be displayed
            if hasattr(exception, "get_response"):
                return response.view(exception.get_response(), exception.get_status())

            # else fallback to an unknown exception should be displayed as a 500 error
            exception.get_status = lambda: 500
            exception.get_response = lambda: str(exception) or "Unknown error"
            return self.application.make("HttpExceptionHandler").handle(exception)

        # else display exceptionite error page
        handler = Handler(exception)

        if self.options.get("handlers.stack_overflow"):
            handler.integrate(StackOverflowIntegration())
        if self.options.get("handlers.solutions"):
            handler.integrate(SolutionsIntegration())

        handler.context(
            {
                "WSGI": {
                    "Path": request.get_path(),
                    "Input": request.input_bag.all_as_values() or None,
                    # 'Parameters': request.url_params,
                    "Request Method": request.get_request_method(),
                },
                "Headers": request.header_bag.to_dict(),
            }
        )

        return response.view(handler.render(), status=500)
