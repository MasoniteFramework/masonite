from masonite.helpers import urls_helpers


def test_get_sets_route():
    assert urls_helpers.get('test', None)


def test_post_sets_route():
    assert urls_helpers.post('test', None)


def test_put_sets_route():
    assert urls_helpers.put('test', None)


def test_delete_sets_route():
    assert urls_helpers.delete('test', None)


def test_patch_sets_route():
    assert urls_helpers.patch('test', None)
