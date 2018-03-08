from masonite.exceptions import InvalidCSRFToken


class CsrfMiddleware(object):
    """
    Verify csrf token middleware
    """

    exempt = []

    def __init__(self, Request, CSRF, ViewClass):
        self.request = Request
        self.csrf = CSRF
        self.view = ViewClass

    def before(self):
        # Verify token
        token = self.__verify_csrf_token()

        self.view.share({
            'csrf_field': "<input type='hidden' name='csrf_token' value='{0}' />".format(token)
        })

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

    def __verify_csrf_token(self):
        """
        Verify si csrf token in post is valid.
        """

        if self.request.is_post():
            token = self.request.input('csrf_token')
            if (not self.csrf.verify_csrf_token(token)
                    and not self.__in_except()):
                raise InvalidCSRFToken("Invalid CSRF token.")
        else:
            token = self.csrf.generate_csrf_token()

        return token
