from masonite.request import Request
from masonite.view import View


class ControllerTest:

    def __init__(self, request: Request):
        self.request = request

    def show(self):
        return self.request

    def test(self):
        return 'test'

    def returns_a_view(self, view: View):
        return View('index')

    def returns_a_dict(self):
        return {'id': 1}

    def param(self):
        return self.request.param('id')
