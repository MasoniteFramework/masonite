from masonite.routes import Get, Post

def test_get_initialized():
    assert callable(Get)
    assert callable(Post)

def test_get_sets_route():
    assert Get().route('test', None)

def test_sets_name():
    get = Get().route('test', None).name('test')

    assert get.named_route == 'test'

def test_loads_request():
    get = Get().route('test', None).name('test').load_request('test')

    assert get.request == 'test'

def test_loads_middleware():
    get = Get().route('test', None).middleware('auth', 'middleware')

    assert get.list_middleware == ('auth', 'middleware')

def test_method_type():
    assert Post().method_type == 'POST'
    assert Get().method_type == 'GET'