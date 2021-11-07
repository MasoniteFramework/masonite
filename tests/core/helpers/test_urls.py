from tests import TestCase

from src.masonite.helpers import url


class TestUrlsHelper(TestCase):
    def test_url(self):
        self.assertEqual(url.url("about/us"), "http://localhost:8000/about/us")
        self.assertEqual(url.url("/about/us"), "http://localhost:8000/about/us")
        self.assertEqual(url.url(), "http://localhost:8000/")

    def test_route(self):
        self.assertEqual(url.route("welcome"), "http://localhost:8000/")
        self.assertEqual(
            url.route("users.profile", {"id": 1}), "http://localhost:8000/users/1"
        )
        self.assertEqual(url.route("upload"), "http://localhost:8000/upload")
        self.assertEqual(url.route("upload", absolute=False), "/upload")

    def test_asset(self):
        self.assertTrue(
            url.asset("local", "test.jpg").endswith(
                "storage/framework/filesystem/test.jpg"
            )
        )
