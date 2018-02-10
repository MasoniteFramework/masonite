from masonite.view import view, View
from masonite.app import App
def test_view_compiles_jinja():
    assert view('test', {'test': 'test'}) == 'test'

def test_view_extends_dictionary():
    container = App()

    container.bind('View', View().render)

    view = container.make('View')

    assert view('test', {'test': 'test'}) == 'test'


def test_view_extends_without_dictionary_parameters():
    container = App()

    view = View()
    view.share({'test': 'test'})

    container.bind('View', view.render)

    view = container.make('View')

    assert view('test') == 'test'


def test_render_from_container_as_view_class():
    container = App()

    ViewClass = View()

    container.bind('ViewClass', ViewClass)
    container.bind('View', ViewClass.render)

    container.make('ViewClass').share({'test': 'test'})

    view = container.make('View')
    assert view('test') == 'test'


def test_composers():
    container = App()

    ViewClass = View()

    container.bind('ViewClass', ViewClass)
    container.bind('View', ViewClass.render)

    container.make('ViewClass').composer('test', {'test': 'test'})

    assert container.make('ViewClass').composers == {'test': {'test': 'test'}}

    view = container.make('View')
    assert view('test') == 'test'


def test_composers_load_all_views_with_astericks():
    container = App()

    ViewClass = View()

    container.bind('ViewClass', ViewClass)
    container.bind('View', ViewClass.render)

    container.make('ViewClass').composer('*', {'test': 'test'})

    assert container.make('ViewClass').composers == {'*': {'test': 'test'}}

    view = container.make('View')
    assert view('test') == 'test'


def test_composers_load_all_views_with_list():
    container = App()

    ViewClass = View()

    container.bind('ViewClass', ViewClass)
    container.bind('View', ViewClass.render)

    container.make('ViewClass').composer(['home', 'test'], {'test': 'test'})

    assert container.make('ViewClass').composers == {
        'home': {'test': 'test'}, 'test': {'test': 'test'}}

    view = container.make('View')
    assert view('test') == 'test'
