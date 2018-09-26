import os
from masonite.packages import create_or_append_config, create_controller, append_api_routes, append_web_routes


PACKAGE_DIRECTORY = os.getcwd()


class TestPackage:

    def test_create_config(self):
        create_or_append_config(os.path.join(PACKAGE_DIRECTORY, 'testpackage/test-config.py'))
        assert os.path.exists('config/test-config.py')
        os.remove('config/test-config.py')

    def test_append_config(self):
        create_or_append_config(os.path.join(PACKAGE_DIRECTORY, 'testpackage/test-config.py'))
        create_or_append_config(os.path.join(PACKAGE_DIRECTORY, 'testpackage/test-config.py'))
        assert os.path.exists('config/test-config.py')
        with open(os.path.join(PACKAGE_DIRECTORY, 'config/test-config.py')) as f:
            assert 'ROUTES = []' in f.read()
        os.remove('config/test-config.py')

    def test_create_controller(self):
        create_controller(os.path.join(
            PACKAGE_DIRECTORY, 'testpackage/test-config.py'))
        assert os.path.exists('app/http/controllers/test-config.py')
        os.remove('app/http/controllers/test-config.py')
