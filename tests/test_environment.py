from masonite.environment import LoadEnvironment
import os

class TestEnvironment:

    def setup_method(self):
        LoadEnvironment()
    
    def test_environment_loaded_correctly(self):
        pass
    
    def test_environment_loads_custom_env(self):
        LoadEnvironment('local')
        assert 'LOCAL' in os.environ
        assert os.environ.get('LOCAL') == 'TEST'
    
    def test_environment_loads_custom_production_environment(self):
        assert os.environ.get('TEST_PRODUCTION') == 'TEST'
        
    

    

