from flask import Blueprint
from flask.ext.lazyviews import LazyViews


blueprint = Blueprint('test', 'testapp.test', template_folder='templates')

views = LazyViews(blueprint, '.views')
views.add('/', 'test')
views.add('/advanced', 'advanced', methods=('GET', 'POST'))
