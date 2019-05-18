import subprocess
import unittest

from orator.orm import Factory
from masonite import env


class DatabaseTestCase(unittest.TestCase):

    sqlite = True

    def setUp(self):
        self.factory = Factory()

        if self.sqlite and env('DB_CONNECTION') != 'sqlite':
            raise Exception("Cannot run tests without using the 'sqlite' database.")

        self.setUpDatabase()

    def make(self, model, factory, amount=50):
        self.registerFactory(model, factory)
        self.makeFactory(model, amount)

    def makeFactory(self, model, amount):
        return self.factory(model, amount).create()

    def registerFactory(self, model, callable_factory):
        self.factory.register(model, callable_factory)

    def setUpDatabase(self):
        subprocess.call(['craft', 'migrate'])

    def tearDownDatabase(self):
        subprocess.call(['craft', 'migrate:reset'])

    def tearDown(self):
        self.tearDownDatabase()
