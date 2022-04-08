from typing import TYPE_CHECKING

if TYPE_CHECKING:
    from ...request import Request
    from ...response import Response

from ...utils.str import match


class CorsMiddleware:
    def before(self, request: "Request", response: "Response"):
        cors = request.app.make("cors")

        if not self.match_paths(request, cors):
            return request

        if cors.is_preflight(request):
            response = cors.build_preflight_response(request, response)
            response = cors.update_vary_header(
                response, "Access-Control-Request-Method"
            )
            return response

        return request

    def after(self, request: "Request", response: "Response"):
        cors = request.app.make("cors")

        if request.get_request_method() == "OPTIONS":
            cors.update_vary_header(response, "Access-Control-Request-Method")

        response = cors.add_actual_request_headers(request, response)
        return response

    def match_paths(self, request: "Request", cors):
        host = request.get_host()
        request_path = request.get_path().strip("/")
        paths = cors.options.get("paths")

        for path in paths:
            if path != "/":
                path = path.strip("/")

            if path == host:
                return True
            elif match(request_path, path):
                return True

        return False
