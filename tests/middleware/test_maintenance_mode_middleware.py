""" Test Maintenance Mode Midddleware """
import os

from src.masonite.app import App
from src.masonite.request import Request
from src.masonite.middleware import MaintenanceModeMiddleware
from src.masonite.testing import generate_wsgi

from config import application
import unittest


class TestMaintenanceModeMiddleware(unittest.TestCase):

    def setUp(self):
        self.request = Request(generate_wsgi())
        self.middleware = MaintenanceModeMiddleware(self.request)
        down_path = os.path.join(application.BASE_DIRECTORY, 'bootstrap/down')
        down = os.path.exists(down_path)
        if down:
            os.remove(down_path)

    def test_maintenance_mode_middleware(self):
        app = App()
        app.bind('Request', self.request)
        app.bind('StatusCode', '200 OK')
        request = app.make('Request').load_app(app)
        down_path = os.path.join(application.BASE_DIRECTORY, 'bootstrap/down')
        down = open(down_path, 'w+')
        down.close()
        self.middleware.before()
        self.assertEqual(request.get_status_code(), '503 Service Unavailable')

    def test_maintenance_mode_middleware_is_not_down(self):
        app = App()
        app.bind('Request', self.request)
        app.bind('StatusCode', '200 OK')
        request = app.make('Request').load_app(app)
        self.middleware.before()
        self.assertEqual(request.get_status_code(), '200 OK')
