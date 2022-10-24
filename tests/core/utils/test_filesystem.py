from tests import TestCase

from src.masonite.utils.filesystem import get_extension


class TestFileUtils(TestCase):
    def test_get_extension(self):
        self.assertEqual(get_extension("log.txt"), ".txt")
        self.assertEqual(get_extension("archive.tar.gz"), ".tar.gz")
        self.assertEqual(get_extension("path/to/log.txt"), ".txt")
        self.assertEqual(get_extension("image.iso"), ".iso")
        self.assertEqual(get_extension("archlinux-2022.09.03-x86_64.iso"), ".iso")
        self.assertEqual(get_extension(".hidden_file"), "")
        self.assertEqual(get_extension("file-without-extension"), "")

        self.assertEqual(get_extension("log.txt", without_dot=True), "txt")
        self.assertEqual(get_extension("archive.tar.gz", without_dot=True), "tar.gz")
        self.assertEqual(get_extension(".hidden_file", without_dot=True), "")
        self.assertEqual(get_extension("file-without-extension", without_dot=True), "")
