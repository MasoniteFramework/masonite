from masonite.app import App
from middleware.CsrfMiddleware import CsrfMiddleware
from masonite.auth.Csrf import Csrf
from masonite.testsuite.TestSuite import TestSuite

container = TestSuite().create_container().container

container.bind('Csrf', Csrf(container.make('Request')))

csrf = container.make('Csrf')
request = container.make('Request')

middleware = container.resolve(CsrfMiddleware)

middleware.before()

def test_middleware_sets_csrf_cookie():
    assert request.get_cookie('csrf_token', decrypt=False)

def test_middleware_shares_view():
    assert 'csrf_field' in container.make('ViewClass').dictionary
    assert 'input' in container.make('ViewClass').dictionary['csrf_field']

def test_verify_token():
    token = request.get_cookie('csrf_token', decrypt=False)
    assert csrf.verify_csrf_token(token)
