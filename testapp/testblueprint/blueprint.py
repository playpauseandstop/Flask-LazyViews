from flask import Blueprint
from flask.ext.lazyviews import LazyViews


def create_blueprint(name=None):
    """
    Factory for create blueprint.
    """
    # Create blueprint
    name = name or 'testblueprint'
    blueprint = Blueprint(name,
                          'testapp.{0}'.format(name),
                          template_folder='templates')

    # Initialize lazy views extension, register views and error handlers
    views = LazyViews(blueprint, import_prefix='.views')
    views.add('/', 'test')
    views.add('/advanced', 'advanced', methods=('GET', 'POST'))
    views.add('/error/<int:code>', 'custom_error')
    views.add('/gone', 'custom_error', defaults={'code': 410}, endpoint='gone')

    views.add_error(403, 'error')
    views.add_error(410, 'error', app=True)

    return blueprint
