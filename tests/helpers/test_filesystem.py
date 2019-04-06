import shutil

from masonite.helpers.filesystem import make_directory

import unittest

class TestFilesystem(unittest.TestCase):

    def test_make_directory(self):
        dir_path = 'storage/uploads/test-dir'
        file_path = 'storage/uploads/test-dir/test.py'
        self.assertTrue(make_directory(dir_path))
        self.assertTrue(make_directory(file_path))
        with open(file_path, "w+"):
            pass
        self.assertFalse(make_directory(file_path))
        shutil.rmtree(dir_path)
