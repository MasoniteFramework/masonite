from src.masonite.request import Request
from src.masonite.view import View


class ControllerTest:

    def __init__(self, request: Request):
        self.request = request

    def show(self):
        return self.request

    def test(self):
        return 'test'

    def returns_a_view(self, view: View):
        return view.render('index')

    def returns_a_dict(self):
        return {'id': 1}

    def param(self):
        return self.request.param('id')

    def get_param(self, first):
        self.request.first = first
        return self.request

    def get_param_and_object(self, first, view: View):
        self.request.first = first
        self.request.view = view
        return self.request
