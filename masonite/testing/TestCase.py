import io
import json
import unittest
from contextlib import contextmanager
from urllib.parse import urlencode

from masonite import env
from masonite.helpers.routes import flatten_routes, create_matchurl
from masonite.helpers.migrations import Migrations
from masonite.testsuite import generate_wsgi
from orator.orm import Factory

from .MockRoute import MockRoute


class TestCase(unittest.TestCase):

    sqlite = True
    transactions = True
    refreshes_database = False
    _transaction = False

    def setUp(self):
        from wsgi import container
        self.container = container
        self.acting_user = False
        self.factory = Factory()
        self.withoutExceptionHandling()
        self.withoutCsrf()
        if not self._transaction:
            self.startTransaction()
            if hasattr(self, 'setUpFactories'):
                self.setUpFactories()

        if self.sqlite and env('DB_CONNECTION') != 'sqlite':
            raise Exception("Cannot run tests without using the 'sqlite' database.")

        if not self.transactions and self.refreshes_database:
            self.refreshDatabase()

    @classmethod
    def setUpClass(cls):
        cls.staticSetUpDatabase()

    @classmethod
    def tearDownClass(cls):
        if not cls.refreshes_database and cls.transactions:
            cls.staticStopTransaction()
        else:
            cls.staticTearDownDatabase()

    def refreshDatabase(self):
        if not self.refreshes_database and self.transactions:
            self.stopTransaction()
            self.startTransaction()
            if hasattr(self, 'setUpFactories'):
                self.setUpFactories()
        else:
            self.tearDownDatabase()
            self.setUpDatabase()

    def startTransaction(self):
        from config.database import DB
        DB.begin_transaction()
        self.__class__._transaction = True

    def stopTransaction(self):
        from config.database import DB
        DB.rollback()
        self.__class__._transaction = False

    @classmethod
    def staticStopTransaction(cls):
        from config.database import DB
        DB.rollback()
        cls._transaction = False

    def make(self, model, factory, amount=50):
        self.registerFactory(model, factory)
        self.makeFactory(model, amount)

    def makeFactory(self, model, amount):
        return self.factory(model, amount).create()

    def registerFactory(self, model, callable_factory):
        self.factory.register(model, callable_factory)

    def setUpDatabase(self):
        self.tearDownDatabase()
        Migrations().run()
        if hasattr(self, 'setUpFactories'):
            self.setUpFactories()

    def tearDownDatabase(self):
        Migrations().reset()

    @staticmethod
    def staticSetUpDatabase():
        Migrations().run()

    @staticmethod
    def staticTearDownDatabase():
        Migrations().reset()

    def tearDown(self):
        if not self.transactions and self.refreshes_database:
            self.tearDownDatabase()

    def call(self, method, url, params, wsgi={}):
        custom_wsgi = {
            'PATH_INFO': url,
            'REQUEST_METHOD': method
        }

        custom_wsgi.update(wsgi)
        if not self._with_csrf:
            params.update({'__token': 'tok'})
            custom_wsgi.update({
                'HTTP_COOKIE': 'csrf_token=tok',
                'CONTENT_LENGTH': len(str(json.dumps(params))),
                'wsgi.input': io.BytesIO(bytes(json.dumps(params), 'utf-8')),
            })

        custom_wsgi.update({
            'QUERY_STRING': urlencode(params),
        })

        self.run_container(custom_wsgi)
        self.container.make('Request').request_variables = params
        return self.route(url, method)

    def get(self, url, params={}):
        return self.call('GET', url, params)

    def json(self, method, url, params={}):
        return self.call(method, url, params, wsgi={
            'CONTENT_TYPE': 'application/json',
            'CONTENT_LENGTH': len(str(json.dumps(params))),
            'wsgi.input': io.BytesIO(bytes(json.dumps(params), 'utf-8')),
        })

    def post(self, url, params={}):
        return self.call('POST', url, params)

    def put(self, url, params={}):
        return self.json('PUT', url, params)

    def patch(self, url, params={}):
        return self.json('PATCH', url, params)

    def delete(self, url, params={}):
        return self.json('DELETE', url, params)

    def actingAs(self, user):
        if not user:
            raise TypeError("Cannot act as a user of type: {}".format(type(user)))
        self.acting_user = user
        return self

    def route(self, url, method=False):
        for route in self.container.make('WebRoutes'):
            matchurl = create_matchurl(url, route)
            if matchurl.match(url) and method in route.method_type:
                return MockRoute(route, self.container)

    def routes(self, routes):
        self.container.bind('WebRoutes', flatten_routes(self.container.make('WebRoutes') + routes))

    @contextmanager
    def captureOutput(self):
        new_out, new_err = StringIO(), StringIO()
        old_out, old_err = sys.stdout, sys.stderr
        try:
            sys.stdout, sys.stderr = new_out, new_err
            yield sys.stdout, sys.stderr
        finally:
            sys.stdout, sys.stderr = old_out, old_err

    def run_container(self, wsgi_values={}):
        wsgi = generate_wsgi()
        wsgi.update(wsgi_values)
        self.container.bind('Environ', wsgi)
        self.container.make('Request')._test_user = self.acting_user
        try:
            for provider in self.container.make('WSGIProviders'):
                self.container.resolve(provider.boot)
        except Exception as e:
            if self._exception_handling:
                self.container.make('ExceptionHandler').load_exception(e)
            else:
                raise e

    def withExceptionHandling(self):
        self._exception_handling = True

    def withoutExceptionHandling(self):
        self._exception_handling = False

    def withCsrf(self):
        self._with_csrf = True

    def withoutCsrf(self):
        self._with_csrf = False

    def assertDatabaseHas(self, schema, value):
        from config.database import DB

        table = schema.split('.')[0]
        column = schema.split('.')[1]

        self.assertTrue(DB.table(table).where(column, value).first())

    def assertDatabaseNotHas(self, schema, value):
        from config.database import DB

        table = schema.split('.')[0]
        column = schema.split('.')[1]

        self.assertFalse(DB.table(table).where(column, value).first())
