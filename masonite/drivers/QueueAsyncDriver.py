import threading


class QueueAsyncDriver(object):
    """
    Queue Aysnc Driver
    """
    def __init__(self, Container):
        self.container = Container

    def push(self, *objects):
        for obj in objects:
            obj = self.container.resolve(obj)
            thread = threading.Thread(target=obj.dispatch(), args=(), kwargs={})
            thread.start()
