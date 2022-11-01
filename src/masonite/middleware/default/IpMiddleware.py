import ipaddress
from .. import Middleware
from ...request import Request


class IpMiddleware(Middleware):

    # order of resolution of headers used to fetch request ip
    headers = [
        "HTTP_CLIENT_IP",
        "HTTP_X_FORWARDED_FOR",
        "HTTP_X_FORWARDED",
        "HTTP_X_CLUSTER_CLIENT_IP",
        "HTTP_FORWARDED_FOR",
        "HTTP_FORWARDED",
        "REMOTE_ADDR",
    ]

    def get_ip(self, request: Request):
        for header in self.headers:
            for raw_ip in request.environ.get(header, "").split(","):
                try:
                    ip = ipaddress.ip_address(raw_ip.strip())
                except ValueError:
                    continue
                if not ip.is_private and not ip.is_reserved:
                    return str(ip)
        return request.environ.get("REMOTE_ADDR")

    def before(self, request, response):
        request._ip = self.get_ip(request)
        return request

    def after(self, request, response):
        return request
