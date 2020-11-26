import unittest

from src.masonite.cookies import CookieJar
from src.masonite.helpers import cookie_expire_time

class TestCookies(unittest.TestCase):

    def test_cookies_can_get_set(self):
        cookiejar = CookieJar()
        cookiejar.add("cookie", "name")
        self.assertEqual(cookiejar.get('cookie').value, "name")
        self.assertEqual(cookiejar.get('cookie').name, "cookie")

    def test_cookies_can_put_to_dict(self):
        cookiejar = CookieJar()
        cookiejar.add("cookie", "name")
        self.assertEqual(cookiejar.to_dict(), {"cookie": "name"})

    def test_cookie_jar_can_render_cookie_string(self):
        cookiejar = CookieJar()
        cookiejar.add("cookie", "name", http_only=False)
        self.assertEqual(cookiejar.render_response(), [('Set-Cookie', "cookie=name;")])

    def test_cookie_jar_can_render_multiple_cookies(self):
        cookiejar = CookieJar()
        cookiejar.add("cookie1", "name", http_only=False)
        cookiejar.add("cookie2", "name", http_only=False)
        self.assertEqual(cookiejar.render_response(), [('Set-Cookie', "cookie1=name;"), ('Set-Cookie', "cookie2=name;")])

    def test_cookie_jar_can_render_multiple_cookies_with_different_options(self):
        cookiejar = CookieJar()
        cookiejar.add("cookie1", "name", path='/')
        self.assertEqual(cookiejar.render_response(), [('Set-Cookie', "cookie1=name;HttpOnly;Path=/;")])

    def test_cookie_with_timezone(self):
        cookiejar = CookieJar()
        cookiejar.add("cookie1", "name", path='/', expires=cookie_expire_time("2 months"), timezone="GMT")
        # self.assertEqual(cookiejar.render_response(), [('Set-Cookie', "cookie1=name;HttpOnly;Path=/;")])

    def test_cookie_can_load(self):
        cookiejar = CookieJar()
        cookiejar.add("cookie1", "name", http_only=False)
        cookiejar.load("csrf_token=tok")
        self.assertEqual(cookiejar.render_response(), [('Set-Cookie', "cookie1=name;")])
        self.assertEqual(cookiejar.get('csrf_token').value, 'tok')
