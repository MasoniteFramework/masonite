from masonite.stacktrace import StackTrace

try:
    import failmodule
except Exception as e:
    exception = e

def test_stacktrace_is_callable():
    assert callable(StackTrace)

def test_stacktrace_renders_view():
    assert StackTrace(exception).render() == 'test'