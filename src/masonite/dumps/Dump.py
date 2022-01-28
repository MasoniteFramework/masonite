import time


class Dump:
    def __init__(self, objects, method, filename, line):
        self.objects = objects
        self.method = method
        self.filename = filename
        self.line = line
        self.timestamp = time.time()

    def serialize(self):
        objects = {name: str(obj) for name, obj in self.objects.items()}
        return {
            "objects": objects,
            "method": self.method,
            "filename": self.filename,
            "line": self.line,
            "timestamp": self.timestamp,
        }

    def __repr__(self):
        return self._format()

    def __str__(self):
        return self._format()

    def _format(self):
        return f"""{self.name} -> {self.filename}::{self.function}()::L{self.line}
        {self.objects}
        """
