from masonite.routes import Get, Post

GET = Get()
POST = Post()

def test_get_middleware_returns_bool():
    assert GET.middleware(True) == GET
    assert GET.continueroute == True
    assert GET.middleware(False) == GET
    assert GET.continueroute == False

def test_get_name_sets_route_name():
    assert GET.name('routename') == GET
    assert GET.named_route == 'routename'

def test_post_middleware_returns_bool():
    assert POST.middleware(True) == POST
    assert POST.continueroute == True
    assert POST.middleware(False) == POST
    assert POST.continueroute == False
