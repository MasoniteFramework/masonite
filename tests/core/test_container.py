from src.masonite.app import App
from src.masonite.request import Request
from src.masonite.drivers import UploadDiskDriver
from src.masonite.contracts import UploadContract
from src.masonite.exceptions import ContainerError, StrictContainerException

import unittest


class MockObject:
    pass


class MockSelfObject:

    def __init__(self):
        self.id = 1

    def get_id(self):
        return self.id


class GetObject(MockObject):

    def find(self):
        return 1


class GetAnotherObject(MockObject):

    def find(self):
        return 2


class MakeObject:
    pass


class SubstituteThis:
    pass


class TestContainer(unittest.TestCase):

    def setUp(self):
        self.app = App()
        self.app.bind('Request', Request(None))
        self.app.bind('MockObject', MockObject)
        self.app.bind('GetObject', GetObject)
        self.app.bind('Container', self.app)

    def test_container_gets_direct_class(self):
        self.assertIsInstance(self.app.make('Request'), Request)

    def test_container_resolving_annotation(self):
        self.assertIsInstance(self.app.resolve(self._function_test_annotation), MockObject)

    def _function_test_annotation(self, mock: MockObject):
        return mock

    def test_container_resolving_instance_of_object(self):
        self.app = App()
        self.app.bind('Get', GetObject)
        self.assertIsInstance(self.app.resolve(self._function_test_annotation), GetObject)

    def test_container_resolving_similiar_objects(self):
        self.app.bind('GetAnotherObject', GetAnotherObject)

        obj = self.app.resolve(self._function_test_find_method_on_similiar_objects)
        self.assertEqual(obj[0], 2)
        self.assertEqual(obj[1], 1)

    def _function_test_find_method_on_similiar_objects(self, user: GetAnotherObject, country: GetObject):
        return [user.find(), country.find()]

    def test_raises_error_when_getting_instances_of_classes(self):
        with self.assertRaises(ContainerError):
            self.assertTrue(self.app.resolve(self._function_test_find_method_on_similiar_objects))

    def _function_test_double_annotations(self, mock: MockObject, request: Request):
        return {'mock': mock, 'request': request}

    def test_container_resolving_multiple_annotations(self):
        self.assertIsInstance(self.app.resolve(self._function_test_double_annotations)['mock'], MockObject)
        self.assertIsInstance(self.app.resolve(self._function_test_double_annotations)['request'], Request)

    def test_container_contract_returns_upload_disk_driver(self):
        self.app.bind('UploadDiskDriver', UploadDiskDriver)
        self.assertIsInstance(self.app.resolve(self._function_test_contracts), UploadDiskDriver)

    def _function_test_contracts(self, upload: UploadContract):
        return upload

    def _function_not_in_container(self, NotIn):
        return NotIn

    def test_container_raises_value_error(self):
        with self.assertRaises(ContainerError):
            self.assertTrue(self.app.resolve(self._function_not_in_container))

    def test_container_collects_correct_objects(self):
        self.app.bind('ExceptionHook', object)
        self.app.bind('SentryExceptionHook', object)
        self.app.bind('ExceptionHandler', object)

        self.assertEqual(self.app.collect('*ExceptionHook'), {'ExceptionHook': object, 'SentryExceptionHook': object})
        self.assertEqual(self.app.collect('Exception*'), {'ExceptionHook': object, 'ExceptionHandler': object})
        self.assertEqual(self.app.collect('Sentry*Hook'), {'SentryExceptionHook': object})
        with self.assertRaises(AttributeError):
            self.app.collect('Sentry')

    def test_container_collects_correct_subclasses_of_objects(self):
        self.app.bind('GetAnotherObject', GetAnotherObject)
        objects = self.app.collect(MockObject)

        self.assertIn('GetAnotherObject', objects)
        self.assertIn('GetObject', objects)

    def test_container_makes_from_class(self):
        self.assertIsInstance(self.app.make(Request), Request)

    def test_container_can_bind_and_make_from_class_key(self):
        self.app.bind(MakeObject, MakeObject)
        self.assertIsInstance(self.app.make(MakeObject), MakeObject)

    def test_container_makes_from_base_class(self):
        del self.app.providers['MockObject']
        self.assertIsInstance(self.app.make(MockObject), GetObject)

    def test_container_has_obj(self):
        assert self.app.has('Request')
        assert self.app.has(Request)

    def test_container_makes_from_contract(self):
        self.app.bind('UploadDriver', UploadDiskDriver)
        self.assertIsInstance(self.app.make(UploadContract), UploadDiskDriver)

    def test_strict_container_raises_exception(self):
        self.app = App(strict=True)

        self.app.bind('Request', object)

        with self.assertRaises(StrictContainerException):
            self.app.bind('Request', object)

    def test_override_container_does_not_override(self):
        self.app = App(override=False)

        self.app.bind('Request', 'test')
        self.app.bind('Request', 'override')
        self.assertEqual(self.app.make('Request'), 'test')

    def test_app_simple_bind(self):
        app = App()
        app.simple(Request)
        self.assertEqual(app.providers, {Request: Request})

    def test_app_simple_bind_init(self):
        app = App()
        req = Request()
        app.simple(req)
        self.assertEqual(app.providers, {Request: req})

    def test_app_make_after_simple_bind(self):
        app = App()
        req = Request()
        app.simple(req)
        self.assertEqual(app.make(Request), req)

    def test_can_pass_variables(self):
        app = App()
        req = Request()
        app.bind('Request', req)
        obj = app.resolve(self._test_resolves_variables, 'test1', 'test2')
        self.assertEqual(obj[0], 'test1')
        self.assertEqual(obj[1], req)
        self.assertEqual(obj[2], 'test2')

    def _test_resolves_variables(self, var1, request: Request, var2):
        return [var1, request, var2]

    def test_can_substitute(self):
        app = App()
        app.swap(SubstituteThis, self._substitute)

        self.assertEqual(app.resolve(self._test_substitute), 'test')

    def test_can_substitute_with_object(self):
        app = App()
        app.swap(SubstituteThis, MakeObject())

        self.assertIsInstance(app.resolve(self._test_substitute), MakeObject)

    def test_instantiates_obj(self):
        app = App()
        app.bind('MockSelf', MockSelfObject)

        self.assertEqual(app.resolve(self._test_self_object).id, 1)

    def test_can_use_in_keyword(self):
        app = App()
        app.bind('test', 'value')

        self.assertIn('test', app)

    def test_can_substitute_with_make_object(self):
        app = App()
        app.swap(SubstituteThis, MakeObject())

        self.assertIsInstance(app.make(SubstituteThis), MakeObject)

    def _substitute(self, _, __):
        return 'test'

    def _test_substitute(self, test: SubstituteThis):
        return test

    def _test_self_object(self, obj: MockSelfObject):
        return obj
