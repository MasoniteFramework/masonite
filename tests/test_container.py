from masonite.app import App
from masonite.request import Request

app = App()
app.bind('Request', Request(None))

def test_container_gets_direct_class():
    assert isinstance(app.make('Request'), Request)


class MockObject:
    pass

class GetObject(MockObject):
    pass

def function_test(MockObject):
    return MockObject

app.bind('MockObject', MockObject)

def test_container_resolves_object():
    assert isinstance(app.resolve(function_test), MockObject.__class__)


def function_test1(mock: MockObject):
    return mock

def test_container_resolving_annotation():
    assert isinstance(app.resolve(function_test1), MockObject.__class__)


def function_test2(mock: MockObject):
    return mock


app.bind('GetObject', GetObject)


def test_container_resolving_instance_of_object():
    # assert isinstance(GetObject, MockObject.__class__)
    assert isinstance(app.resolve(function_test2), GetObject.__class__)


def function_test3(mock: MockObject, request: Request):
    return {'mock': MockObject, 'request': Request}

def test_container_resolving_multiple_annotations():
    assert isinstance(app.resolve(function_test3)['mock'], MockObject.__class__)
    assert isinstance(app.resolve(function_test3)['request'], Request.__class__)