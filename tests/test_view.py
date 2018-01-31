from masonite.view import view

def test_view_compiles_jinja():
    assert view('test', {'test': 'test'}) == 'test'