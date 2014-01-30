import os
import sys

from flask import Flask
from flask.ext.admin import Admin
from flask.ext.lazyviews import LazyViews
from flask.ext.sqlalchemy import SQLAlchemy

from testapp.test.blueprint import blueprint as test_blueprint


DUMMY = None


def init_app():
    """
    Factory function to init Flask applictaion.
    """
    # Init Flask application and necessary extensions
    app = Flask(__name__)
    app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite://'

    admin = Admin(app)
    db = SQLAlchemy(app)

    # Add url rules to application
    views = LazyViews(app)
    views.add('/', 'views.home')
    views.add('/db', 'views.database_page')
    views.add('/error', 'views.server_error')
    views.add('/page/<int:page_id>', 'views.page', endpoint='flatpage')
    views.add('/page/<int:page_id>/cls',
              'views.PageView',
              endpoint='flatpage_cls')
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

    return (app, admin, db)


(app, admin, db) = init_app()
