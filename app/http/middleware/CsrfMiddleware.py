""" CSRF Middleware """
from masonite.middleware.CsrfMiddleware import CsrfMiddleware as Middleware


class CsrfMiddleware(Middleware):
    """ Verify CSRF Token Middleware """

    exempt = []
