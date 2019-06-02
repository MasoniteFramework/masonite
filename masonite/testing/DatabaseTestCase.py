import subprocess
import unittest

from orator.orm import Factory
from masonite import env


class DatabaseTestCase(unittest.TestCase):

    sqlite = True
    refreshes_database = True
    has_setup_database = False

    def setUp(self):
        self.factory = Factory()

        if self.sqlite and env('DB_CONNECTION') != 'sqlite':
            raise Exception("Cannot run tests without using the 'sqlite' database.")

        if self.has_setup_database:
            self.setUpFactories()

            self.__class__.has_setup_database = False

        if self.refreshes_database:
            self.refreshDatabase()

    @classmethod
    def setUpClass(cls):
        cls.staticSetUpDatabase()
        if hasattr(cls, 'setUpFactories'):
            cls.has_setup_database = True

    @classmethod
    def tearDownClass(cls):
        cls.staticTearDownDatabase()

    def refreshDatabase(self):
        self.tearDownDatabase()
        self.setUpDatabase()

    def make(self, model, factory, amount=50):
        self.registerFactory(model, factory)
        self.makeFactory(model, amount)

    def makeFactory(self, model, amount):
        return self.factory(model, amount).create()

    def registerFactory(self, model, callable_factory):
        self.factory.register(model, callable_factory)

    def setUpDatabase(self):
        self.tearDownDatabase()
        subprocess.call(['craft', 'migrate'])
        self.setUpFactories()

    def tearDownDatabase(self):
        subprocess.call(['craft', 'migrate:reset'])

    @staticmethod
    def staticSetUpDatabase():
        subprocess.call(['craft', 'migrate'])

    @staticmethod
    def staticTearDownDatabase():
        subprocess.call(['craft', 'migrate:reset'])

    def tearDown(self):
        if self.refreshes_database:
            self.tearDownDatabase()
