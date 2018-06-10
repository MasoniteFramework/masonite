from masonite.environment import LoadEnvironment
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
            env_file.write('APP_DEBUG=production')
            env_file.close()

        LoadEnvironment()

        assert os.environ.get('TEST_PRODUCTION') == 'TEST'
        
    def test_environment_only_loads(self):
        LoadEnvironment(only='local')
        assert 'LOCAL' in os.environ
        assert os.environ.get('LOCAL') == 'TEST'
    

    

