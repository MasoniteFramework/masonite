import requests


class TestRequest:

    def __init__(self):
        self.request = None
        pass

    def get(self, route_url):
        from config import application
        self.request = requests.get(application.URL + route_url)
        return self

    def status_code(self, code):
        if self.request.status_code == code:
            return True

        return False

    def contains(self, content):
        if content in self.request.text:
            return True

        return False
