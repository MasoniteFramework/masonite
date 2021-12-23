import sys
import traceback
import pkg_resources
import math
import pprint


class JsonHandler:
    def __init__(self, e=False, **kwargs):
        self.e = e
        self._contexts = {}
        self._integrations = {}

        self.type, self.value, self.tb = (
            exc_type,
            exc_value,
            exc_traceback,
        ) = sys.exc_info()
        self.traceback = traceback.TracebackException(
            self.type, self.value, self.tb, capture_locals=True
        )
        self.trace = self.create_trace()

        self.python_version = (
            str(sys.version_info[0])
            + "."
            + str(sys.version_info[1])
            + "."
            + str(sys.version_info[2])
        )
        self.default_encoding = sys.getdefaultencoding()
        self.file_system_encoding = sys.getfilesystemencoding()
        self.platform = sys.platform

        self.context(
            {
                "Environment & Details": {
                    "Python Version": self.python_version,
                    "Platform": self.platform,
                    "File System Encoding": self.file_system_encoding,
                    "Default Encoding": self.default_encoding,
                    "Argv": sys.argv,
                }
            }
        )

        installed_packages = pkg_resources.working_set
        packages = {}
        for i in installed_packages:
            packages.update({i.key: i.version})

        self.context({"Packages": packages})

    def any(self):
        return bool(self.e)

    def count(self):
        return len(self.trace)

    def message(self):
        return str(self.e)

    def exception(self):
        return self.e.__class__.__name__

    def namespace(self):
        return self.e.__class__.__module__ + "." + self.exception()

    def stacktrace(self):
        traceback = self.trace
        traceback.reverse()
        return traceback

    def context(self, context: dict):
        self._contexts.update(context)
        return self

    def integrate(self, integration):
        if isinstance(integration, dict):
            self._integrations.update(integration)
        else:
            self.integrate(
                {
                    integration.name: {
                        "content": integration.content(self),
                        "cls": integration,
                    }
                }
            )
        return self

    def get_contexts(self):
        return self._contexts

    def get_integrations(self):
        return self._integrations

    def create_trace(self):
        traceback = []
        for tb in self.traceback.stack:
            traceback.append(SimpleStackLine(tb, variables=tb.locals))

        return traceback

    def render(self):
        data = {
            "exception": self.exception(),
            "message": self.message(),
            "file": self.stacktrace()[0].file,
            "trace": [],
        }

        for trace in self.trace:
            data["trace"].append(
                {
                    "file": trace.file,
                    "line": trace.lineno,
                    "statement": trace.parent_statement,
                }
            )

        return data


class SimpleStackLine:
    def __init__(self, frame_summary, variables={}):
        self.file = frame_summary[0]

        # Cut off 30% of the string
        self.file_short = ".." + self.file[math.floor(len(self.file) * 0.30) :]
        self.lineno = frame_summary[1]
        self.offending_line = self.lineno
        self.parent_statement = frame_summary[2]
        self.statement = frame_summary[3]
        self.start_line = self.lineno - 5
        self.end_line = self.lineno + 5
        self.variables = variables
