from flask import Blueprint
from flask.ext.lazyviews import LazyViews

from .admin import AdminView


blueprint = Blueprint('test', 'testapp.test', template_folder='templates')

views = LazyViews(blueprint, import_prefix='.views')
views.add('/', 'test')
views.add('/advanced', 'advanced', methods=('GET', 'POST'))
views.add_admin(AdminView(endpoint='blueprint_admin', name='Blueprint View'))
