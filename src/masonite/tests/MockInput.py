class MockInput:
    def __init__(self, data):
        self.data = data

    def read(self, _):
        return self.data
