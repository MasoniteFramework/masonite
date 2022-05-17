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

        # add headers to response if any
        if hasattr(exception, "get_headers"):
            headers = exception.get_headers()
            response.with_headers(headers)

        # if an exception handler is registered for this exception, use it instead
        # add headers to response if any
        if hasattr(exception, "get_headers"):
            headers = exception.get_headers()
            response.with_headers(headers)

        if self.application.has(f"{exception.__class__.__name__}Handler"):
            return self.application.make(
                f"{exception.__class__.__name__}Handler"
            ).handle(exception)

        # handle exception in production
        if not self.application.is_debug():
            # for HTTP error codes (500, 404, 403...) a specific page should be displayed
            # if a renderable exception is raised let it be displayed
            if hasattr(exception, "is_http_exception") or hasattr(
                exception, "get_response"
            ):
                return self.application.make("HttpExceptionHandler").handle(exception)

            # else fallback to an unknown exception that should be displayed as a 500 error
            exception.get_status = lambda: 500
            exception.get_response = lambda: str(exception) or "Unknown error"
            return self.application.make("HttpExceptionHandler").handle(exception)

        # handle exception in development mode with Exceptionite
        exceptionite = self.get_driver("exceptionite")
        exceptionite.start(exception)
        exceptionite.render("terminal")

        if request.accepts_json():
            return response.view(exceptionite.render("json"), status=500)
        else:
            return response.view(exceptionite.render("web"), status=500)
