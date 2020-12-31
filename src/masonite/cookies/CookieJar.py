from .Cookie import Cookie
from ..helpers import cookie_expire_time


class CookieJar:
    def __init__(self):
        self.cookies = {}
        self.loaded_cookies = {}
        self.deleted_cookies = {}

    def add(self, name, value, **options):
        self.cookies.update({name: Cookie(name, value, **options)})

    def all(self):
        return self.cookies

    def get(self, name):
        aggregate = self.loaded_cookies
        aggregate.update(self.cookies)
        return aggregate.get(name)

    def exists(self, name):
        return name in self.cookies or name in self.loaded_cookies

    def delete(self, name):
        self.deleted_cookies.update(
            {
                name: Cookie(
                    name, "", expires=cookie_expire_time("2 months"), timezone="GMT"
                )
            }
        )
        if name in self.cookies:
            return self.cookies.pop(name)

    def load_cookie(self, key, value):
        self.loaded_cookies.update({key: Cookie(key, value)})

    def to_dict(self):
        dic = {}
        aggregate = self.cookies
        aggregate.update(self.loaded_cookies)
        for name, cookie in aggregate.items():
            dic.update({name: cookie.value})

        return dic

    def load(self, cookie_string):
        for compound_value in cookie_string.split("; "):
            key, value = compound_value.split("=", 1)
            self.load_cookie(key, value)
        return self

    def render_response(self):
        cookies = []
        for name, cookie in self.all().items():
            cookies.append(("Set-Cookie", cookie.render()))

        return cookies
