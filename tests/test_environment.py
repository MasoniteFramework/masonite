
from masonite.environment import LoadEnvironment
from masonite import env

import os


class TestEnvironment:

    def test_environment_loaded_correctly(self):
        pass

    def test_environment_loads_custom_env(self):
        LoadEnvironment('local')
        assert 'LOCAL' in os.environ
        assert os.environ.get('LOCAL') == 'TEST'

    def test_environment_loads_custom_production_environment(self):
        env_path = os.path.join(os.getcwd(), '.env')
        if not os.path.exists(env_path):
            env_file = open(env_path, 'w')
            env_file.write('APP_ENV=production')
            env_file.close()

        LoadEnvironment()

        assert os.environ.get('TEST_PRODUCTION') == 'TEST'

    def test_environment_only_loads(self):
        LoadEnvironment(only='local')
        assert 'LOCAL' in os.environ
        assert os.environ.get('LOCAL') == 'TEST'

class TestEnv:

    def test_env_returns_numeric(self):
        os.environ["numeric"] = "1"
        assert env('numeric') == 1

    def test_env_returns_numeric_with_default(self):
        os.environ["numeric"] = "1"
        assert env('na', '1') == 1

    def test_env_returns_bool(self):
        os.environ["bool"] = "True"
        assert env('bool') == True
        os.environ["bool"] = "true"
        assert env('bool') == True
        os.environ["bool"] = "False"
        assert env('bool') == False
        os.environ["bool"] = "false"
        assert env('bool') == False

    def test_env_returns_default(self):
        os.environ["test"] = "1"
        assert env('na', 'default') == 'default'

