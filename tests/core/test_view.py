import glob
import time

from jinja2 import FileSystemLoader

from config import cache
from masonite.app import App
from masonite.drivers import CacheDiskDriver
from masonite.exceptions import RequiredContainerBindingNotFound, ViewException
from masonite.managers.CacheManager import CacheManager
from masonite.view import View
import unittest


class TestView(unittest.TestCase):

    def setUp(self):
        self.container = App()
        view = View(self.container)

        self.container.bind('View', view.render)
        self.container.bind('ViewClass', view)

    def test_view_extends_dictionary(self):
        view = self.container.make('View')

        self.assertEqual(view('test', {'test': 'test'}).rendered_template, 'test')

    def test_view_exists(self):
        view = self.container.make('ViewClass')

        assert view.exists('index')
        self.assertFalse(view.exists('not_available'))

    def test_view_render_does_not_keep_previous_variables(self):
        view = self.container.make('ViewClass')

        view.render('test', {'var1': 'var1'})
        view.render('test', {'var2': 'var2'})

        self.assertNotIn('var1', view.dictionary)
        self.assertIn('var2', view.dictionary)

    def test_global_view_exists(self):
        view = self.container.make('ViewClass')

        self.assertTrue(view.exists('/resources/templates/index'))
        self.assertFalse(view.exists('/resources/templates/not_available'))

    def test_view_gets_global_template(self):
        view = self.container.make('View')
        self.assertEqual(view('/templates/test', {'test': 'test'}).rendered_template, 'test')

    def test_view_extends_without_dictionary_parameters(self):
        view = self.container.make('ViewClass')
        view.share({'test': 'test'})
        view = self.container.make('View')

        self.assertEqual(view('test').rendered_template, 'test')

    def test_render_from_container_as_view_class(self):
        self.container.make('ViewClass').share({'test': 'test'})

        view = self.container.make('View')
        self.assertEqual(view('test').rendered_template, 'test')

    def test_composers(self):
        self.container.make('ViewClass').composer('test', {'test': 'test'})
        view = self.container.make('View')

        self.assertEqual(self.container.make('ViewClass').composers, {'test': {'test': 'test'}})
        self.assertEqual(view('test').rendered_template, 'test')

    def test_composers_load_all_views_with_astericks(self):

        self.container.make('ViewClass').composer('*', {'test': 'test'})

        self.assertEqual(self.container.make('ViewClass').composers, {'*': {'test': 'test'}})

        view = self.container.make('View')
        self.assertEqual(view('test').rendered_template, 'test')

    def test_composers_with_wildcard_base_view(self):
        self.container.make('ViewClass').composer('mail*', {'to': 'test_user'})

        self.assertEqual(self.container.make('ViewClass').composers, {'mail*': {'to': 'test_user'}})

        view = self.container.make('View')
        self.assertIn('test_user', view('mail/welcome').rendered_template)

    def test_composers_with_wildcard_base_view_route(self):
        self.container.make('ViewClass').composer('mail*', {'to': 'test_user'})

        self.assertEqual(self.container.make('ViewClass').composers, {'mail*': {'to': 'test_user'}})

        view = self.container.make('View')
        self.assertIn('test_user', view('mail/welcome').rendered_template)

    def test_render_deep_in_file_structure_with_package_loader(self):

        self.container.make('ViewClass').add_environment('storage')

        view = self.container.make('View')
        self.assertEqual(view('/templates/tests/test', {'test': 'testing'}).rendered_template, 'testing')

    def test_composers_with_wildcard_lower_directory_view(self):
        self.container.make('ViewClass').composer(
            'mail/welcome*', {'to': 'test_user'})

        self.assertEqual(self.container.make('ViewClass').composers, {'mail/welcome*': {'to': 'test_user'}})

        view = self.container.make('View')
        self.assertIn('test_user', view('mail/welcome').rendered_template)

    def test_composers_with_wildcard_lower_directory_view_and_incorrect_shortend_wildcard(self):
        self.container.make('ViewClass').composer(
            'mail/wel*', {'to': 'test_user'})

        self.assertEqual(self.container.make('ViewClass').composers, {'mail/wel*': {'to': 'test_user'}})

        view = self.container.make('View')
        assert 'test_user' not in view('mail/welcome').rendered_template

    def test_composers_load_all_views_with_list(self):
        self.container.make('ViewClass').composer(
            ['home', 'test'], {'test': 'test'})

        self.assertEqual(self.container.make('ViewClass').composers, {'home': {'test': 'test'}, 'test': {'test': 'test'}})

        view = self.container.make('View')
        self.assertEqual(view('test').rendered_template, 'test')

    def test_view_share_updates_dictionary_not_overwrite(self):
        viewclass = self.container.make('ViewClass')

        viewclass.share({'test1': 'test1'})
        viewclass.share({'test2': 'test2'})

        self.assertEqual(viewclass._shared, {'test1': 'test1', 'test2': 'test2'})
        viewclass.render('test', {'var1': 'var1'})
        self.assertEqual(viewclass.dictionary, {'test1': 'test1', 'test2': 'test2', 'var1': 'var1'})

    def test_adding_environment(self):
        viewclass = self.container.make('ViewClass')

        viewclass.add_environment('storage', loader=FileSystemLoader)

        self.assertEqual(viewclass.render('test_location', {'test': 'testing'}).rendered_template, 'testing')

    def test_view_throws_exception_without_cache_binding(self):
        view = self.container.make('View')

        with self.assertRaises(RequiredContainerBindingNotFound):
            view('test_cache').cache_for('5', 'seconds')

    def test_view_can_add_custom_filters(self):
        view = self.container.make('ViewClass')

        view.filter('slug', self._filter_slug)

        self.assertEqual(view._filters, {'slug': self._filter_slug})
        self.assertEqual(view.render('filter', {'test': 'test slug'}).rendered_template, 'test-slug')

    @staticmethod
    def _filter_slug(item):
        return item.replace(' ', '-')

    def test_view_cache_caches_files(self):

        # self.container.bind('CacheConfig', cache)
        self.container.bind('CacheDiskDriver', CacheDiskDriver)
        self.container.bind('CacheManager', CacheManager(self.container))
        self.container.bind('Application', self.container)
        self.container.bind('Cache', self.container.make(
            'CacheManager').driver('disk'))

        view = self.container.make('View')

        self.assertEqual(view('test_cache', {'test': 'test'}).cache_for(1, 'second').rendered_template, 'test')

        self.assertEqual(open(glob.glob('bootstrap/cache/test_cache:*')[0]).read(), 'test')

        time.sleep(2)

        self.assertEqual(view('test_cache', {'test': 'macho'}).cache_for(5, 'seconds').rendered_template, 'macho')

        time.sleep(2)

        self.assertEqual(open(glob.glob('bootstrap/cache/test_cache:*')[0]).read(), 'macho')

        self.assertEqual(view('test_cache', {'test': 'macho'}).cache_for(1, 'second').rendered_template, 'macho')

        time.sleep(1)

        self.assertEqual(open(glob.glob('bootstrap/cache/test_cache:*')[0]).read(), 'macho')

        self.assertEqual(view('test_cache', {'test': 'macho'}).cache_for('1', 'second').rendered_template, 'macho')

    def test_cache_throws_exception_with_incorrect_cache_type(self):
        # self.container.bind('CacheConfig', cache)
        self.container.bind('CacheDiskDriver', CacheDiskDriver)
        self.container.bind('CacheManager', CacheManager(self.container))
        self.container.bind('Application', self.container)
        self.container.bind('Cache', self.container.make(
            'CacheManager').driver('disk'))

        view = self.container.make('View')

        with self.assertRaises(ValueError):
            view(
                'test_exception', {'test': 'test'}
            ).cache_for(1, 'monthss')

    def test_view_can_change_template_splice(self):
        self.container.make('ViewClass').set_splice('.')

        view = self.container.make('View')
        self.container.make('ViewClass').composer(
            'mail/welcome', {'test': 'test'})
        self.container.make('ViewClass').share(
            {'test': 'John'})

        self.assertIn('John', view('mail.welcome', {'to': 'John'}).rendered_template)
        self.assertEqual(view('mail.composers', {'test': 'John'}).rendered_template, 'John')
        self.assertEqual(view('mail.share').rendered_template, 'John')
        self.assertIn('John', view('mail/welcome', {'to': 'John'}).rendered_template)

        self.container.make('ViewClass').set_splice('@')

        self.assertIn('John', view('mail@welcome', {'to': 'John'}).rendered_template)
        self.assertIn('John', view('mail@composers', {'test': 'John'}).rendered_template)
        self.assertIn('John', view('mail/welcome', {'to': 'John'}).rendered_template)

    def test_can_add_tests_to_view(self):
        view = self.container.make('ViewClass')

        view.test('admin', self._is_admin)

        self.assertEqual(view._tests, {'admin': self._is_admin})

        user = MockAdminUser
        self.assertEqual(view.render('admin_test', {'user': user}).rendered_template, 'True')

        user.admin = 0

        self.assertEqual(view.render('admin_test', {'user': user}).rendered_template, 'False')

    def _is_admin(self, obj):
        return obj.admin == 1

    def test_can_render_pubjs(self):
        view = self.container.make('ViewClass')
        view.add_extension('pypugjs.ext.jinja.PyPugJSExtension')
        self.assertEqual(view._jinja_extensions, ['jinja2.ext.loopcontrols', 'pypugjs.ext.jinja.PyPugJSExtension'])

        self.assertEqual(view.render('pug/hello.pug', {'name': 'Joe'}).rendered_template, '<p>hello Joe</p>')

    def test_throws_exception_on_incorrect_type(self):
        view = self.container.make('ViewClass')
        with self.assertRaises(ViewException):
            assert view.render('test', {'', ''})

    def test_can_use_dot_templates(self):
        view = self.container.make('ViewClass')
        self.assertEqual(view.render('mail.share', {'test': 'test'}).rendered_template, 'test')

    def test_can_use_at_line_statements(self):
        view = self.container.make('ViewClass')
        self.assertIn('test this string', view.render('line-statements', {'test': 'test this string'}).rendered_template)


class MockAdminUser:
    admin = 1
