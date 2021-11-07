from src.masonite.controllers import Controller


class TestController(Controller):
    def show(self):
        return "welcome"
