from src.masonite.middleware.route.IpMiddleware import IpMiddleware
from tests import TestCase
from src.masonite.request import Request
from src.masonite.utils.http import generate_wsgi


class TestRequest(TestCase):
    def test_request_can_get_path(self):
        request = Request(generate_wsgi(path="/test"))
        self.assertEqual(request.get_path(), "/test")
        self.assertEqual(request.get_request_method(), "GET")

    def test_request_contains(self):
        request = Request(generate_wsgi(path="/test"))
        self.assertTrue(request.contains("/test"))

        request = Request(generate_wsgi(path="/test/user"))
        self.assertTrue(request.contains("/test/*"))

        request = Request(generate_wsgi(path="/test/admin/user"))
        self.assertTrue(request.contains("/test/*/user"))

        request = Request(generate_wsgi(path="/test/admin/user"))
        self.assertTrue(request.contains("*"))

    def test_request_ip(self):
        request = self.make_request(
            {
                # private or reserved
                "HTTP_CLIENT_IP": "172.16.0.2,255.255.255.255",
                # should be okay
                "HTTP_X_FORWARDED": "93.16.100.10",
                "REMOTE_ADDR": "192.167.2.1",
            }
        )
        response = self.make_response()
        request = IpMiddleware().before(request, response)
        self.assertEqual(request.ip(), "93.16.100.10")

        request = self.make_request(
            {
                "REMOTE_ADDR": "127.0.0.1",
            }
        )
        request = IpMiddleware().before(request, response)
        self.assertEqual(request.ip(), "127.0.0.1")
