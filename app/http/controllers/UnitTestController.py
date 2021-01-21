"""A UnitTestController Module."""

from src.masonite.request import Request
from src.masonite.controllers import Controller
from src.masonite.view import View


class UnitTestController(Controller):
    """UnitTestController Controller Class."""

    def __init__(self, request: Request):
        """UnitTestController Initializer

        Arguments:
            request {masonite.request.Request} -- The Masonite Request class.
        """
        self.request = request

    def show(self):
        return 'got'

    def store(self):
        return 'posted'

    def params(self):
        return self.request.input('test')

    def get_params(self):
        return self.request.input('test')

    def user(self):
        return self.request.user().name

    def json(self):
        return self.request.input('test')

    def response(self):
        return {
            'count': 5,
            'iterable': [1, 2, 3]
        }

    def multi(self):
        return {
            'author': {
                'name': 'Joe'
            }
        }

    def multi_count(self):
        return {"count": 5, "iterable": [1, 2, 3]}

    def patch(self):
        return self.request.input('test')

    def param(self):
        return self.request.param('post_id')

    def view(self, view: View):
        return view.render("test", {"count": 1, "users": ["John", "Joe"]})
