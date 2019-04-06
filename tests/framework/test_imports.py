from unittest import TestCase

class TestMasoniteImport(TestCase):

    def test_masonite_import(self):
        """ Application should be able to import Masonite modules """
        try:
            import masonite
        except ImportError:
            self.fail('Should import Masonite. Package not installed')
