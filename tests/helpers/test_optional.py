from masonite.helpers import optional

class MockUser:
    id = 1

class CallThis:

    def method(self, var):
        self.test = var
        return self

class TestOptional:

    def test_optional_returns_object_id(self):
        assert optional(MockUser).id == 1
        assert optional(object).id == None
        assert optional(None).id == None
        assert optional(object).instance() == object
    
    def test_optional_can_handle_method_calls(self):
        assert optional(MockUser).method() == None
        assert not optional(MockUser).method()
        assert optional(CallThis()).method('test').test == 'test'
