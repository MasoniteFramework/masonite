
import json
import unittest

from masonite.app import App
from masonite.providers import ValidationProvider
from masonite.validation.Validator import (ValidationFactory, Validator,
                                           accepted, contains, equals,
                                           greater_than, in_range, is_in, isnt)
from masonite.validation.Validator import json as vjson
from masonite.validation.Validator import (length, less_than, none, numeric,
                                           required, string, truthy, when)


class TestValidation(unittest.TestCase):

    def setUp(self):
        pass

    def test_required(self):
        validate = Validator().validate({
            'test': 1
        }, required(['user', 'email']))

        self.assertEqual(validate.errors, ['user is required', 'email is required'])

        validate = Validator().validate({
            'test': 1
        }, required(['test']))

        self.assertEqual(len(validate.errors), 0)

    def test_extendable(self):
        v = Validator()
        v.extend('numeric', numeric)

        validate = v.validate({
            'test': 1
        }, v.numeric(['test']))

        self.assertEqual(len(validate.errors), 0)

    def test_accepted(self):
        validate = Validator().validate({
            'terms': 'on'
        }, accepted(['terms']))

        self.assertEqual(len(validate.errors), 0)

        # validate = Validator().validate({
        #     'terms': 'test'
        # }, accepted(['terms']))

        # self.assertEqual(validate.errors, ['terms must be yes, on, 1 or true'])

    def test_conditional(self):
        validate = Validator().validate({
            'terms': 'on'
        }, when(accepted(['terms'])).then(
            required(['user'])
        ))

        self.assertEqual(validate.errors, ['user is required'])

        validate = Validator().validate({
            'terms': 'test'
        }, accepted(['terms']))

        self.assertEqual(validate.errors, ['terms must be yes, on, 1 or true'])

    def test_error_message_required(self):
        validate = Validator().validate({
            'test': 1
        }, required(['user', 'email'], messages={
            'user': 'there must be a user value'
        }))

        self.assertEqual(validate.errors, ['there must be a user value', 'email is required'])

        validate = Validator().validate({
            'test': 1
        }, required(['user', 'email'], messages={
            'email': 'there must be an email value'
        }))

        self.assertEqual(validate.errors, ['user is required', 'there must be an email value'])

    def test_numeric(self):
        validate = Validator().validate({
            'test': 1
        }, numeric(['test']))

        self.assertEqual(len(validate.errors), 0)

        validate = Validator().validate({
            'test': 'hey'
        }, numeric(['test']))

        self.assertEqual(validate.errors, ['test must be a numeric'])

    def test_several_tests(self):
        validate = Validator().validate({
            'test': 'hey'
        }, required(['notin']), numeric(['notin']))

        self.assertEqual(validate.errors, ['notin is required', 'notin must be a numeric'])

    def test_json(self):
        validate = Validator().validate({
            'json': 'hey'
        }, vjson(['json']))

        self.assertEqual(validate.errors, ['json must be json'])

        validate = Validator().validate({
            'json': json.dumps({'test': 'key'})
        }, vjson(['json']))

        self.assertEqual(len(validate.errors), 0)

    def test_length(self):
        validate = Validator().validate({
            'json': 'hey'
        }, length(['json'], min=1, max=10))

        self.assertEqual(len(validate.errors), 0)

        validate = Validator().validate({
            'json': 'hey'
        }, length(['json'], '1..10'))

        self.assertEqual(len(validate.errors), 0)

        validate = Validator().validate({
            'json': 'this is a really long string'
        }, length(['json'], min=1, max=10))

        self.assertEqual(validate.errors, ['json length must be between 1 and 10'])

    def test_string(self):
        validate = Validator().validate({
            'text': 'hey'
        }, string(['text']))

        self.assertEqual(len(validate.errors), 0)

        validate = Validator().validate({
            'text': 1
        }, string(['text']))

        self.assertEqual(validate.errors, ['text must be a string'])

    def test_none(self):
        validate = Validator().validate({
            'text': None
        }, none(['text']))

        self.assertEqual(len(validate.errors), 0)

        validate = Validator().validate({
            'text': 1
        }, none(['text']))

        self.assertEqual(validate.errors, ['text must be None'])

    def test_equals(self):
        validate = Validator().validate({
            'text': 'test1'
        }, equals(['text'], 'test1'))

        self.assertEqual(len(validate.errors), 0)

        validate = Validator().validate({
            'text': 'test2'
        }, equals(['text'], 'test1'))

        self.assertEqual(validate.errors, ['text must be equal to test1'])

    def test_truthy(self):
        validate = Validator().validate({
            'text': 'value'
        }, truthy(['text']))

        self.assertEqual(len(validate.errors), 0)

        validate = Validator().validate({
            'text': 1
        }, truthy(['text']))

        self.assertEqual(len(validate.errors), 0)

        validate = Validator().validate({
            'text': False
        }, truthy(['text']))

        self.assertEqual(validate.errors, ['text must be a truthy value'])

    def test_in_range(self):
        validate = Validator().validate({
            'text': 52
        }, in_range(['text'], min=25, max=72))

        self.assertEqual(len(validate.errors), 0)

        validate = Validator().validate({
            'text': 101
        }, in_range(['text'], min=25, max=72))

        self.assertEqual(validate.errors, ['text must be between 25 and 72'])

    def test_greater_than(self):
        validate = Validator().validate({
            'text': 52
        }, greater_than(['text'], 25))

        self.assertEqual(len(validate.errors), 0)

        validate = Validator().validate({
            'text': 101
        }, greater_than(['text'], 150))

        self.assertEqual(validate.errors, ['text must be greater than 150'])

    def test_less_than(self):
        validate = Validator().validate({
            'text': 10
        }, less_than(['text'], 25))

        self.assertEqual(len(validate.errors), 0)

        validate = Validator().validate({
            'text': 101
        }, less_than(['text'], 75))

        self.assertEqual(validate.errors, ['text must be less than 75'])

    def test_isnt(self):
        validate = Validator().validate({
            'test': 50
        }, isnt(
            in_range(['test'], min=10, max=20)
        )
        )

        self.assertEqual(len(validate.errors), 0)

        validate = Validator().validate({
            'test': 15
        }, isnt(
            in_range(['test'], min=10, max=20))
        )

        self.assertEqual(validate.errors, ['test must not be between 10 and 20'])

    def test_isnt_equals(self):
        validate = Validator().validate({
            'test': 'test'
        }, isnt(
            equals(['test'], 'test'),
            length(['test'], min=10, max=20)
        )
        )

        # self.assertEqual(validate.errors, ['test must not be equal to test', 'test length must not be between 1 and 4'])
        self.assertEqual(validate.errors, ['test must not be equal to test'])

    def test_contains(self):
        validate = Validator().validate({
            'test': 'this is a sentence'
        }, contains(['test'], 'this'))

        self.assertEqual(len(validate.errors), 0)

        validate = Validator().validate({
            'test': 'this is a not sentence'
        }, contains(['test'], 'test'))

        self.assertEqual(validate.errors, ['test must contain test'])

    def test_is_in(self):
        validate = Validator().validate({
            'test': 1
        }, is_in(['test'], [1, 2, 3]))

        self.assertEqual(len(validate.errors), 0)

        validate = Validator().validate({
            'test': 1
        }, is_in(['test'], [4, 2, 3]))

        self.assertEqual(validate.errors, ['test must contain an element in [4, 2, 3]'])


