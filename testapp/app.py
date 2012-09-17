#!/usr/bin/env python

import os
import sys

from flask import Flask
from flask.ext.lazyviews import LazyViews

from testapp.test import blueprint as test_blueprint


# Init Flask application
app = Flask(__name__)

# Add url routes to application
views = LazyViews(app)
views.add('/', 'views.home')
views.add('/page/<int:page_id>', 'views.page', endpoint='flatpage')
views.add_static('/favicon.ico',
                 defaults={'filename': 'img/favicon.ico'},
                 endpoint='favicon')

# Register test blueprint
app.register_blueprint(test_blueprint, url_prefix='/test')


if __name__ == '__main__':
    host = '0.0.0.0'
    port = 5000

    if len(sys.argv) == 2:
        mixed = sys.argv[1]

        try:
            host, port = mixed.split(':')
        except ValueError:
            port = mixed
    elif len(sys.argv) == 3:
        host, port = sys.argv[1:]

    try:
        port = int(port)
    except (TypeError, ValueError):
        print >> sys.stderr, 'Please, use proper digit value to the ' \
                             '``port`` argument.\nCannot convert {0!r} to ' \
                             'integer.'.format(port)
        sys.exit(1)

    app.debug = bool(int(os.environ.get('DEBUG', 1)))
    app.run(host=host, port=port)
