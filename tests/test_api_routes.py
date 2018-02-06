from masonite.routes import Api

def test_api_is_callable():
    assert callable(Api)

def test_default_method_type():
    assert Api().method_type == 'POST'

def test_load_routes():
    api = Api().route('/api/test')
    assert api.url == '/api/test'

def test_load_model():
    api = Api().model(object)
    assert api.model_obj == object

def test_exclude():
    api = Api().model(object).exclude(['username', 'password'])
    assert api.exclude_list == ['username', 'password']