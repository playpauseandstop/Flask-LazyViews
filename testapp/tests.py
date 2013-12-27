import platform

try:
    from unittest2 import TestCase
except ImportError:
    from unittest import TestCase

from random import choice, randint
from string import ascii_letters as letters

from flask import Blueprint, Flask, url_for
from flask.ext.lazyviews import LazyViews
from werkzeug.utils import ImportStringError

from admin import AdminView
from app import init_app
from test.blueprint import init_blueprint
from views import PageView, page as page_view


class TestFlaskLazyViews(TestCase):

    TESTING = True

    def setUp(self):
        self.app, self._ctx = None, None

        self.app = self.create_app()
        self.client = self.app.test_client()

        self._ctx = self.app.test_request_context()
        self._ctx.push()

    def tearDown(self):
        if self._ctx is not None:
            self._ctx.pop()

        if self.app is not None:
            for attr in dir(self):
                if not attr.startswith('original_'):
                    continue
                name = attr.replace('original_', '')
                self.app.config[name] = getattr(self, attr)

    def assert200(self, response):
        self.assertStatus(response, 200)

    def assert404(self, response):
        self.assertStatus(response, 404)

    def assertStatus(self, response, status_code):
        self.assertEqual(response.status_code, status_code)

    def create_app(self):
        app, _, _ = init_app()

        for attr in dir(self):
            if not attr.isupper() or attr.startswith('_'):
                continue
            setattr(self, 'original_{0}'.format(attr), app.config.get(attr))
            app.config[attr] = getattr(self, attr)

        return app

    def get_blueprint_name(self):
        return 'test_{0}'.format(''.join([choice(letters) for i in range(4)]))

    def url(self, *args, **kwargs):
        return url_for(*args, **kwargs)

    def test_app(self):
        page = randint(1, 9999)

        home_url = self.url('home')
        page_url = self.url('flatpage', page_id=page)
        first_page_url = self.url('flatpage', page_id=1)
        second_page_url = self.url('flatpage_cls', page_id=2)
        admin_url = self.url('admin.index')
        favicon_url = self.url('favicon')

        response = self.client.get(home_url)
        self.assert200(response)
        self.assertIn('<h1>Flask-LazyViews test project</h1>', response.data)
        self.assertIn('<a href="{0}">'.format(first_page_url), response.data)
        self.assertIn('<a href="{0}">'.format(second_page_url), response.data)
        self.assertIn('<a href="{0}">'.format(admin_url), response.data)
        self.assertIn('<a href="{0}">'.format(favicon_url), response.data)

        response = self.client.get(page_url)
        self.assert200(response)
        self.assertIn('Page #{0:d}'.format(page), response.data)
        self.assertIn('<a href="{0}">'.format(home_url), response.data)

        response = self.client.get(admin_url)
        self.assert200(response)
        self.assertIn('App View', response.data)

        response = self.client.get(favicon_url)
        self.assert200(response)

    def test_blueprint(self):
        home_url = self.url('home')
        test_url = self.url('test.test')
        advanced_url = self.url('test.advanced')

        response = self.client.get(home_url)
        self.assert200(response)
        self.assertIn('<a href="{0}">'.format(test_url), response.data)
        self.assertIn('<a href="{0}?q='.format(advanced_url), response.data)

        response = self.client.get(test_url)
        self.assert200(response)
        self.assertIn('<h2>Test page</h2>', response.data)
        self.assertIn(
            '<a href="{0}">To advanced test page'.format(advanced_url),
            response.data
        )

        number = str(randint(1, 9999))

        response = self.client.get('{0}?q={1}'.format(advanced_url, number))
        self.assert200(response)
        self.assertIn('Advanced test page', response.data)
        self.assertIn('$REQUEST', response.data)
        self.assertIn(number, response.data)
        self.assertIn('Make POST request', response.data)

        text = ''.join([choice(letters) for i in range(16)])

        response = self.client.post(advanced_url, data={'text': text})
        self.assert200(response)
        self.assertIn(text, response.data)

    def test_custom_config_app(self):
        views = LazyViews(self.app, import_prefix='testapp.views')
        views.add('/default-page',
                  'page',
                  defaults={'page_id': 1},
                  endpoint='default_page')

        self.assertIn('default_page', self.app.view_functions)

        response = self.client.get(self.url('default_page'))
        self.assert200(response)
        self.assertIn('Page #1', response.data)

    def test_custom_config_blueprint(self):
        name = self.get_blueprint_name()
        blueprint = init_blueprint(name)

        views = LazyViews(blueprint, import_prefix=blueprint.import_name)
        views.add('/more-advanced',
                  'views.advanced',
                  endpoint='more_advanced',
                  methods=('GET', 'POST', 'PUT'))

        self.app.register_blueprint(blueprint, url_prefix='/test')
        self.assertIn('{0}.more_advanced'.format(name),
                      self.app.view_functions)

        response = self.client.put(self.url('{0}.more_advanced'.format(name)))
        self.assert200(response)
        self.assertIn('Advanced test page', response.data)

    def test_doc_and_repr(self):
        view_func = self.app.view_functions['home']
        hex_repr = '{0:x}'.format(id(view_func.view))

        if platform.system() == 'windows':
            view_repr = '0x0{0}'.format(hex_repr.upper())
        else:
            view_repr = '0x{0}'.format(hex_repr)

        self.assertEqual(view_func.__doc__, '\n    Home page.\n    ')
        self.assertEqual(repr(view_func),
                         '<function home at {0}>'.format(view_repr))

    def test_error_config_app(self):
        views = LazyViews(self.app, import_prefix='weird.path')
        views.add('/default-page',
                  'views.page',
                  defaults={'page_id': 1},
                  endpoint='default_page')

        self.assertIn('default_page', self.app.view_functions)
        self.assertRaises(ImportStringError,
                          self.client.get,
                          self.url('default_page'))

        views = LazyViews(self.app, import_prefix='testapp.views')
        views.add('/another-default-page',
                  'does_not_exist',
                  endpoint='another_default_page')

        self.assertIn('another_default_page', self.app.view_functions)

        self.assertRaises(ImportStringError,
                          self.client.get,
                          self.url('another_default_page'))

    def test_error_config_blueprint(self):
        name = self.get_blueprint_name()
        blueprint = init_blueprint(name)

        views = LazyViews(blueprint, import_prefix='weird.path')
        views.add('/more-advanced',
                  'views.advanced',
                  endpoint='more_advanced')

        self.app.register_blueprint(blueprint, url_prefix='/test')
        self.assertIn('{0}.more_advanced'.format(name),
                      self.app.view_functions)
        self.assertRaises(ImportStringError,
                          self.client.get,
                          self.url('{0}.more_advanced'.format(name)))

        name = self.get_blueprint_name()
        blueprint = init_blueprint(name)

        views = LazyViews(blueprint, blueprint.import_name)
        views.add('/more-more-advanced',
                  'views.does_not_exist',
                  endpoint='more_more_advanced')

        self.app.register_blueprint(blueprint, url_prefix='/test')
        self.assertIn('{0}.more_more_advanced'.format(name),
                      self.app.view_functions)
        self.assertRaises(ImportStringError,
                          self.client.get,
                          self.url('{0}.more_more_advanced'.format(name)))

    def test_error_handling(self):
        self.original_DEBUG = self.app.debug
        self.app.debug = False
        client = self.app.test_client()

        response = client.get('/does-not-exist.exe')
        self.assert404(response)
        self.assertIn('<h2>Error 404: Page Not Found</h2>', response.data)

    def test_init_app(self):
        self.app.blueprints.pop('app_admin')

        views = LazyViews()
        self.assertRaises(AssertionError,
                          views.add,
                          '/default-page',
                          'page',
                          defaults={'page_id': 1},
                          endpoint='default_page')
        self.assertRaises(AssertionError,
                          views.add_admin,
                          AdminView(name='Admin View'))
        self.assertRaises(AssertionError,
                          views.add_error,
                          404,
                          'error')
        self.assertRaises(AssertionError,
                          views.add_static,
                          '/more-static/<path:filename>',
                          endpoint='more_static')

        views.init_app(self.app)
        views.add('/default-page',
                  page_view,
                  defaults={'page_id': 1},
                  endpoint='default_page')
        views.add('/advanced-page',
                  PageView.as_view('page'),
                  defaults={'page_id': 2},
                  endpoint='advanced_page')
        views.add_admin(AdminView(name='Admin View'))
        views.add_static('/more-static/<path:filename>',
                         endpoint='more_static')

        self.assertIn('advanced_page', self.app.view_functions)
        self.assertIn('default_page', self.app.view_functions)
        self.assertIn('more_static', self.app.view_functions)

        response = self.client.get(self.url('default_page'))
        self.assert200(response)
        self.assertIn('Page #1', response.data)

        response = self.client.get(self.url('advanced_page'))
        self.assert200(response)
        self.assertIn('Page #2', response.data)

        response = self.client.get(self.url('admin.index'))
        self.assert200(response)
        self.assertIn('Admin View', response.data)

        favicon_url = self.url('more_static', filename='img/favicon.ico')
        response = self.client.get(favicon_url)
        self.assert200(response)

    def test_init_blueprint(self):
        views = LazyViews()
        self.assertRaises(AssertionError,
                          views.add,
                          '/more-advanced',
                          'views.advanced',
                          endpoint='more_advanced',
                          methods=('GET', 'POST', 'PUT'))

        name = self.get_blueprint_name()
        blueprint = init_blueprint(name)

        views.init_blueprint(blueprint, import_prefix=blueprint.import_name)
        views.add('/more-advanced',
                  'views.advanced',
                  endpoint='more_advanced',
                  methods=('GET', 'POST', 'PUT'))
        self.assertRaises(ValueError,
                          views.add_admin,
                          AdminView(name='Admin View'))

        # Don't forget to re-register blueprint
        self.app.register_blueprint(blueprint, url_prefix='/test')
        self.assertIn('{0}.more_advanced'.format(name),
                      self.app.view_functions)

        response = self.client.put(self.url('{0}.more_advanced'.format(name)))
        self.assert200(response)
        self.assertIn('Advanced test page', response.data)
