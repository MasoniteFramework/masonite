from tests import TestCase

from src.masonite.helpers import url


class TestUrlsHelper(TestCase):
    def test_url(self):
        self.assertEqual(url.url("about/us"), "http://localhost:8000/about/us")
        self.assertEqual(url.url("/about/us"), "http://localhost:8000/about/us")
        self.assertEqual(url.url(), "http://localhost:8000/")

        # with query parameters
        self.assertEqual(
            url.url("search", {"q": "joe", "order": "asc"}),
            "http://localhost:8000/search?q=joe&order=asc",
        )
        self.assertEqual(
            url.url("search", {"q": "El Niño", "order": "asc"}),
            "http://localhost:8000/search?q=El+Ni%C3%B1o&order=asc",
        )

        self.assertEqual(
            url.url("search?q=joe", {"order": "asc"}),
            "http://localhost:8000/search?q=joe&order=asc",
        )

        self.assertEqual(
            url.url("/users/search?q=joe", {"q": "john doe", "debug": 1}),
            "http://localhost:8000/users/search?q=john+doe&debug=1",
        )

    def test_route(self):
        self.assertEqual(url.route("welcome"), "http://localhost:8000/")
        self.assertEqual(
            url.route("users.profile", {"id": 1}), "http://localhost:8000/users/1"
        )
        self.assertEqual(url.route("upload"), "http://localhost:8000/upload")
        self.assertEqual(url.route("upload", absolute=False), "/upload")
        # with query parameters
        self.assertEqual(
            url.route("upload", query_params={"force": 1}),
            "http://localhost:8000/upload?force=1",
        )

    def test_asset(self):
        self.assertTrue(
            url.asset("local", "test.jpg").endswith(
                "storage/framework/filesystem/test.jpg"
            )
        )
