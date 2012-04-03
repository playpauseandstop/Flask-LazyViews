#!/usr/bin/env python

import unittest

# Simple manipulation to use ``unittest2`` if current Python version is
# less than 2.7
if not hasattr(unittest.TestCase, 'assertIn'):
    import unittest2 as unittest

from random import choice, randint
from string import letters

from flask import Blueprint, Flask, url_for
from flask.ext.lazyviews import LazyViews
from werkzeug.utils import ImportStringError

from app import app
from test import blueprint


class TestFlaskLazyViews(unittest.TestCase):

    def setUp(self):
        app.config['TESTING'] = True
        self.app = app.test_client()

    def tearDown(self):
        app.config['TESTING'] = False

    def url(self, *args, **kwargs):
        with app.test_request_context():
            return url_for(*args, **kwargs)

    def test_app(self):
        page = randint(1, 9999)

        home_url = self.url('home')
        page_url = self.url('flatpage', page_id=page)
        first_page_url = self.url('flatpage', page_id=1)

        response = self.app.get(home_url)
        self.assertEqual(response.status_code, 200)
        self.assertIn('<h1>Flask-LazyViews test project</h1>', response.data)
        self.assertIn('<a href="%s">' % first_page_url, response.data)

        response = self.app.get(page_url)
        self.assertEqual(response.status_code, 200)
        self.assertIn('Page #%d' % page, response.data)
        self.assertIn('<a href="%s">' % home_url, response.data)

    def test_blueprint(self):
        home_url = self.url('home')
        test_url = self.url('test.test')
        advanced_url = self.url('test.advanced')

        response = self.app.get(home_url)
        self.assertEqual(response.status_code, 200)
        self.assertIn('<a href="%s">' % test_url, response.data)
        self.assertIn('<a href="%s?q=' % advanced_url, response.data)

        response = self.app.get(test_url)
        self.assertEqual(response.status_code, 200)
        self.assertIn('<h2>Test page</h2>', response.data)
        self.assertIn(
            '<a href="%s">To advanced test page' % advanced_url,
            response.data
        )

        number = str(randint(1, 9999))

        response = self.app.get('%s?q=%s' % (advanced_url, number))
        self.assertEqual(response.status_code, 200)
        self.assertIn('Advanced test page', response.data)
        self.assertIn('$REQUEST', response.data)
        self.assertIn(number, response.data)
        self.assertIn('Make POST request', response.data)

        text = ''.join([choice(letters) for i in range(16)])

        response = self.app.post(advanced_url, data={'text': text})
        self.assertEqual(response.status_code, 200)
        self.assertIn(text, response.data)

    def test_custom_config_app(self):
        views = LazyViews(app, 'testapp.views')
        views.add('/default-page',
                  'page',
                  defaults={'page_id': 1},
                  endpoint='default_page')

        self.assertIn('default_page', app.view_functions)

        test_app = app.test_client()
        response = test_app.get(self.url('default_page'))
        self.assertEqual(response.status_code, 200)
        self.assertIn('Page #1', response.data)

    def test_custom_config_blueprint(self):
        views = LazyViews(blueprint, blueprint.import_name)
        views.add('/more-advanced',
                  'views.advanced',
                  endpoint='more_advanced',
                  methods=('GET', 'POST', 'PUT'))

        # Don't forget to re-register blueprint
        app.blueprints.pop('test')
        app.register_blueprint(blueprint, url_prefix='/test')

        self.assertIn('test.more_advanced', app.view_functions)

        test_app = app.test_client()
        response = test_app.put(self.url('test.more_advanced'))
        self.assertEqual(response.status_code, 200)
        self.assertIn('Advanced test page', response.data)

    def test_error_config_app(self):
        views = LazyViews(app, 'weird.path')
        views.add('/default-page',
                  'views.page',
                  defaults={'page_id': 1},
                  endpoint='default_page')

        self.assertIn('default_page', app.view_functions)

        test_app = app.test_client()
        self.assertRaises(ImportStringError,
                          test_app.get,
                          self.url('default_page'))

        views = LazyViews(app, 'testapp.views')
        views.add('/another-default-page',
                  'does_not_exist',
                  endpoint='another_default_page')

        self.assertIn('another_default_page', app.view_functions)

        test_app = app.test_client()
        self.assertRaises(ImportStringError,
                          test_app.get,
                          self.url('another_default_page'))

    def test_error_config_blueprint(self):
        views = LazyViews(blueprint, 'weird.path')
        views.add('/more-advanced',
                  'views.advanced',
                  endpoint='more_advanced')

        app.blueprints.pop('test')
        app.register_blueprint(blueprint, url_prefix='/test')

        self.assertIn('test.more_advanced', app.view_functions)

        test_app = app.test_client()
        self.assertRaises(ImportStringError,
                          test_app.get,
                          self.url('test.more_advanced'))

        views = LazyViews(blueprint, blueprint.import_name)
        views.add('/more-more-advanced',
                  'views.does_not_exist',
                  endpoint='more_more_advanced')

        app.blueprints.pop('test')
        app.register_blueprint(blueprint, url_prefix='/test')

        self.assertIn('test.more_more_advanced', app.view_functions)

        test_app = app.test_client()
        self.assertRaises(ImportStringError,
                          test_app.get,
                          self.url('test.more_more_advanced'))


if __name__ == '__main__':
    unittest.main()
