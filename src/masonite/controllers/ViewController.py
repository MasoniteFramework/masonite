from ..facades import View


class ViewController:
    def __init__(self, template, data):
        self.template = template
        self.data = data

    def show(self):
        return View.render(self.template, self.data)
