import os
from masonite.storage import Storage
import unittest


class TestCompileSass(unittest.TestCase):

    def test_compiles_sass(self):
        Storage().compile_sass()

        self.assertTrue(os.path.exists(os.path.join(os.getcwd(), 'storage/compiled/style.css')))
        os.remove(os.path.join(os.getcwd(), 'storage/compiled/style.css'))
