class PublishableResource:
    def __init__(self, key: str):
        self.key = key
        self.files: list = []

    def add(self, source: str, destination: str):
        self.files.append((source, destination))
        return self

    # def add(self, *resources):
    #     for source, destination in resources:
    #         self.sources.append(source)
    #         self.destinations.append(destination)
    #     return self
