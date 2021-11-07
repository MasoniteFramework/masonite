from src.masonite.controllers import Controller
from src.masonite.views import View


class HelloController(Controller):
    def show(self, view: View):
        return view.render("")
