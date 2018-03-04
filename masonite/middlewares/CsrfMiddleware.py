from masonite.exceptions import InvalidCSRFToken


class CsrfMiddleware(object):
    """
    Verify csrf token middleware
    """

    exempt = []

    def __init__(self, Request, CSRF):
        self.request = Request
        self.csrf = CSRF

    def before(self):
        if self.request.is_post():
            token = self.request.input('csrf_token')
            if (not self.csrf.verify_csrf_token(token)
                    and not self.__in_except()):
                raise InvalidCSRFToken("Invalid CSRF token.")
        else:
            self.csrf.generate_token()

    def after(self):
        pass

    def __in_except(self):
        """
        Determine if the request has a URI that should pass
        through CSRF verification.
        """

        if self.request.path in self.exempt:
            return True
        else:
            return False
