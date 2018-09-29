from masonite.providers.StartResponseProvider import StartResponseProvider
from masonite.request import Request
from masonite.testsuite.TestSuite import generate_wsgi
from masonite.app import App
from masonite.exceptions import ResponseError
import pytest


class TestResponseProvider:

    def setup_method(self):
        self.app = App()
        self.provider = StartResponseProvider()

        self.app.bind('Response', None)
        self.app.bind('Request', Request(generate_wsgi()).load_app(self.app))
        self.app.bind('Headers', [])

        self.provider.app = self.app

    def test_response_boot_throws_response_exception(self):
        with pytest.raises(ResponseError):
            self.provider.boot(self.app.make('Request'))

    def test_response_encodes_header_response_to_bytes(self):
        encoded_bytes = bytes('test', 'utf-8')
        self.app.bind('Response', 'test')
        self.app.bind('StatusCode', '200 OK')

        self.provider.boot(self.app.make('Request'))

        assert self.app.make('Headers')[0] == ("Content-Length", str(len(encoded_bytes)))

    def test_redirect_sets_redirection_headers(self):
        self.app.make('Request').redirect_url = '/redirection'
        self.provider.boot(self.app.make('Request'))
        assert self.app.make('StatusCode') == '302 OK'
        assert ('Location', '/redirection') in self.app.make('Headers')
