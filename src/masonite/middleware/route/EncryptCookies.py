from ...exceptions import InvalidToken


class EncryptCookies:
    def before(self, request, response):
        for _, cookie in request.cookie_jar.all().items():
            try:
                cookie.value = request.app.make("sign").unsign(cookie.value)
            except InvalidToken:
                pass

        return request

    def after(self, request, response):
        for _, cookie in response.cookie_jar.all().items():
            try:
                cookie.value = request.app.make("sign").sign(cookie.value)
            except InvalidToken:
                pass

        return request
