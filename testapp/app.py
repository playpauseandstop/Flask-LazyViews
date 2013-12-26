import os
import sys

from flask import Flask
from flask.ext.admin import Admin
from flask.ext.lazyviews import LazyViews
from flask.ext.script import Manager

from testapp.test.blueprint import blueprint as test_blueprint


def init_app():
    """
    Factory function to init Flask applictaion.
    """
    # Init Flask application and necessary extensions
    app = Flask(__name__)
    admin = Admin(app)
    manager = Manager(app)

    # Add url rules to application
    views = LazyViews(app)
    views.add('/', 'views.home')
    views.add('/error', 'views.server_error')
    views.add('/page/<int:page_id>', 'views.page', endpoint='flatpage')
    views.add('/page/<int:page_id>/cls', 'views.PageView', endpoint='flatpage_cls')
    views.add_admin('admin.AdminView',
                    endpoint='app_admin',
                    name='App View')
    views.add_error(404, 'views.error')
    views.add_error(500, 'views.error')
    views.add_static('/favicon.ico',
                     defaults={'filename': 'img/favicon.ico'},
                     endpoint='favicon')

    # Register test blueprint
    app.register_blueprint(test_blueprint, url_prefix='/test')

    return (app, admin, manager)


app, admin, manager = init_app()
