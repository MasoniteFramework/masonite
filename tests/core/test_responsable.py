from masonite.testing import TestCase


class TestResponsable(TestCase):

    def setUp(self):
        super().setUp()

    def test_mail_can_respond(self):
        self.assertTrue(self.get('/test/mail').contains('mail'))
