import os
class Request:

    def __init__(self):
        self.method = os.environ['REQUEST_METHOD']
        self.path = os.environ['URI_PATH']