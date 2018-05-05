class ControllerTest:

    def __init__(self, Request):
        self.request = Request

    def show(self):
        return self.request
