from masonite.helpers import optional, optional_call

class MockUser:
    id = 1

class TestOptional:

    def test_optional_returns_object_id(self):
        assert optional(MockUser).id == 1
        assert optional(object).id == None
        assert optional(None).id == None
        assert optional(object).instance() == object
    
    def test_optional_can_handle_method_calls(self):
        assert optional_call(MockUser).method() == None
