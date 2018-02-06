from masonite.view import view

class StackTrace(object):

    def __init__(self, trace_obj):
        self.trace_obj = trace_obj

    def render(self):
        return view('traceback', {'traceback': self.trace_obj})
