from masonite.helpers import routes
from masonite.routes import Get, Post, Delete, Patch, Put


class TestHelperUrl:

    def test_get_sets_route(self):
        assert routes.get('test', None)
        assert isinstance(routes.get('test', None), Get)

    def test_post_sets_route(self):
        assert routes.post('test', None)
        assert isinstance(routes.post('test', None), Post)

    def test_put_sets_route(self):
        assert routes.put('test', None)
        assert isinstance(routes.put('test', None), Put)

    def test_delete_sets_route(self):
        assert routes.delete('test', None)
        assert isinstance(routes.delete('test', None), Delete)

    def test_patch_sets_route(self):
        assert routes.patch('test', None)
        assert isinstance(routes.patch('test', None), Patch)
