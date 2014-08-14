import platform

try:
    import unittest2 as unittest
except ImportError:
    import unittest

from flask import Flask, url_for
from flask_lazyviews import LazyViews
from flask_lazyviews.utils import LazyView
from jinja2.filters import escape

from testapp.app import create_app
from testapp.views import page as page_view


strong = lambda text: '<strong>{0}</strong>'.format(escape(text))


def create_test_app(name=None, **options):
    options.update({'DEBUG': True, 'TESTING': True})

    app = Flask(name or 'testapp')
    app.config.update(options)

    return app


class TestCase(unittest.TestCase):

    def setUp(self):
        self.app, self._ctx = None, None

        self.app = self.create_app()
        self.client = self.app.test_client()

        self._ctx = self.app.test_request_context()
        self._ctx.push()

    def tearDown(self):
        if self._ctx is not None:
            self._ctx.pop()

    def assert200(self, response):
        self.assertStatus(response, 200)

    def assert404(self, response):
        self.assertStatus(response, 404)

    def assertContains(self, response, text):
        self._prepare_response(response)
        self.assertIn(text, response.decoded)

    def assertNotContains(self, response, text):
        self._prepare_response(response)
        self.assertNotIn(text, response.decoded)

    def assertStatus(self, response, status_code):
        self.assertEqual(response.status_code, status_code)

    def create_app(self, **kwargs):
        return create_app(TESTING=True, **kwargs)

    def url(self, *args, **kwargs):
        return url_for(*args, **kwargs)

    def _prepare_response(self, response):
        if not hasattr(response, 'decoded'):
            response.decoded = response.data.decode(response.charset)


class TestApplication(TestCase):

    def test_admin(self):
        response = self.client.get(self.url('app_admin.index'))
        self.assert200(response)
        self.assertContains(
            response,
            'Custom Admin page added via <code>Flask-LazyViews</code>.'
        )

    def test_complex(self):
        check_link = lambda response, url, label: self.assertContains(
            response, '<li><a href="{0}">{1}</a></li>'.format(url, label)
        )

        response = self.client.get(self.url('home'))
        self.assert200(response)
        self.assertContains(response, 'Home page')
        self.assertContains(response, 'Application views')

        check_link(response, self.url('flatpage', page_id=1), 'Page #1')
        check_link(response, self.url('flatpage_cls', page_id=2), 'Page #2')
        check_link(response, self.url('dbpage'), 'Database page')
        check_link(response, self.url('app_admin.index'), 'Custom Admin page')
        check_link(response, self.url('favicon'), 'Favicon')
        check_link(response, self.url('old_favicon'), 'Old Favicon')
        check_link(response, self.url('custom_error', code=403), '403 page')
        check_link(response, '/does-not-exist.exe', '404 page')
        check_link(response, self.url('gone'), '410 page')
        check_link(response, self.url('server_error'), '500 page')
        check_link(response, self.url('template'), 'Template page')
        check_link(response,
                   self.url('template_callable_context'),
                   'Template page with callable context')
        check_link(response,
                   self.url('template_no_context'),
                   'Template page without context')

    def test_error_default(self):
        response = self.client.get('/error/default')
        self.assertStatus(response, 400)

    def test_error_handled(self):
        response = self.client.get('/does-not-exist.exe')
        self.assert404(response)
        self.assertContains(response, 'Error 404: Page Not Found')
        self.assertNotContains(
            response,
            'This error page generated from Blueprint.'
        )

    def test_error_handled_from_blueprint(self):
        response = self.client.get(self.url('gone'))
        self.assertStatus(response, 410)
        self.assertContains(response, 'Error 410: Gone')
        self.assertContains(
            response, 'This error page generated from Blueprint.'
        )

    def test_error_not_handled(self):
        response = self.client.get(self.url('custom_error', code=403))
        self.assertStatus(response, 403)
        self.assertNotContains(response, 'Error 403: Forbidden')

    def test_error_server_error(self):
        self.assertRaises(AssertionError,
                          self.client.get,
                          self.url('server_error'))

        # Dummy request to home page to avoid "Popped wrong request context."
        # error on teardown
        self.assert200(self.client.get(self.url('home')))

    def test_static(self):
        response = self.client.get(self.url('favicon'))
        self.assert200(response)
        self.assertEqual(response.mimetype, 'image/x-icon')

    def test_template(self):
        response = self.client.get(self.url('template'))
        self.assert200(response)
        self.assertContains(response, strong("'Test Text'"))

    def test_template_callable_context(self):
        response = self.client.get(self.url('template_callable_context'))
        self.assert200(response)
        self.assertContains(response, strong("'Callable Test Text'"))

    def test_template_no_context(self):
        response = self.client.get(self.url('template_no_context'))
        self.assert200(response)
        self.assertContains(response, strong('Undefined'))

    def test_view_class(self):
        response = self.client.get(self.url('flatpage_cls', page_id=2))
        self.assert200(response)
        self.assertContains(response, 'Page #2')
        self.assertContains(response, 'Dummy page content ;)')

    def test_view_function(self):
        response = self.client.get(self.url('flatpage', page_id=1))
        self.assert200(response)
        self.assertContains(response, 'Page #1')
        self.assertContains(response, 'Dummy page content ;)')

    def test_view_function_and_database(self):
        response = self.client.get(self.url('dbpage'))
        self.assert200(response)
        self.assertContains(response, 'Page #')
        self.assertContains(response, 'Dummy content.')


