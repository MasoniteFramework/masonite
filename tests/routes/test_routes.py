from src.masonite.utils.http import HTTP_STATUS_CODES
from tests import TestCase
from src.masonite.exceptions.exceptions import MethodNotAllowedException
from src.masonite.routes import Route, Router


class TestRoutes(TestCase):
    def setUp(self):
        super().setUp()
        Route.set_controller_locations("tests.integrations.controllers")
        pass

    def test_can_add_routes(self):
        routes = Route.group(
            [
                Route.get("/home", "WelcomeController"),
                Route.post("/login", "WelcomeController"),
            ]
        )

        self.assertEqual(len(routes), 2)

    def test_can_find_route(self):
        router = Router([Route.get("/home", "WelcomeController")])

        route = router.find("/home/", "GET")
        self.assertTrue(route)

    def test_can_add_routes_after(self):
        router = Router([Route.get("/home", "WelcomeController")])

        router.add(Route.get("/added", None))

        route = router.find("/added", "GET")
        self.assertTrue(route)

    def test_can_find_route_with_parameter(self):
        router = Router([Route.get("/home/@id", "WelcomeController")])

        route = router.find("/home/1", "GET")
        self.assertTrue(route)

    def test_can_compile_url_from_route_name(self):
        router = Router(
            Route.get("/home/@id", "WelcomeController").name("home"),
            Route.get("/dashboard/@id/@user", "WelcomeController").name("dashboard"),
        )

        url = router.route("home", {"id": 1})
        self.assertEqual(url, "/home/1")
        url = router.route("dashboard", {"user": 2, "id": 1})
        self.assertEqual(url, "/dashboard/1/2")
        url = router.route("dashboard", [2, 1])
        self.assertEqual(url, "/dashboard/2/1")

        # with query parameters
        url = router.route("home", {"id": 1}, query_params={"preview": "true"})
        self.assertEqual(url, "/home/1?preview=true")

    def test_can_find_route_optional_params(self):
        router = Router(Route.get("/home/?id", "WelcomeController"))

        route = router.find("/home/1", "GET")
        self.assertTrue(route)
        route = router.find("/home", "GET")
        self.assertTrue(route)

    def test_can_find_route_compiler(self):
        router = Router(Route.get("/route/@id:int", "WelcomeController"))

        route = router.find("/route/1", "GET")
        self.assertTrue(route)
        route = router.find("/route/string", "GET")
        self.assertFalse(route)

    def test_can_make_route_group(self):
        router = Router(
            Route.group(
                Route.get("/group", "WelcomeController@show"),
                Route.post("/login", "WelcomeController@show"),
                prefix="/testing",
            )
        )

        route = router.find("/testing/group", "GET")
        self.assertTrue(route)

    def test_can_make_base_route_group(self):
        router = Router(
            Route.group(
                [
                    Route.get("", "WelcomeController@show"),
                ],
                prefix="/testing",
            )
        )

        route = router.find("/testing", "GET")
        self.assertTrue(route)

    def test_can_make_route_group_nested(self):
        router = Router(
            Route.group(
                Route.get("/group", "WelcomeController@show"),
                Route.post("/login", "WelcomeController@show"),
                Route.group(
                    Route.get("/api/user", "WelcomeController@show"),
                    Route.group(Route.get("/api/test", None), prefix="/v1"),
                ),
                prefix="/testing",
            )
        )

        route = router.find("/testing/api/user", "GET")
        self.assertTrue(route)
        route = router.find("/testing/v1/api/test", "GET")
        self.assertTrue(route)

    def test_can_make_route_group_deep_module_nested(self):
        router = Router(
            Route.get(
                "/test/deep", "tests.integrations.controllers.api.TestController@show"
            )
        )

        route = router.find("/test/deep", "GET")
        self.assertTrue(route)

    def test_group_naming(self):
        router = Router(
            Route.group(
                Route.get("/group", "WelcomeController@show").name(".index"),
                Route.post("/login", "WelcomeController@show").name(".index"),
                prefix="/testing",
                name="dashboard",
            )
        )

        route = router.find_by_name("dashboard.index")
        self.assertTrue(route)

    def test_compile_year(self):
        Route.compile("year", r"[0-9]{4}")
        router = Router(Route.get("/year/@date:year", "WelcomeController@show"))

        route = router.find("/year/2005", "GET")
        self.assertTrue(route)

    def test_find_by_name(self):
        router = Router(
            Route.get("/getname", "WelcomeController@show").name("testname")
        )

        route = router.find_by_name("testname")
        self.assertTrue(route)

    def test_extract_parameters(self):
        router = Router(
            Route.get("/params/@id", "WelcomeController@show").name("testparam")
        )

        route = router.find_by_name("testparam")
        self.assertEqual(route.extract_parameters("/params/2")["id"], "2")

    def test_route_prefix(self):
        router = Router(
            Route.get("/params/route", "WelcomeController@show").name("testparam")
        )

        route = router.find("/params/route", "get")
        self.assertTrue(route)

        router = Router(
            Route.group([
                Route.get("/route", "WelcomeController@show").name("testparam")
            ], prefix="params")
            
        )

        route = router.find("/params/route", "get")

        self.assertTrue(route)

    def test_extract_parameters_ending_in_a_slash(self):
        router = Router(
            Route.get("/params/@id/", "WelcomeController@show").name("testparam")
        )

        route = router.find_by_name("testparam")
        self.assertEqual(route.extract_parameters("/params/2")["id"], "2")

    def test_casts_parameters_explicitly(self):
        route = Route.get("/params/@id", "WelcomeController@show").casts({"id": int})
        params = route.extract_parameters("/params/1")
        self.assertEqual(params, {"id": 1})

        # test that several params can be cast
        route = Route.get("/params/@id/@count", "WelcomeController@show").casts(
            {"id": int, "count": float}
        )
        params = route.extract_parameters("/params/1/2.3")
        self.assertEqual(params, {"id": 1, "count": 2.3})

        # test than callable can be used
        route = Route.get("/params/@id", "WelcomeController@show").casts(
            {"id": lambda value: value.upper()}
        )
        params = route.extract_parameters("/params/test")
        self.assertEqual(params, {"id": "TEST"})

    def test_casts_parameters_explicitly_based_on_route_compiler(self):
        route = Route.get("/params/@id", "WelcomeController@show").casts()
        params = route.extract_parameters("/params/1")
        self.assertEqual(params, {"id": "1"})

        route = Route.get("/params/@id:int", "WelcomeController@show").casts()
        params = route.extract_parameters("/params/1")
        self.assertEqual(params, {"id": 1})
        route = Route.get("/params/@id:integer", "WelcomeController@show").casts()
        params = route.extract_parameters("/params/1")
        self.assertEqual(params, {"id": 1})

        Route.compile("float", r"(\d+)")
        route = Route.get("/params/@id:float", "WelcomeController@show").casts()
        params = route.extract_parameters("/params/2")
        self.assertEqual(params, {"id": 2.0})

    def test_domain(self):
        router = Router(
            Route.get("/domain/@id", "WelcomeController@show").domain("sub")
        )

        route = router.find("/domain/2", "get")
        self.assertIsNone(route)

        route = router.find("/domain/2", "get", "sub")
        self.assertTrue(route)

    def test_finds_correct_methods(self):
        router = Router(Route.get("/test/1", "WelcomeController@show"))

        route = router.find("/test/1", "get")
        self.assertTrue(route)

        with self.assertRaises(MethodNotAllowedException) as e:
            route = router.find("/test/1", "post")

    def test_route_views(self):
        self.get("/test_view").assertContains("111")

    def test_can_exclude_middleware_from_route(self):
        router = Router(
            Route.group(
                Route.get("/group", "WelcomeController@show")
                .name("one")
                .middleware("web"),
                Route.post("/login", "WelcomeController@show")
                .name("two")
                .exclude_middleware("api"),
                Route.post("/", "WelcomeController@show")
                .name("three")
                .exclude_middleware("api", "test"),
                middleware=["api", "test"],
            )
        )

        self.assertEqual(len(router.find_by_name("one").get_middlewares()), 3)
        self.assertEqual(router.find_by_name("two").get_middlewares(), ["test"])
        self.assertEqual(router.find_by_name("three").get_middlewares(), [])

    def test_can_set_middleware_in_correct_order(self):
        router = Router(
            Route.group(
                Route.get("/group", "WelcomeController@show")
                .name("one")
                .middleware("web"),
                middleware=["api", "test"],
            )
        )

        self.assertEqual(len(router.find_by_name("one").get_middlewares()), 3)
        self.assertEqual(
            router.find_by_name("one").get_middlewares(), ["api", "test", "web"]
        )

    def test_can_set_multiple_middleware_in_correct_order(self):
        router = Router(
            Route.group(
                Route.get("/group", "WelcomeController@show")
                .name("one")
                .middleware("m3", "m4"),
                middleware=["m1", "m2"],
            )
        )

        self.assertEqual(len(router.find_by_name("one").get_middlewares()), 4)
        self.assertEqual(
            router.find_by_name("one").get_middlewares(), ["m1", "m2", "m3", "m4"]
        )

    def test_method_not_allowed_raised_if_wrong_method(self):
        router = Router(
            [
                Route.get("/home", "WelcomeController@show"),
                Route.put("/home", "WelcomeController@show"),
            ]
        )

        with self.assertRaises(MethodNotAllowedException) as context:
            router.find("/home", "POST")

        self.assertIn(
            "Supported methods are: GET, HEAD, PUT.", str(context.exception.message)
        )

    def test_options_method_returns_allowed_methods(self):

        router = Router(
            [
                Route.get("/home", "WelcomeController@show"),
                Route.put("/home", "WelcomeController@show"),
            ]
        )

        route = router.find("/home", "OPTIONS")
        self.assertEqual(route.request_method, ["options"])
        response = route.get_response(self.application)

        self.assertEqual(response.content, "")
        self.assertEqual(response._status, HTTP_STATUS_CODES[204])
        self.assertEqual(response.header("Allow"), "GET, HEAD, PUT")

    def test_head_method_is_registered_for_get_routes(self):
        router = Router(
            [
                Route.get("/home", "WelcomeController@show"),
            ]
        )
        route = router.find("/home", "HEAD")
        self.assertIsNotNone(route)
        self.assertEqual(route.request_method, ["get", "head"])
