
import inspect

class QueueRedisDriver(object):

    def __init__(self, QueueConfig, Container):
        self.config = QueueConfig
        self.container = Container

    def push(self, obj):
        obj.delay(self.container.make('Request'))
    
    def pop(self):
        pass
    
    def load_container(self, container):
        self.container = container
        return self
