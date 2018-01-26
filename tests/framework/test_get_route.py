from masonite.routes import Get, Post

GET = Get()
POST = Post()

def test_get_middleware_returns_get():
    assert GET.middleware(True) == GET
    assert GET.middleware(False) == GET

def test_get_name_sets_route_name():
    assert GET.name('routename') == GET
    assert GET.named_route == 'routename'

def test_post_middleware_returns_bool():
    assert POST.middleware(True) == POST
    assert POST.middleware(False) == POST
