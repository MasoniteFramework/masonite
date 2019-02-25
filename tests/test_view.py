import glob
import time

import pytest
from jinja2 import FileSystemLoader, PackageLoader

from config import cache
from masonite.app import App
from masonite.drivers.CacheDiskDriver import CacheDiskDriver
from masonite.exceptions import RequiredContainerBindingNotFound, ViewException
from masonite.managers.CacheManager import CacheManager
from masonite.view import View


class TestView:

    def setup_method(self):
        self.container = App()
        view = View(self.container)

        self.container.bind('View', view.render)
        self.container.bind('ViewClass', view)

    def test_view_extends_dictionary(self):
        view = self.container.make('View')

        assert view('test', {'test': 'test'}).rendered_template == 'test'

    def test_view_exists(self):
        view = self.container.make('ViewClass')

        assert view.exists('index')
        assert view.exists('not_available') is False

    def test_view_render_does_not_keep_previous_variables(self):
        view = self.container.make('ViewClass')

        view.render('test', {'var1': 'var1'})
        view.render('test', {'var2': 'var2'})

        assert 'var1' not in view.dictionary
        assert 'var2' in view.dictionary

    def test_global_view_exists(self):
        view = self.container.make('ViewClass')

        assert view.exists('/resources/templates/index')
        assert view.exists('/resources/templates/not_available') is False

    def test_view_gets_global_template(self):
        view = self.container.make('View')

        assert view('/storage/test', {'test': 'test'}
                    ).rendered_template == 'test'
        assert view('/storage/static/test',
                    {'test': 'test'}).rendered_template == 'test'

    def test_view_extends_without_dictionary_parameters(self):
        view = self.container.make('ViewClass')
        view.share({'test': 'test'})
        view = self.container.make('View')

        assert view('test').rendered_template == 'test'

    def test_render_from_container_as_view_class(self):
        self.container.make('ViewClass').share({'test': 'test'})

        view = self.container.make('View')
        assert view('test').rendered_template == 'test'

    def test_composers(self):
        self.container.make('ViewClass').composer('test', {'test': 'test'})
        view = self.container.make('View')

        assert self.container.make('ViewClass').composers == {
            'test': {'test': 'test'}}
        assert view('test').rendered_template == 'test'

    def test_composers_load_all_views_with_astericks(self):

        self.container.make('ViewClass').composer('*', {'test': 'test'})

        assert self.container.make('ViewClass').composers == {
            '*': {'test': 'test'}}

        view = self.container.make('View')
        assert view('test').rendered_template == 'test'

    def test_composers_with_wildcard_base_view(self):
        self.container.make('ViewClass').composer('mail*', {'to': 'test_user'})

        assert self.container.make('ViewClass').composers == {
            'mail*': {'to': 'test_user'}}

        view = self.container.make('View')
        assert 'test_user' in view('mail/welcome').rendered_template

    def test_composers_with_wildcard_base_view_route(self):
        self.container.make('ViewClass').composer('mail*', {'to': 'test_user'})

        assert self.container.make('ViewClass').composers == {
            'mail*': {'to': 'test_user'}}

        view = self.container.make('View')
        assert 'test_user' in view('mail/welcome').rendered_template

    def test_render_deep_in_file_structure_with_package_loader(self):

        self.container.make('ViewClass').add_environment('storage')

        view = self.container.make('View')
        assert view('/storage/templates/tests/test',
                    {'test': 'testing'}).rendered_template == 'testing'

    def test_composers_with_wildcard_lower_directory_view(self):
        self.container.make('ViewClass').composer(
            'mail/welcome*', {'to': 'test_user'})

        assert self.container.make('ViewClass').composers == {
            'mail/welcome*': {'to': 'test_user'}}

        view = self.container.make('View')
        assert 'test_user' in view('mail/welcome').rendered_template

    def test_composers_with_wildcard_lower_directory_view_and_incorrect_shortend_wildcard(self):
        self.container.make('ViewClass').composer(
            'mail/wel*', {'to': 'test_user'})

        assert self.container.make('ViewClass').composers == {
            'mail/wel*': {'to': 'test_user'}}

        view = self.container.make('View')
        assert 'test_user' not in view('mail/welcome').rendered_template

    def test_composers_load_all_views_with_list(self):
        self.container.make('ViewClass').composer(
            ['home', 'test'], {'test': 'test'})

        assert self.container.make('ViewClass').composers == {
            'home': {'test': 'test'}, 'test': {'test': 'test'}}

        view = self.container.make('View')
        assert view('test').rendered_template == 'test'

    def test_view_share_updates_dictionary_not_overwrite(self):
        viewclass = self.container.make('ViewClass')

        viewclass.share({'test1': 'test1'})
        viewclass.share({'test2': 'test2'})

        assert viewclass._shared == {'test1': 'test1', 'test2': 'test2'}
        viewclass.render('test', {'var1': 'var1'})
        assert viewclass.dictionary == {'test1': 'test1', 'test2': 'test2', 'var1': 'var1'}

    def test_adding_environment(self):
        viewclass = self.container.make('ViewClass')

        viewclass.add_environment('storage', loader=FileSystemLoader)

        assert viewclass.render(
            'test_location', {'test': 'testing'}).rendered_template == 'testing'

    def test_view_throws_exception_without_cache_binding(self):
        view = self.container.make('View')

        with pytest.raises(RequiredContainerBindingNotFound):
            view('test_cache').cache_for('5', 'seconds')

    def test_view_can_add_custom_filters(self):
        view = self.container.make('ViewClass')

        view.filter('slug', self._filter_slug)

        assert view._filters == {'slug': self._filter_slug}
        assert view.render(
            'filter', {'test': 'test slug'}).rendered_template == 'test-slug'

    @staticmethod
    def _filter_slug(item):
        return item.replace(' ', '-')

    def test_view_cache_caches_files(self):

        self.container.bind('CacheConfig', cache)
        self.container.bind('CacheDiskDriver', CacheDiskDriver)
        self.container.bind('CacheManager', CacheManager(self.container))
        self.container.bind('Application', self.container)
        self.container.bind('Cache', self.container.make(
            'CacheManager').driver('disk'))

        view = self.container.make('View')

        assert view(
            'test_cache', {'test': 'test'}
        ).cache_for(1, 'second').rendered_template == 'test'

        assert open(glob.glob('bootstrap/cache/test_cache:*')
                    [0]).read() == 'test'

        time.sleep(2)

        assert view(
            'test_cache', {'test': 'macho'}
        ).cache_for(5, 'seconds').rendered_template == 'macho'

        time.sleep(2)

        assert open(glob.glob('bootstrap/cache/test_cache:*')
                    [0]).read() == 'macho'

        assert view(
            'test_cache', {'test': 'macho'}
        ).cache_for(1, 'second').rendered_template == 'macho'

        time.sleep(1)

        assert open(glob.glob('bootstrap/cache/test_cache:*')
                    [0]).read() == 'macho'

        assert view(
            'test_cache', {'test': 'macho'}
        ).cache_for('1', 'second').rendered_template == 'macho'

    def test_cache_throws_exception_with_incorrect_cache_type(self):
        self.container.bind('CacheConfig', cache)
        self.container.bind('CacheDiskDriver', CacheDiskDriver)
        self.container.bind('CacheManager', CacheManager(self.container))
        self.container.bind('Application', self.container)
        self.container.bind('Cache', self.container.make(
            'CacheManager').driver('disk'))

        view = self.container.make('View')

        with pytest.raises(ValueError):
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

        assert 'John' in view('mail.welcome', {'to': 'John'}).rendered_template
        assert view('mail.composers', {'test': 'John'}).rendered_template == 'John'
        assert view('mail.share').rendered_template == 'John'
        assert 'John' in view('mail/welcome', {'to': 'John'}).rendered_template

        self.container.make('ViewClass').set_splice('@')

        assert 'John' in view('mail@welcome', {'to': 'John'}).rendered_template
        assert 'John' in view('mail@composers', {'test': 'John'}).rendered_template == 'John'
        assert 'John' in view('mail/welcome', {'to': 'John'}).rendered_template

    def test_can_add_tests_to_view(self):
        view = self.container.make('ViewClass')

        view.test('admin', self._is_admin)

        assert view._tests == {'admin': self._is_admin}

        user = MockAdminUser
        assert view.render(
            'admin_test', {'user': user}).rendered_template == 'True'

        user.admin = 0

        assert view.render(
            'admin_test', {'user': user}).rendered_template == 'False'

    def _is_admin(self, obj):
        return obj.admin == 1

    def test_can_render_pubjs(self):
        view = self.container.make('ViewClass')
        view.add_extension('pypugjs.ext.jinja.PyPugJSExtension')
        assert view._jinja_extensions == ['jinja2.ext.loopcontrols', 'pypugjs.ext.jinja.PyPugJSExtension']

        assert view.render(
            'pug/hello.pug', {'name': 'Joe'}).rendered_template == '<p>hello Joe</p>'

    def test_throws_exception_on_incorrect_type(self):
        view = self.container.make('ViewClass')
        with pytest.raises(ViewException):
            assert view.render('test', {'', ''})


class MockAdminUser:
    admin = 1
