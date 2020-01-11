from src.masonite.middleware import CsrfMiddleware
from src.masonite.testing import TestCase
from src.masonite.routes import Get, Post


class TestCsrf(TestCase):

    def setUp(self):
        super().setUp()
        self.routes(only=[Get('/', 'ControllerTest@show').middleware('csrf'), Post('/test-route', 'ControllerTest@show').middleware('csrf')])
        csrf = CsrfMiddleware
        csrf.exempt = ['/*']
        self.withRouteMiddleware({'csrf': csrf})

    def test_middleware_sets_csrf_cookie(self):
        self.assertTrue(
            self.get('/').container.make('Request').get_cookie('csrf_token', decrypt=False)
        )
 
    def test_middleware_shares_view(self):
        self.assertIn('csrf_field', self.get('/').container.make('ViewClass')._shared)

    def test_middleware_does_not_need_safe_filter(self):
        self.assertNotIn('&lt;', self.container.make('ViewClass').render('csrf_field').rendered_template)

    def test_verify_token(self):
        token = self.get('/').container.make('Request').get_cookie('csrf_token', decrypt=False)
        self.assertTrue(self.container.make('Csrf').verify_csrf_token(token))

    def test_csrf_with_dashes(self):
        (self.withCsrf()
            .withoutHttpMiddleware()
            .post('/test-route'))

    def test_csrf_can_use_header(self):
        (self.withoutCsrf()
            .withHeaders({
                'X-CSRF-TOKEN': 'tok'
            })
            .post('/test-route'))
