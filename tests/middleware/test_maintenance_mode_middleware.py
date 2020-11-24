""" Test Maintenance Mode Midddleware """
import os

from src.masonite.app import App
from src.masonite.request import Request
from src.masonite.response import Response
from src.masonite.middleware import MaintenanceModeMiddleware
from src.masonite.testing import generate_wsgi

from config import application
import unittest
from src.masonite.testing import TestCase


class TestMaintenanceModeMiddleware(TestCase):

    def setUp(self):
        super().setUp()
        self.withHttpMiddleware([MaintenanceModeMiddleware])
        self.down_path = os.path.join(application.BASE_DIRECTORY, 'bootstrap/down')

    def test_maintenance_mode_middleware(self):
        down = open(self.down_path, 'w+')
        down.close()
        self.get('/')
        request = self.container.make('Request')
        response = self.container.make(Response)
        self.assertEqual(response.get_status_code(), '503 Service Unavailable')

    def test_maintenance_mode_middleware_is_not_down(self):
        os.remove(self.down_path)
        self.get('/')
        request = self.container.make('Request')
        response = self.container.make(Response)
        self.assertEqual(response.get_status_code(), '200 OK')
