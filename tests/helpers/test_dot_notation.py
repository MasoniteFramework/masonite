import pytest
from masonite.helpers import dot, Dot as DictDot


def test_dot():
    assert dot('hey.dot', compile_to="{1}[{.}]") == "hey[dot]"
    assert dot('hey.dot.another', compile_to="{1}[{.}]") == "hey[dot][another]"
    assert dot('hey.dot.another.and.another', compile_to="{1}[{.}]") == "hey[dot][another][and][another]"
    assert dot('hey.dot.another.and.another', compile_to="/{1}[{.}]") == "/hey[dot][another][and][another]"
    assert dot('hey.dot', compile_to="{1}/{.}") == "hey/dot"
    assert dot('hey.dot.another', compile_to="{1}/{.}") == "hey/dot/another"
    assert dot('hey.dot.another', compile_to="{1}/{.}") == "hey/dot/another"
    assert dot('hey.dot.another', compile_to="/{1}/{.}") == "/hey/dot/another"
    with pytest.raises(ValueError):
        assert dot('hey.dot.another', compile_to="{1}//{.}") == "hey/dot/another"

def test_dict_dot():
    assert DictDot().dot('key', {'key': 'value'}) == 'value'
    assert DictDot().dot('key.test', {'key': {'test': 'value'}}) == 'value'
    assert DictDot().dot('key.test.layer', {'key': {'test': {'layer': 'value'}}}) == 'value'
    assert DictDot().dot('key.none', {'key': {'test': {'layer': 'value'}}}) == None
    assert DictDot().dot('key', {'key': {'test': {'layer': 'value'}}}) == {'test': {'layer': 'value'}}
