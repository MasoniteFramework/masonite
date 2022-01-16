import unittest

from src.masonite.cookies import CookieJar
from src.masonite.utils.time import cookie_expire_time


class TestCookies(unittest.TestCase):
    def test_cookies_can_get_set(self):
        cookiejar = CookieJar()
        cookiejar.add("cookie", "name")
        self.assertEqual(cookiejar.get("cookie").value, "name")
        self.assertEqual(cookiejar.get("cookie").name, "cookie")

    def test_cookies_can_put_to_dict(self):
        cookiejar = CookieJar()
        cookiejar.add("cookie", "name")
        self.assertEqual(cookiejar.to_dict(), {"cookie": "name"})

    def test_cookie_jar_can_render_cookie_string(self):
        cookiejar = CookieJar()
        cookiejar.add("cookie", "name", http_only=False)
        self.assertEqual(
            cookiejar.render_response(),
            [("Set-Cookie", "cookie=name;Path=/;SameSite=Strict;")],
        )

    def test_cookie_jar_can_render_multiple_cookies(self):
        cookiejar = CookieJar()
        cookiejar.add("cookie1", "name", http_only=False)
        cookiejar.add("cookie2", "name", http_only=False)
        self.assertEqual(
            cookiejar.render_response(),
            [
                ("Set-Cookie", "cookie1=name;Path=/;SameSite=Strict;"),
                ("Set-Cookie", "cookie2=name;Path=/;SameSite=Strict;"),
            ],
        )

    def test_cookie_jar_can_render_multiple_cookies_with_different_options(self):
        cookiejar = CookieJar()
        cookiejar.add("cookie1", "name", path="/")
        self.assertEqual(
            cookiejar.render_response(),
            [("Set-Cookie", "cookie1=name;HttpOnly;Path=/;SameSite=Strict;")],
        )

    def test_cookie_with_expires(self):
        cookiejar = CookieJar()
        time = cookie_expire_time("2 months")
        cookiejar.add("cookie1", "name", path="/", expires=time, timezone="GMT")
        self.assertEqual(
            cookiejar.render_response(),
            [
                (
                    "Set-Cookie",
                    f"cookie1=name;HttpOnly;Expires={time} GMT;Path=/;SameSite=Strict;",
                )
            ],
        )

    def test_cookie_with_expired_already(self):
        cookiejar = CookieJar()
        time = cookie_expire_time("expired")
        cookiejar.add("cookie1", "name", path="/", expires=time, timezone="GMT")
        self.assertEqual(
            cookiejar.render_response(),
            [
                (
                    "Set-Cookie",
                    f"cookie1=name;HttpOnly;Expires={time} GMT;Path=/;SameSite=Strict;",
                )
            ],
        )

    def test_cookie_can_load(self):
        cookiejar = CookieJar()
        cookiejar.add("cookie1", "name", http_only=False)
        cookiejar.load("csrf_token=tok")
        self.assertEqual(
            cookiejar.render_response(),
            [("Set-Cookie", "cookie1=name;Path=/;SameSite=Strict;")],
        )
        self.assertEqual(cookiejar.get("csrf_token").value, "tok")

    def test_cookie_can_make_secure_cookies(self):
        cookiejar = CookieJar()
        cookiejar.add("cookie1", "name", http_only=False, secure=True)
        self.assertEqual(
            cookiejar.render_response(),
            [("Set-Cookie", "cookie1=name;Secure;Path=/;SameSite=Strict;")],
        )
