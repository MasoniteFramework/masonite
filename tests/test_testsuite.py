from masonite.testsuite.TestSuite import TestSuite


def test_testsuite_creates_container():
    suite = TestSuite().create_container()

    container = suite.get_container()

    assert container.make('Request')


def test_testsuite_should_return_route_exists():
    suite = TestSuite().create_container()
    container = suite.get_container()

    assert suite.route('/test').exists() is True


def test_testsuite_route_should_return_bool_if_has_middleware():
    suite = TestSuite().create_container()
    container = suite.get_container()

    assert suite.route('/test').has_middleware('auth') is True
    assert suite.route('/test').has_middleware('none') is False