class TestDotNotationValidation(unittest.TestCase):

    def setUp(self):
        pass

    def test_dot_required(self):
        validate = Validator().validate({
            'user': {
                'email': 'user@example.com'
            }
        }, required(['user.id']))

        self.assertEqual(validate.errors, ['user.id is required'])

        validate = Validator().validate({
            'user': {
                'id': 1
            }
        }, required(['user.id']))

        self.assertEqual(len(validate.errors), 0)

    def test_dot_numeric(self):
        validate = Validator().validate({
            'user': {
                'id': 1,
                'email': 'user@example.com'
            }
        }, numeric(['user.id']))

        self.assertEqual(len(validate.errors), 0)

        validate = Validator().validate({
            'user': {
                'id': 1,
                'email': 'user@example.com'
            }
        }, numeric(['user.email']))

        self.assertEqual(validate.errors, ['user.email must be a numeric'])

    def test_dot_several_tests(self):
        validate = Validator().validate({
            'user': {
                'id': 1,
                'email': 'user@example.com'
            }
        }, required(['user.id', 'user.email']), numeric(['user.id']))

        self.assertEqual(len(validate.errors), 0)

        validate = Validator().validate({
            'user': {
                'id': 1,
                'email': 'user@example.com'
            }
        }, required(['user.id', 'user.email']), numeric(['user.email']))

        self.assertEqual(validate.errors, ['user.email must be a numeric'])

    def test_dot_json(self):
        validate = Validator().validate({
            'user': {
                'id': 1,
                'email': 'user@example.com'
            }
        }, vjson(['user.id']))

        self.assertEqual(validate.errors, ['user.id must be json'])

        validate = Validator().validate({
            'user': {
                'id': 1,
                'email': 'user@example.com',
                'payload': json.dumps({'test': 'key'})
            }
        }, vjson(['user.payload']))

        self.assertEqual(len(validate.errors), 0)

    def test_dot_length(self):
        validate = Validator().validate({
            'user': {
                'id': 1,
                'email': 'user@example.com'
            }
        }, length(['user.id'], min=1, max=10))

        self.assertEqual(len(validate.errors), 0)

        validate = Validator().validate({
            'user': {
                'id': 1,
                'email': 'user@example.com',
                'description': 'this is a really long description'
            }
        }, length(['user.id'], '1..10'))

        self.assertEqual(len(validate.errors), 0)

        validate = Validator().validate({
            'user': {
                'id': 1,
                'email': 'user@example.com',
                'description': 'this is a really long description'
            }
        }, length(['user.description'], min=1, max=10))

        self.assertEqual(validate.errors, ['user.description length must be between 1 and 10'])

    def test_dot_in_range(self):
        validate = Validator().validate({
            'user': {
                'id': 1,
                'email': 'user@example.com',
                'age': 25
            }
        }, in_range(['user.age'], min=25, max=72))

        self.assertEqual(len(validate.errors), 0)

        validate = Validator().validate({
            'user': {
                'id': 1,
                'email': 'user@example.com',
                'age': 25
            }
        }, in_range(['user.age'], min=27, max=72))

        self.assertEqual(validate.errors, ['user.age must be between 27 and 72'])

    def test_dot_equals(self):
        validate = Validator().validate({
            'user': {
                'id': 1,
                'email': 'user@example.com',
                'age': 25
            }
        }, equals(['user.age'], 25))

        self.assertEqual(len(validate.errors), 0)

        validate = Validator().validate({
            'user': {
                'id': 1,
                'email': 'user@example.com',
                'age': 25
            }
        }, equals(['user.age'], 'test1'))

        self.assertEqual(validate.errors, ['user.age must be equal to test1'])

    def test_dot_error_message_required(self):
        validate = Validator().validate({
            'user': {
                'id': 1,
                'email': 'user@example.com',
                'age': 25
            }
        }, required(['user.description'], messages={
            'user.description': 'You are missing a description'
        }))

        self.assertEqual(validate.errors, ['You are missing a description'])

        validate = Validator().validate({
            'user': {
                'id': 1,
                'email': 'user@example.com'
            }
        }, required(['user.id', 'user.email', 'user.age'], messages={
            'user.age': 'You are missing a user age'
        }))

        self.assertEqual(validate.errors, ['You are missing a user age'])


class TestValidationFactory(unittest.TestCase):

    def test_can_register(self):
        factory = ValidationFactory()
        factory.register(required)
        self.assertEqual(factory.registry['required'], required)


class TestValidationProvider(unittest.TestCase):

    def setUp(self):
        from masonite.request import Request
        self.app = App()
        self.app.bind('Request', Request().load_app(self.app))
        self.provider = ValidationProvider().load_app(self.app)
        self.provider.register()
        self.app.resolve(self.provider.boot)

    def test_loaded_validator_class(self):
        self.assertIsInstance(self.app.make(Validator), Validator)

    def test_loaded_registry(self):
        self.assertTrue(self.app.make(Validator).numeric)

    def test_request_validation(self):
        request = self.app.make('Request')
        validate = self.app.make('Validator')

        request.request_variables = {
            'id': 1,
            'name': 'Joe'
        }

        validated = request.validate(
            validate.required(['id', 'name'])
        )

        self.assertEqual(len(validated.errors), 0)

        validated = request.validate(
            validate.required(['user'])
        )

        self.assertEqual(validated.errors, ['user is required'])
