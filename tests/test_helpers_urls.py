from masonite.helpers import urls_helpers
from masonite.routes import Get, Post, Delete, Patch, Put


def test_get_sets_route():
    assert urls_helpers.get('test', None)
    assert isinstance(urls_helpers.get('test', None), Get)


def test_post_sets_route():
    assert urls_helpers.post('test', None)
    assert isinstance(urls_helpers.post('test', None), Post)


def test_put_sets_route():
    assert urls_helpers.put('test', None)
    assert isinstance(urls_helpers.put('test', None), Put)


def test_delete_sets_route():
    assert urls_helpers.delete('test', None)
    assert isinstance(urls_helpers.delete('test', None), Delete)


def test_patch_sets_route():
    assert urls_helpers.patch('test', None)
    assert isinstance(urls_helpers.patch('test', None), Patch)
