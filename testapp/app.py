from flask import Flask
from flask.ext.admin import Admin
from flask.ext.lazyviews import LazyViews
from flask.ext.sqlalchemy import SQLAlchemy

from testblueprint.blueprint import create_blueprint


def create_app(name=None, **options):
    """
    Factory function to create Flask applictaion.
    """
    # Init Flask application and configure it
    app = Flask(name or __name__)
    app.config.update({
        'DEBUG': True,
        'SQLALCHEMY_DATABASE_URI': 'sqlite://',
    })
    app.config.update(options)

    # Setup necessary extensions
    Admin(app), SQLAlchemy(app)

    # Add lazy views to application
    views = LazyViews(app)
    views.add('/', 'views.home')
    views.add('/db', 'views.database_page', endpoint='dbpage')
    views.add('/error', 'views.server_error')
    views.add('/error/<int:code>', 'views.custom_error')
    views.add('/gone',
              'views.custom_error',
              defaults={'code': 410},
              endpoint='gone')
    views.add('/page/<int:page_id>', 'views.page', endpoint='flatpage')
    views.add('/page/<int:page_id>/cls',
              'views.PageView',
              endpoint='flatpage_cls')

    # Admin view
    views.add_admin('admin.AdminView',
                    endpoint='app_admin',
                    name='Custom Admin Page')

    # Error handlers
    views.add_error(404, 'views.error')
    views.add_error(500, 'views.error')

    # Custom static file serving
    views.add_static('/favicon.ico',
                     defaults={'filename': 'img/favicon.ico'},
                     endpoint='favicon')

    # Render templates with dict/callable context or without any context
    views.add_template('/template',
                       'template.html',
                       context={'text': 'Test Text'},
                       endpoint='template')
    views.add_template('/template/callable-context',
                       'template.html',
                       context=lambda: {'text': 'Callable Test Text'},
                       endpoint='template_callable_context')
    views.add_template('/template/no-context',
                       'template.html',
                       endpoint='template_no_context')

    # Create and register test blueprint
    app.register_blueprint(create_blueprint(), url_prefix='/test')

    return app


app = create_app()
