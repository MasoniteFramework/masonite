from masonite.helpers import compact
import pytest
from masonite.request import Request
from masonite.exceptions import AmbiguousError

class TestCompact:

    def test_compact_returns_dict_of_local_variable(self):
        x = 'hello'
        assert compact(x) == {'x': 'hello'}
    
    def test_works_with_several_variables(self):
        x = 'hello'
        y = 'world'
        assert compact(x, y) == {'x': 'hello', 'y': 'world'}
    
    def test_can_contain_dict(self):
        x = 'hello'
        y = 'world'
        assert compact(x, y, {'z': 'foo'}) == {'x': 'hello', 'y': 'world', 'z': 'foo'}

    def test_exception_on_too_many(self):
        x = 'hello'
        y = 'world'
        with pytest.raises(ValueError):
            compact(x, y, 'z')

    def test_compact_throws_exceptions(self):
        r = Request(None)
        request = r
        with pytest.raises(AmbiguousError):
            compact(request)

    def test_works_with_classes(self):
        request = Request(None)
        assert 'request' in compact(request) 
