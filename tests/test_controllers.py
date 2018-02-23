from masonite.app import App
from masonite.controllers import Controller


def test_controller_loads_app():
    app = App()
    app.bind('object', object)

    controller = Controller().load_app(app)
    assert controller.app.providers == {'object': object}
