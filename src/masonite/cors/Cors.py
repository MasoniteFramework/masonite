from typing import TYPE_CHECKING

if TYPE_CHECKING:
    from ..foundation import Application
    from ..request import Request
    from ..response import Response


class Cors:
    """Service to handle Cross-Origin Resource Sharing operations."""

    def __init__(self, application: "Application", options: dict = {}):
        self.application = application
        self.options = {}
        self.allow_all_headers = False
        self.allow_all_methods = False
        self.allow_all_origins = False

        self.set_options(options)

    def set_options(self, options: dict) -> "Cors":

        # normalize options
        allowed_headers = list(
            map(lambda h: h.lower(), options.get("allowed_headers", []))
        )
        allowed_methods = list(
            map(lambda h: h.upper(), options.get("allowed_methods", []))
        )
        self.allow_all_headers = "*" in allowed_headers
        self.allow_all_methods = "*" in allowed_methods
        self.allow_all_origins = "*" in options.get("allowed_origins", [])

        self.options = {
            **options,
            "allowed_headers": allowed_headers,
            "allowed_methods": allowed_methods,
        }
        return self

    def is_single_origin_allowed(self) -> bool:
        if self.allow_all_origins:
            return False
        return len(self.options.get("allowed_origins", [])) == 1

    def is_preflight(self, request: "Request") -> bool:
        """Check if given request is a preflight request."""
        return request.get_request_method() == "OPTIONS" and request.header(
            "Access-Control-Request-Method"
        )

    def is_cors(self, request: "Request") -> bool:
        """Check if given request is CORS request by inspecting 'Origin' header."""
        return request.header("Origin")

    def is_allowed(self, request: "Request") -> bool:
        """Check if request 'Origin' is allowed regarding CORS config."""
        if self.allow_all_origins:
            return True

        origin = request.header("Origin")

        if origin in self.options.get("allowed_origins", []):
            return True

        return False

    def matches(self, request: "Request") -> bool:
        """Check if given request matches paths defined in CORS options."""
        pass

    def build_preflight_response(
        self, request: "Request", response: "Response"
    ) -> "Response":
        """Build a preflight response for the given request."""
        response.status(204)

        response = self.set_allowed_origin(request, response)

        if response.header("Access-Control-Allow-Origin"):
            response = self.set_allowed_credentials(response)
            response = self.set_allowed_methods(request, response)
            response = self.set_allowed_headers(request, response)
            response = self.set_max_age(response)

        return response

    def set_allowed_origin(
        self, request: "Request", response: "Response"
    ) -> "Response":
        if self.allow_all_origins and not self.options.get("supports_credentials"):
            response.header("Access-Control-Allow-Origin", "*")
        elif self.is_single_origin_allowed():
            response.header(
                "Access-Control-Allow-Origin", self.options.get("allowed_origins")[0]
            )
        else:
            if self.is_cors(request) and self.is_allowed(request):
                response.header("Access-Control-Allow-Origin", request.header("Origin"))

            self.update_vary_header(response, "Origin")
        return response

    def update_vary_header(self, response: "Response", value: str) -> "Response":
        if not response.header("Vary"):
            response.header("Vary", value)
        else:
            vary_header = response.header("Vary").split(", ")
            if value not in vary_header:
                vary_header.append(value)
                response.header("Vary", ", ".join(vary_header))
        return response

    def set_allowed_headers(
        self, request: "Request", response: "Response"
    ) -> "Response":
        if self.allow_all_headers:
            allowed_headers = request.header("Access-Control-Request-Headers")
            response = self.update_vary_header(
                response, "Access-Control-Request-Headers"
            )
        else:
            allowed_headers = ", ".join(self.options.get("allowed_headers", []))
        response.header("Access-Control-Allow-Headers", allowed_headers)
        return response

    def set_allowed_methods(
        self, request: "Request", response: "Response"
    ) -> "Response":
        if self.allow_all_methods:
            allowed_methods = request.header("Access-Control-Request-Method").upper()
            response = self.update_vary_header(
                response, "Access-Control-Request-Method"
            )
        else:
            allowed_methods = ", ".join(self.options.get("allowed_methods", []))
        response.header("Access-Control-Allow-Methods", allowed_methods)
        return response

    def set_max_age(self, response: "Response") -> "Response":
        max_age = self.options.get("max_age", None)
        # Here max_age could be set to 0s, different from None
        if max_age is not None:
            response.header("Access-Control-Max-Age", str(max_age))
        return response

    def set_exposed_headers(self, response: "Response") -> "Response":
        exposed_headers = self.options.get("exposed_headers", [])
        if exposed_headers:
            response.header("Access-Control-Expose-Headers", ", ".join(exposed_headers))
        return response

    def set_allowed_credentials(self, response: "Response") -> "Response":
        if self.options.get("supports_credentials", False):
            response.header("Access-Control-Allow-Credentials", "true")
        return response

    def add_actual_request_headers(
        self, request: "Request", response: "Response"
    ) -> "Response":
        """Add request headers to response."""
        response = self.set_allowed_origin(request, response)
        if response.header("Access-Control-Allow-Origin"):
            response = self.set_allowed_credentials(response)
            response = self.set_exposed_headers(response)
        return response
