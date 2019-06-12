import os
import unittest

from masonite.testsuite import TestSuite
from masonite.managers import StorageManager
from masonite.drivers import StorageDiskDriver
from config import storage


class TestStorage(unittest.TestCase):

    def setUp(self):
        self.app = TestSuite().create_container().container
        self.app.bind('StorageDiskDriver', StorageDiskDriver)
        self.app.bind('StorageManager', StorageManager(self.app))
        self.app.bind('Storage', StorageManager(self.app).driver(storage.DRIVER))
        self.manager = self.app.make('Storage')

    def test_storage_creates_disk_driver(self):
        self.assertIsInstance(self.manager.driver('disk'), StorageDiskDriver)

    def test_storage_puts_file(self):
        driver = self.manager.driver('disk')
        driver.put('storage/some_file.txt', 'HI')
        self.assertEqual(driver.get('storage/some_file.txt'), 'HI')

    def test_storage_appends_file(self):
        driver = self.manager.driver('disk')
        driver.append('storage/some_file.txt', 'HI')
        self.assertEqual(driver.get('storage/some_file.txt'), 'HIHI')

    def test_storage_deletes_file(self):
        driver = self.manager.driver('disk')
        driver.put('storage/some_file.txt', 'HI')
        self.assertTrue(driver.delete('storage/some_file.txt'))

    def test_storage_file_exists(self):
        driver = self.manager.driver('disk')
        driver.put('storage/some_file.txt', 'HI')
        self.assertTrue(driver.exists('storage/some_file.txt'))
        self.assertTrue(driver.delete('storage/some_file.txt'))
        self.assertFalse(driver.exists('storage/some_file.txt'))

    def test_storage_file_gets_size(self):
        driver = self.manager.driver('disk')
        self.assertEqual(driver.size('storage/not_exists.txt'), 0)
        driver.put('storage/file.txt', 'HI')
        self.assertEqual(driver.size('storage/file.txt'), 2)
        self.assertTrue(driver.delete('storage/file.txt'))

    def test_storage_get_extension(self):
        driver = self.manager.driver('disk')
        driver.put('storage/file.txt', 'HI')
        self.assertEqual(driver.extension('storage/file.txt'), 'txt')

    def test_storage_upload(self):
        driver = self.manager.driver('disk')
        driver.upload(ImageMock())

    def test_storage_make_directory(self):
        driver = self.manager.driver('disk')
        self.assertTrue(driver.make_directory('storage/some_directory'))
        self.assertTrue(os.path.isdir('storage/some_directory'))

    def test_storage_delete_directory(self):
        driver = self.manager.driver('disk')
        self.assertTrue(driver.delete_directory('storage/some_directory'))
        self.assertFalse(os.path.isdir('storage/some_directory'))


class ImageMock():
    """
    Image test for emulate upload file
    """

    filename = 'test.jpg'

    @property
    def file(self):
        return self

    def read(self):
        return bytes('file read', 'utf-8')
