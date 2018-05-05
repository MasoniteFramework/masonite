class ControllerTest:

    def __init__(self, Request):
        self.request = Request

    def show(self):
        return self.request
    
    def test(self):
        return 'test'

    def returns_a_view(self, View):
        return View('index')

    def returns_a_dict(self):
        return {'id': 1}
