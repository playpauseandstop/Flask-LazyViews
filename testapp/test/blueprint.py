from flask import Blueprint
from flask.ext.lazyviews import LazyViews

from .admin import AdminView


def init_blueprint(name=None):
    """
    Factory for initialize blueprint.
    """
    blueprint = Blueprint(name or 'test',
                          'testapp.test',
                          template_folder='templates')

    views = LazyViews(blueprint, import_prefix='.views')
    views.add('/', 'test')
    views.add('/advanced', 'advanced', methods=('GET', 'POST'))

    return blueprint


blueprint = init_blueprint()
