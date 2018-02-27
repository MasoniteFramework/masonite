import time
import glob

from config import cache
from masonite.app import App
from masonite.drivers.CacheDiskDriver import CacheDiskDriver
from masonite.managers.CacheManager import CacheManager
from masonite.view import view, View
from masonite.exceptions import RequiredContainerBindingNotFound
import pytest


def test_view_compiles_jinja():
    assert view('test', {'test': 'test'}) == 'test'


def test_view_extends_dictionary():
    container = App()

    view = View(container)

    container.bind('View', view.render)

    view = container.make('View')

    assert view('test', {'test': 'test'}).rendered_template == 'test'


def test_view_extends_without_dictionary_parameters():
    container = App()

    view = View(container)
    view.share({'test': 'test'})

    container.bind('View', view.render)

    view = container.make('View')

    assert view('test').rendered_template == 'test'


def test_render_from_container_as_view_class():
    container = App()

    ViewClass = View(container)

    container.bind('ViewClass', ViewClass)
    container.bind('View', ViewClass.render)

    container.make('ViewClass').share({'test': 'test'})

    view = container.make('View')
    assert view('test').rendered_template == 'test'


def test_composers():
    container = App()

    ViewClass = View(container)

    container.bind('ViewClass', ViewClass)
    container.bind('View', ViewClass.render)

    container.make('ViewClass').composer('test', {'test': 'test'})

    assert container.make('ViewClass').composers == {'test': {'test': 'test'}}

    view = container.make('View')
    assert view('test').rendered_template == 'test'


def test_composers_load_all_views_with_astericks():
    container = App()

    ViewClass = View(container)

    container.bind('ViewClass', ViewClass)
    container.bind('View', ViewClass.render)

    container.make('ViewClass').composer('*', {'test': 'test'})

    assert container.make('ViewClass').composers == {'*': {'test': 'test'}}

    view = container.make('View')
    assert view('test').rendered_template == 'test'


def test_composers_load_all_views_with_list():
    container = App()

    ViewClass = View(container)

    container.bind('ViewClass', ViewClass)
    container.bind('View', ViewClass.render)

    container.make('ViewClass').composer(['home', 'test'], {'test': 'test'})

    assert container.make('ViewClass').composers == {
        'home': {'test': 'test'}, 'test': {'test': 'test'}}

    view = container.make('View')
    assert view('test').rendered_template == 'test'


def test_view_share_updates_dictionary_not_overwrite():
    container = App()

    ViewClass = View(container)

    container.bind('ViewClass', ViewClass)

    viewclass = container.make('ViewClass')

    viewclass.share({'test1': 'test1'})
    viewclass.share({'test2': 'test2'})

    assert viewclass.dictionary == {'test1': 'test1', 'test2': 'test2'}


def test_view_throws_exception_without_cache_binding():
    container = App()

    ViewClass = View(container)

    container.bind('ViewClass', ViewClass)
    container.bind('View', ViewClass.render)

    view = container.make('View')

    with pytest.raises(RequiredContainerBindingNotFound):
        view('test_cache').cache_for('5', 'seconds')


def test_view_cache():
    """
    Test for cache template each 5 min
    """

    container = App()

    view = View(container)

    container.bind('CacheConfig', cache)
    container.bind('CacheDiskDriver', CacheDiskDriver)
    container.bind('CacheManager', CacheManager(container))
    container.bind('Application', container)
    container.bind('Cache', container.make('CacheManager').driver('disk'))
    container.bind('View', view.render)

    view = container.make('View')

    assert view(
        'test_cache', {'test': 'test'}
    ).cache_for(1, 'second').rendered_template == 'test'

    assert open(glob.glob('bootstrap/cache/test_cache:*')[0]).read() == 'test'

    time.sleep(2)

    assert view(
        'test_cache', {'test': 'macho'}
    ).cache_for(5, 'seconds').rendered_template == 'macho'

    time.sleep(2)

    assert open(glob.glob('bootstrap/cache/test_cache:*')[0]).read() == 'macho'

    assert view(
        'test_cache', {'test': 'macho'}
    ).cache_for(1, 'second').rendered_template == 'macho'

    time.sleep(1)

    assert open(glob.glob('bootstrap/cache/test_cache:*')[0]).read() == 'macho'

    assert view(
        'test_cache', {'test': 'macho'}
    ).cache_for('1', 'second').rendered_template == 'macho'
