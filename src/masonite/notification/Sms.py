"""Sms Component"""


class Sms:

    _from = ""
    _to = ""
    _text = ""
    _client_ref = ""
    _type = "text"

    def __init__(self, text=""):
        self._text = text

    def from_(self, number):
        """Set the name or number the message should be sent from. Numbers should
        be specified in E.164 format. Details can be found here:
        https://developer.nexmo.com/messaging/sms/guides/custom-sender-id"""
        self._from = number
        return self

    def text(self, text):
        self._text = text
        return self

    def to(self, to):
        self._to = to
        return self

    def set_unicode(self):
        """Set message as unicode to handle unicode characters in text."""
        self._type = "unicode"
        return self

    def client_ref(self, client_ref):
        """Set your own client reference (up to 40 characters)."""
        if len(client_ref) > 40:
            raise ValueError("client_ref should have less then 40 characters.")
        self._client_ref = client_ref
        return self

    def build(self, *args, **kwargs):
        return self

    def get_options(self):
        base_dict = {
            "to": self._to,
            "from": self._from,
            "text": self._text,
            "type": self._type,
        }
        if self._client_ref:
            base_dict.update({"client-ref": self._client_ref})
        return base_dict
