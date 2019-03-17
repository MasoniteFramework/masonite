from masonite.request import Request

class MockUser:
    pass

class InsteadOf:

    def __init__(self, cls, method):
        self.cls = cls
        self.method = method
    
    def _return(self, value):
        setattr(self.cls, self.method, value)
        return self.cls

def test_user():
    return MockUser

def test_instead_of_attribute():
    request = Request()

    InsteadOf(request, 'user')._return('awesome')

    assert request.user == 'awesome'

def test_instead_of_with_method():
    request = Request()

    InsteadOf(request, 'user')._return(test_user)

    assert request.user() == MockUser