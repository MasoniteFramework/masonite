import pytest
from masonite.helpers import dot

def test_dot():
    assert dot('hey.dot', compile_to="{1}[{.}]") == "hey[dot]"
    assert dot('hey.dot.another', compile_to="{1}[{.}]") == "hey[dot][another]"
    assert dot('hey.dot.another.and.another', compile_to="{1}[{.}]") == "hey[dot][another][and][another]"
    assert dot('hey.dot', compile_to="{1}/{.}") == "hey/dot"
    assert dot('hey.dot.another', compile_to="{1}/{.}") == "hey/dot/another"
    assert dot('hey.dot.another', compile_to="{1}/{.}") == "hey/dot/another"
    assert dot('hey.dot.another', compile_to="/{1}/{.}") == "/hey/dot/another"
    with pytest.raises(ValueError):
        assert dot('hey.dot.another',
                    compile_to="{1}//{.}") == "hey/dot/another"
