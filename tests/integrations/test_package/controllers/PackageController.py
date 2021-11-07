from src.masonite.controllers import Controller


class PackageController(Controller):
    def api(self):
        return {"data": "ok"}, 201

    def index(self):
        return "index"
