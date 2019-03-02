from masonite.helpers import compact
import pytest
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