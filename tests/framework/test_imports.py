def test_masonite_import():
    """ Application should be able to import Masonite modules """
    try:
        import masonite
        assert True
    except ImportError:
        assert False, 'Should import Masonite. Package not installed'
