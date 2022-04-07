from typing import TYPE_CHECKING

if TYPE_CHECKING:
    from ...request import Request
    from ...response import Response

from ...cors import Cors


class CorsMiddleware:
    def before(self, request: "Request", response: "Response", cors: Cors):

        if not self.match_paths(request):
            return request

        if cors.is_preflight(request):
            response = cors.build_preflight_response(request, response)
            response = cors.update_vary_header(
                response, "Access-Control-Request-Method"
            )
            return response

        return request

    def after(self, request: "Request", response: "Response", cors: Cors):
        if request.get_request_method() == "OPTIONS":
            cors.update_vary_header(response, "Access-Control-Request-Method")

        response = cors.add_actual_request_headers(request)
        return response

    def match_paths(self, request: "Request", cors):
        host = request.get_host()
        request_path = request.get_path()
        paths = cors.options.get("paths")

        for path in paths:
            if path != "/":
                path = path.strip("/")
            if path == host:
                return True
            elif request_path == path:
                return True

        return False
