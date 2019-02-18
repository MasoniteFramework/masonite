from masonite.testsuite import TestSuite
from masonite.managers import StorageManager
from masonite.drivers import StorageDiskDriver
from config import storage

class TestStorage:

    def setup_method(self):
        self.app = TestSuite().create_container().container
        self.app.bind('StorageDiskDriver', StorageDiskDriver)
        self.app.bind('StorageManager', StorageManager(self.app))
        self.app.bind('Storage', StorageManager(self.app).driver(storage.DRIVER))
        self.manager = self.app.make('Storage')
    
    def test_storage_creates_disk_driver(self):
        assert isinstance(self.manager.driver('disk'), StorageDiskDriver)

    def test_storage_puts_file(self):
        driver = self.manager.driver('disk')
        driver.put('storage/some_file.txt', 'HI')
        driver.get('storage/some_file.txt') == 'HI'
        

    def test_storage_appends_file(self):
        driver = self.manager.driver('disk')
        driver.append('storage/some_file.txt', 'HI')
        driver.get('storage/some_file.txt') == 'HIHI'
        
    def test_storage_deletes_file(self):
        driver = self.manager.driver('disk')
        driver.put('storage/some_file.txt', 'HI')
        assert driver.delete('storage/some_file.txt')
        
    def test_storage_file_exists(self):
        driver = self.manager.driver('disk')
        driver.put('storage/some_file.txt', 'HI')
        assert driver.exists('storage/some_file.txt') is True
        assert driver.delete('storage/some_file.txt')
        assert driver.exists('storage/some_file.txt') is False
        
    def test_storage_file_gets_size(self):
        driver = self.manager.driver('disk')
        assert driver.size('storage/not_exists.txt') == 0
        driver.put('storage/file.txt', 'HI')
        assert driver.size('storage/file.txt') == 2
        assert driver.delete('storage/file.txt')

    def test_storage_get_extension(self):
        driver = self.manager.driver('disk')
        driver.put('storage/file.txt', 'HI')
        driver.extension('storage/file.txt') == 'txt'

    def test_storage_download(self):
        driver = self.manager.driver('disk')
        driver.put('storage/file.txt', 'HI')
        driver.download('storage/file.txt')

