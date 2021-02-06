from src.masonite.testing import TestCase
from src.masonite.routes import Get


class TestResponsable(TestCase):
    def setUp(self):
        super().setUp()
        self.routes(only=[Get("/test/mail", "TestController@mail")])

    def test_mail_can_respond(self):
        self.assertTrue(self.get("/test/mail").contains("mail"))
