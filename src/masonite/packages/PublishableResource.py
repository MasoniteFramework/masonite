class PublishableResource:
    def __init__(self, key):
        self.key = key
        self.files = []

    def add(self, source, destination):
        self.files.append((source, destination))
        return self

    # def add(self, *resources):
    #     for source, destination in resources:
    #         self.sources.append(source)
    #         self.destinations.append(destination)
    #     return self
