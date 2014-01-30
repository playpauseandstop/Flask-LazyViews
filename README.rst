===============
Flask-LazyViews
===============

.. image:: https://secure.travis-ci.org/playpauseandstop/Flask-LazyViews.png?branch=master
    :target: https://travis-ci.org/playpauseandstop/Flask-LazyViews

.. image:: https://pypip.in/v/Flask-LazyViews/badge.png
    :target: https://pypi.python.org/pypi/Flask-LazyViews

Registering url routes for your `Flask <http://flask.pocoo.org/>`_ app or
blueprint in lazy way :)

**Based on original snippet from Flask documentation!**

Requirements
============

* `Python <http://www.python.org/>`_ 2.6, 2.7 or 3.3+
* `Flask`_ 0.8 or higher

Installation
============

::

    $ pip install Flask-LazyViews

License
=======

``Flask-LazyViews`` is licensed under the `BSD License
<https://github.com/playpauseandstop/Flask-LazyViews/blob/master/LICENSE>`_.

Usage
=====

For application
---------------

``project/app.py``

::

    from flask import Flask
    from flask.ext.lazyviews import LazyViews


    app = Flask(__name__)
    views = LazyViews(app)

    views.add('/', 'views.home')
    views.add('/page/<int:page>', 'views.page')

``project/views.py``

::

    from flask import render_template


    def home():
        return render_template('home.html')


    def page(page_id):
        page = get_page(page_id)
        return render_template('page.html', page=page)


For blueprint
-------------

``project/app.py``

::

    ...

    from project.test import blueprint as test_blueprint

    ...

    app.register_blueprint(test_blueprint, url_prefix='/test')


``project/test/__init__.py``

::

    from flask import Blueprint
    from flask.ext.lazyviews import LazyViews


    blueprint = Blueprint('test', __name__)
    views = LazyViews(blueprint, '.views')

    views.add('/', 'test')
    views.add('/advanced', 'advanced_test', methods=('GET', 'POST'))

``project/test/views.py``

::

    from flask import render_template, request


    def advanced_test():
        context = generate_context(request.form)
        return render_template('test/advanced.html', **context)


    def test():
        return render_template('test/test.html')

Explanations
============

The main point of ``Flask-LazyViews`` is simplifying process of adding views
to the app and blueprint using `lazy technique
<http://flask.pocoo.org/docs/patterns/lazyloading/>`_ from Flask
documentation.

Also the next goal is simplifying ``viewname`` definition. For most cases our
views functions placed in ``.views`` module of app or blueprint, so we don't
need to input full path to that module.

This especially useful for blueprints. Let see the example above, if we using
original snippet - we'll need to provide path to blueprint's views
module::

    add_url(blueprint, '/', 'test.views.test')

but with ``Flask-LazyViews`` we could to ignore ``test``.

From other side if your view functions placed in some other location or you
need to provide full path to its - you still could do this.

Also you could setup ``import_prefix`` like done in Django's ``patterns``::

    views = LazyViews(app, 'views')
    views.add('/', 'home')
    views.add('/page/<int:id>', 'page', methods=('GET', 'POST'))

Important
---------

Be careful with ``import_prefix`` value if you used ``__name__`` as Flask
application name or blueprint ``import_name``. Setting relative path could
cause server errors.

Other methods
=============

add_admin
---------

Add admin view if `Flask-Admin <http://pypi.python.org/pypi/Flask-Admin>`_
extension is added to Flask application.

.. note:: This method only works for Flask applications, not blueprints.

::

    admin = Admin(app)
    views = LazyViews(app, 'views')
    views.add_admin('PageAdmin', name='Page Admin')

add_error
---------

Add error handler to Flask application or blueprint, e.g.::

    views = LazyViews(app, 'views')
    views.add_error(404, 'error')
    views.add_error(500, server_error_view)

add_static
----------

Add custom URLs for serving static files. It useful when you want handle some
static files outside ``static_url``, e.g.::

    views = LazyViews(app)
    views.add_static('/favicon.ico', defaults={'filename': 'img/favicon.ico'})

Bugs, feature requests?
=======================

If you found some bug in ``Flask-LazyViews`` library, please, add new issue to
the project's `GitHub issues
<https://github.com/playpauseandstop/Flask-LazyViews/issues>`_.

ChangeLog
=========

0.5.1 (Jan 31, 2014)
--------------------

+ Fixes #3. Make ``LazyView`` proxy class lazy again. Fix circullar imports and
  working outside application context

0.5 (Dec 27, 2013)
------------------

+ Python 3 support (only for Flask 0.10+)
+ Flask 0.10+ support
+ Fixes #2. Access view function documentation and repr while loading views via
  strings

0.4 (Oct 28, 2012)
------------------

+ Add support of adding admin views to Flask applications via ``add_admin``
  method.
+ Configure Travis CI support.

0.3 (Oct 4, 2012)
-----------------

+ Implement ``add_error`` shortcut method for adding custom error handling for
  Flask application or blueprint.

0.2 (Sep 17, 2012)
------------------

+ Implement ``init_app`` and ``init_blueprint`` methods for configuring
  ``LazyViews`` instance outside main application module or for multiple
  applications.
+ Add ``add_static`` shortcut method for adding custom URL rules for serving
  static files.
+ Add ability to register real view functions with ``LazyViews`` instance.

0.1 (Apr 3, 2012)
-----------------

* Initial release.
