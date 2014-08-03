from flask import Blueprint, Flask, url_for
from flask_lazyviews import LazyViews

from testapp.tests import TestCase, unittest


TEST_QUERY = 'test-query'


class TestBlueprint(TestCase):

    def test_complex(self):
        check_link = lambda response, url, label: self.assertContains(
            response, '<li><a href="{0}">{1}</a></li>'.format(url, label)
        )

        url = '?'.join((self.url('home'), 'q={0}'.format(TEST_QUERY)))
        response = self.client.get(url)
        self.assert200(response)
        self.assertContains(response, 'Blueprint views')

        check_link(response, self.url('testblueprint.test'), 'Test page')
        check_link(response,
                   '?'.join((self.url('testblueprint.advanced'),
                             'q={0}'.format(TEST_QUERY))),
                   'Advanced test page')
        check_link(response,
                   self.url('testblueprint.custom_error', code=403),
                   '403 page')
        check_link(response, self.url('testblueprint.gone'), '410 page')

    def test_error_handled(self):
        url = self.url('testblueprint.custom_error', code=403)
        response = self.client.get(url)
        self.assertStatus(response, 403)
        self.assertContains(response, 'Error 403: Forbidden')
        self.assertContains(
            response, 'This error page generated from Blueprint.'
        )

        response = self.client.get(self.url('testblueprint.gone'))
        self.assertStatus(response, 410)
        self.assertContains(response, 'Error 410: Gone')
        self.assertContains(
            response, 'This error page generated from Blueprint.'
        )

    def test_view_get(self):
        response = self.client.get(self.url('testblueprint.test'))
        self.assert200(response)
        self.assertContains(response, 'To advanced test page &raquo;')

    def test_view_post(self):
        url = self.url('testblueprint.advanced')
        response = self.client.post(url, {'q': TEST_QUERY})
        self.assert200(response)
        self.assertContains(response, TEST_QUERY)


class TestLazyViews(unittest.TestCase):

    def test_init_blueprint(self):
        app = Flask('test_testapp')
        views = LazyViews(app, 'testapp.views')
        views.add('/', 'home')

        views = LazyViews()
        blueprint = Blueprint('test_testblueprint',
                              'testapp.testblueprint',
                              template_folder='templates')
        self.assertEqual(len(app.view_functions), 2)

        views.init_blueprint(blueprint, 'testapp.testblueprint.views')
        views.add('/advanced', 'advanced', methods=('GET', 'POST'))
        views.add('/test', 'test')

        app.register_blueprint(blueprint, url_prefix='/test')
        self.assertEqual(len(app.view_functions), 4)

        with app.test_request_context():
            client = app.test_client()
            response = client.get(url_for('test_testblueprint.test'))
            self.assertEqual(response.status_code, 200)

    def test_init_blueprint_admin_error(self):
        blueprint = Blueprint('test_testblueprint',
                              'testapp.testblueprint',
                              template_folder='templates')
        views = LazyViews(blueprint, 'testapp')
        self.assertRaises(ValueError,
                          views.add_admin, 'admin.AdminView')
