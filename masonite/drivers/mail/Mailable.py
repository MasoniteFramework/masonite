class Mailable:

    _to = ''
    _from = ''
    _subject = ''

    def view(self, template, variables={}):
        self.template = template
        self.variables = variables
        return self

    def to(self, to):
        self._to = to
        return self

    def reply_to(self, reply_to):
        self._reply_to = reply_to
        return self

    def send_from(self, send_from):
        self._from = send_from
        return self

    def subject(self, subject):
        self._subject = subject
        return self
