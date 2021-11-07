from unittest.mock import MagicMock

from src.masonite.middleware import MiddlewareCapsule
from tests import TestCase


class MockMiddleware:
    def before(self, request, response, arg1):
        return request

    def after(self, request, response):

        return request


class TestMiddleware(TestCase):
    def test_can_create_capsule(self):
        capsule = MiddlewareCapsule()
        self.assertTrue(capsule)

    def test_can_add_middleware(self):
        capsule = MiddlewareCapsule()
        capsule.add({"mock": MockMiddleware})
        capsule.add([MockMiddleware])

        self.assertTrue(len(capsule.route_middleware) == 1)
        self.assertTrue(len(capsule.http_middleware) == 1)

    def test_can_add_and_remove_middleware(self):
        capsule = MiddlewareCapsule()
        capsule.add({"mock": MockMiddleware})
        capsule.add([MockMiddleware])
        capsule.remove(MockMiddleware)

        self.assertTrue(len(capsule.route_middleware) == 1)
        self.assertTrue(len(capsule.http_middleware) == 0)

    def test_can_get_multiple_middleware(self):
        capsule = MiddlewareCapsule()
        capsule.add(
            {
                "mock": MockMiddleware,
                "mock1": MockMiddleware,
                "mock2": MockMiddleware,
                "mock3": [MockMiddleware, MockMiddleware],
            }
        )
        capsule.add([MockMiddleware])
        capsule.remove(MockMiddleware)

        self.assertTrue(
            len(capsule.get_route_middleware(["mock", "mock1", "mock2"])) == 3
        )
        self.assertTrue(
            len(capsule.get_route_middleware(["mock", "mock1", "mock2", "mock3"])) == 5
        )

    def test_can_run_middleware_with_args(self):
        request = self.make_request()
        response = self.make_response()
        capsule = MiddlewareCapsule()
        MockMiddleware.before = MagicMock(return_value=request)
        capsule.add(
            {
                "mock": MockMiddleware,
            }
        )

        capsule.run_route_middleware(["mock:arg1,arg2"], request, response)
        MockMiddleware.before.assert_called_with(request, response, "arg1", "arg2")

    def test_can_use_request_inputs_as_args(self):
        # this create a request with @user_id and @id as in input
        request = self.make_request(query_string="user_id=3&id=1")
        response = self.make_response()
        capsule = MiddlewareCapsule()
        MockMiddleware.before = MagicMock(return_value=request)
        capsule.add(
            {
                "mock": MockMiddleware,
            }
        )

        capsule.run_route_middleware(["mock:@user_id,@id"], request, response)
        MockMiddleware.before.assert_called_with(request, response, "3", "1")

    def test_can_mix_args_and_request_inputs(self):
        # this create a request with @user_id as in input
        request = self.make_request(query_string="user_id=3")
        response = self.make_response()
        capsule = MiddlewareCapsule()
        MockMiddleware.before = MagicMock(return_value=request)
        capsule.add(
            {
                "mock": MockMiddleware,
            }
        )

        capsule.run_route_middleware(["mock:@user_id,value"], request, response)
        MockMiddleware.before.assert_called_with(request, response, "3", "value")
