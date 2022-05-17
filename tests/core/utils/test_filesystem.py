from tests import TestCase

from src.masonite.utils.filesystem import get_extension


class TestFileUtils(TestCase):
    def test_get_extension(self):
        self.assertEqual(get_extension("log.txt"), ".txt")
        self.assertEqual(get_extension("archive.tar.gz"), ".tar.gz")
        self.assertEqual(get_extension("path/to/log.txt"), ".txt")

        self.assertEqual(get_extension("log.txt", without_dot=True), "txt")
        self.assertEqual(get_extension("archive.tar.gz", without_dot=True), "tar.gz")
