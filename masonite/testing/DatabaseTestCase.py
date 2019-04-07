import subprocess
import unittest

from orator.orm import Factory


class DatabaseTestCase(unittest.TestCase):

    def setUp(self):
        self.factory = Factory()
        self.setUpDatabase()

    def make(self, model, factory, amount=50):
        self.registerFactory(model, factory)
        self.makeFactory(model, amount)

    def makeFactory(self, model, amount):
        return self.factory(model, amount).create()

    def registerFactory(self, model, callable_factory):
        self.factory.register(model, callable_factory)

    def setUpDatabase(self):
        subprocess.run(['craft', 'migrate'])

    def tearDownDatabase(self):
        subprocess.run(['craft', 'migrate:reset'])

    def tearDown(self):
        self.tearDownDatabase()
