from masonite.controllers import Controller
from masonite.views import View


class HomeController(Controller):
    def show(self, view: View):
        return view.render("auth.home")
