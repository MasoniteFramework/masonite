from masonite.routes import Api

API = Api()

def test_api_is_callable():
    if callable(API):
        assert True

def test_api_route_returns_self():
    assert API.route('url') == API

def test_api_route_set_url():
    assert API.url == 'url'

def test_api_exclude_list():
    assert API.exclude(['password', 'token']) == API
    assert API.exclude_list == ['password', 'token']