class TestLazyView(unittest.TestCase):

    def test_doc_and_repr(self):
        lazy = LazyView('testapp.views.home')
        lazy_repr = repr(lazy)

        hex_repr = '{0:x}'.format(id(lazy.view))
        if platform.system() == 'Windows':
            hex_repr = hex_repr.upper()

        self.assertEqual(lazy.__doc__, '\n    Home page.\n    ')
        self.assertTrue(lazy_repr.startswith('<function home at 0x'))
        self.assertTrue(lazy_repr.endswith('{0}>'.format(hex_repr)))

    def test_eq(self):
        lazy = LazyView('testapp.views.page')
        view = LazyView('testapp.views.page')
        self.assertNotEqual(id(lazy), id(view))
        self.assertEqual(lazy, view)
        self.assertNotEqual(lazy, page_view)

    def test_wrong_view(self):
        lazy = LazyView('testapp.views.page')
        wrong = LazyView('wrong.views.page')

        self.assertNotEqual(lazy, wrong)
        self.assertEqual(
            wrong.__doc__,
            '\n    Import view function only when necessary.\n    '
        )
        self.assertTrue(repr(wrong).startswith(
            '<flask_lazyviews.utils.LazyView object at 0x'
        ))


class TestLazyViews(unittest.TestCase):

    def test_init_app(self):
        app = create_test_app()
        self.assertEqual(len(app.view_functions), 1)

        views = LazyViews(app, 'testapp')
        views.add_template('/', 'home.html', endpoint='home')
        views.add('/page/<int:page_id>', 'views.page')
        self.assertEqual(len(app.view_functions), 3)

        self.assertRaises(ValueError,
                          views.add_admin, 'admin.AdminView')

        with app.test_request_context():
            response = app.test_client().get(url_for('page', page_id=1))
            self.assertEqual(response.status_code, 200)

    def test_init_app_errors(self):
        views = LazyViews()

        self.assertRaises(AssertionError,
                          views.add, '/page/<int:page_id>', 'page')
        self.assertRaises(AssertionError,
                          views.add_admin, 'admin.AdminView')
        self.assertRaises(AssertionError,
                          views.add_error, 403, 'error')
        self.assertRaises(AssertionError,
                          views.add_static,
                          '/favicon.ico',
                          defaults={'filename': 'img/favicon.ico'},
                          endpoint='favicon')
        self.assertRaises(AssertionError,
                          views.add_template,
                          '/template', 'template.html', endpoint='template')
