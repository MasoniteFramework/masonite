from unittest import TestCase
from src.masonite.routes import Route, Router


class TestRoutes(TestCase):
    def setUp(self):
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

        route = router.find("/test/1", "post")
        self.assertIsNone(route)

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
