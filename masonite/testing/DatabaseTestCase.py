import subprocess
import unittest

from orator.orm import Factory
from masonite import env


class DatabaseTestCase(unittest.TestCase):

    sqlite = True
    transactions = True
    refreshes_database = False
    _has_setup_database = False

    def setUp(self):
        self.factory = Factory()

        if self.sqlite and env('DB_CONNECTION') != 'sqlite':
            raise Exception("Cannot run tests without using the 'sqlite' database.")

        if self._has_setup_database:
            self.setUpFactories()

            self.__class__._has_setup_database = False

        if not self.transactions and self.refreshes_database:
            self.refreshDatabase()

    @classmethod
    def setUpClass(cls):
        cls.staticSetUpDatabase()
        if hasattr(cls, 'setUpFactories'):
            cls._has_setup_database = True
        if cls.transactions:
            from config.database import DB
            DB.begin_transaction()

    @classmethod
    def tearDownClass(cls):
        from config.database import DB
        if cls.transactions:
            DB.rollback()
        else:
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
        if hasattr(self, 'setUpFactories'):
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
        if not self.transactions and self.refreshes_database:
            self.tearDownDatabase()
