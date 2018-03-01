class QueueRedisDriver(object):
    """
    Queue Redis driver
    """
    def __init__(self, QueueConfig, Container):
        self.config = QueueConfig
        self.container = Container

    def push(self, obj):
        obj.delay(self.container.make('Request'))

    def load_container(self, container):
        self.container = container
        return self
