from masonite.provider import ServiceProvider
from masonite.app import App

def test_service_provider_loads_app():
    app = App()
    provider = ServiceProvider()
    provider.load_app(app).boot()

    assert provider.app == app

def test_service_provider_sets_on_app_object():
    app = App()
    provider = ServiceProvider()
    provider.load_app(app).register()

    assert 'Request' in app.providers 
    assert app.make('Request') == object
