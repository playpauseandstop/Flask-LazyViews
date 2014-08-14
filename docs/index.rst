===============
Flask-LazyViews
===============

Flask-LazyViews registers URL routes for `Flask <http://flask.pocoo.org/>`_
application or blueprint in lazy way. Ships with additional support of
registering admin views, error handlers, custom static files and rendering
Jinja2 templates.

* Based on original `snippet
  <http://flask.pocoo.org/docs/patterns/lazyloading/>`_ from Flask
  documentation
* Works on Python 2.6, 2.7 and 3.3+
* BSD licensed
* Latest documentation `on Read the Docs
  <http://flask-lazyviews.readthedocs.org/>`_
* Source, issues and pull requests `on GitHub
  <https://github.com/playpauseandstop/Flask-LazyViews>`_

Installation
============

Use `pip <http://pip.pypa.org>`_ to install Flask-LazyViews to your system or
virtual environment::

    $ pip install Flask-LazyViews

Otherwise you could download source dist from GitHub or PyPI and put
``flask_lazyviews`` directory somewhere to ``$PYTHONPATH``, but this way is not
recommended. Use pip for all good things.

Necessity
=========

The main purpose of registering lazy views instead of standard approach of
adding routes by decorating view functions with :meth:`flask.Flask.route`
decorator is avoiding "Circular Import" errors while organizing code in big
Flask project.

For example, when you have project with structure a like::

    project/
    + app.py
    + models.py
    + settings.py
    + views.py

and want to use ``@app.route`` decorator you obviously need to import ``app``
instance in views module, but to be sure that these view functions registered
as URL routes for your app you need make back import in app module. So you
actually should make inner import if using application factories or just
import views after global ``app`` instance already initialized and maybe
configured. This looks not very Pythonic.

In case of using lazy views you don't need import your views module when you
instantiate your application, all you need to import :class:`~.LazyViews`
instance, init it and add URL routes where view function is a string with valid
Python path. And yes adding view support all other route arguments as
``endpoint``, ``methods``, etc.

And yes, Flask-LazyViews supports :class:`flask.Blueprint` instances and have
extra features as registering error handlers, adding admin views, additional
static routes and rendering Jinja2 templates without actual view function.
Neat!

Usage
=====

To get started all you need to instaniate :class:`~.LazyViews` object after
configuring application::

    from flask import Flask
    from flask_lazyviews import LazyViews

    app = Flask(__name__)
    views = LazyViews(app)

Or blueprint::

    from flask import Blueprint

    blueprint = Blueprint('name', __name__)
    views = LazyViews(blueprint)

You can also pass the Flask application or blueprint object later, by calling
:meth:`~.LazyViews.init_app` or :meth:`~.LazyViews.init_blueprint`
respectfully::

    views = LazyViews()

    def create_app(name=None, **options):
        app = Flask(name or __name__)
        app.config.update(options)
        views.init_app(app, 'path.to.views')  # Full path to views module
        ...
        return app

Or::

    def create_blueprint(name, **options):
        blueprint = Blueprint(name, __name__, **options)
        views.init_blueprint(blueprint, '.views')  # Rel path to views module
        ...
        return blueprint

Now you ready to go and start using Flask-LazyViews extension.

Adding URL routes
-----------------

Main feature of Flask-LazyViews extension is adding lazy views (touche) to your
Flask application or blueprint.

In most cases lazy view is just a string with full Python path to view
function, like ``app.views.view``, where:

* ``app`` is name of Python package with your Flask application/blueprint
* ``views`` is name of views module
* ``view`` is name of view function

In other adding lazy views are equal to registering routes with
:meth:`flask.Flask.route` method and it supports all its keyword arguments
as ``methods``, ``endpoint``, etc.

To add lazy view to your application you need to call :meth:`~.LazyViews.add`
method::

    views.add('/', 'app.views.index')
    views.add('/comment/add', 'app.views.add_comment', methods=('GET', 'POST'))
    views.add('/page/<int:page_id>', 'app.views.page')

To simplify things and avoid repeating base path to your views, like
``app.views`` above, you could use ``import_prefix`` while initializing
:class:`~.LazyViews`::

    views = LazyViews(app, 'app.views')

After you don't need to repeat this prefix and could add views as::

    views.add('/', 'index')
    views.add('/comment/add', 'add_comment', methods=('GET', 'POST'))
    views.add('/page/<int:page_id>', 'page')

Registering error handlers
--------------------------

Flask application and blueprint has ability to register `error handlers
<http://flask.pocoo.org/docs/api/#flask.Flask.errorhandler>`_ to customize
processing HTTP errors. In most cases this handlers are view functions which
take ``error`` as first argument, so Flask-LazyViews allows you to add this
error handlers with :meth:`~.LazyViews.add_error` method::

    views.add_error(404, 'views.not_found')
    views.add_error(500, 'views.server_error')
    views.add_error(AssertionError, 'views.server_error')

Registering app error handler for Blueprint
-------------------------------------------

.. versionadded:: 0.6

In addition to registering error handlers for "own" URLs Flask blueprint has
ability to register custom `error handler for application
<http://flask.pocoo.org/docs/api/#flask.Blueprint.app_errorhandler>`_. To do
this in Flask-LazyViews, you need to pass ``app=True`` to
:meth:`~.LazyViews.add_error` method::

    views.add_error(401, 'views.not_authorized', app=True)
    views.add_error(ValueError, 'views.value_error', app=True)

Adding admin views
------------------

.. versionadded:: 0.4

`Flask-Admin <http://flask-admin.readthedocs.org/>`_ is one of the most popular
choices for making CRUD admin panel for Flask application. Flask-LazyViews has
support adding admin views in lazy way as done for plain routes. To do this you
need to call :meth:`~.LazyViews.add_admin` method::

    views.add_admin('admin.AdminView',
                    endpoint='app_admin',
                    name='Custom Admin Page')

.. note:: Keyword arguments passed to :meth:`~.LazyViews.add_admin` method
   would be transfer to instantiate admin view.

.. important:: Adding admin views only works for Flask application and when
   :class:`flask.ext.admin.base.Admin` extension already initialized before
   calling :meth:`~.LazyViews.add_admin` method.

Additional static routes
------------------------

.. versionchanged:: 0.6

Sometimes you need to create additional static route, for example to serve
``favicon.ico`` in root of your app. To do this you need to call
:meth:`~.LazyViews.add_static` method::

    views.add_static('/favicon.ico', 'icons/favicon.ico', endpoint='favicon')

You also should pass ``filename`` to static handler in ``defaults`` dict
(default approach prior to 0.6 version)::

    views.add_static('/favicon.ico',
                     defaults={'filename': 'icons/favicon.ico'},
                     endpoint='favicon')

Rendering Jinja2 templates without view functions
-------------------------------------------------

.. versionadded:: 0.6

Sometimes rendering template don't require any additional logic in view
function, but you still need to define it. To avoid this you could render
those templates directly with :meth:`~.LazyViews.add_template` method::

    views.add_template('/', 'index.html', endpoint='index')

You also can pass context to your templates, context could be a plain dict::

    views.add_template('/',
                       'index.html',
                       context={'DUMMY_CONSTANT': True},
                       endpoint='index')

Or any callable which returns dict::

    from flask import g

    def settings_context():
        return {'settings': get_user_settings(g.user)}

    views.add_template('/settings',
                       'settings.html',
                       context=settings_context,
                       endpoint='settings')

Example
=======

Flask-LazyViews ships with simple `test application
<https://github.com/playpauseandstop/Flask-LazyViews/tree/master/testapp>`_
which shows basic principles for using extension.

In case you want to run this application in your local environment you need
to bootstrap virtual environment for it and run server as::

    $ cd /path/to/Flask-LazyViews
    $ make -C testapp/ bootstrap
    $ make -C testapp/ server

When done, point your browser to ``http://127.0.0.1:8303/`` to see results.

.. note:: To bootstrap project `bootstrapper
   <http://warehouse.python.org/project/bootstrapper>`_ should be installed to
   your system as well as `GNU Make <http://www.gnu.org/software/make>`_.

API
===

.. module:: flask_lazyviews

.. autoclass:: LazyViews
   :members:
   :special-members:

.. module:: flask_lazyviews.utils

.. autoclass:: LazyView
   :members:
   :special-members:
   :exclude-members: __weakref__

Changelog
=========

0.6 (Aug 14, 2014)
----------------

+ Render Jinja2 templates for given URL rule via
  :meth:`~.LazyViews.add_template` method.
+ Register global app error handler from Blueprint by passing ``app=True`` to
  :meth:`~.LazyViews.add_error` method.
+ Keep ``import_prefix`` in :class:`~.LazyViews` instance.
+ Easify registering additional static routes by auto-adding ``filename`` to
  ``defaults`` dict.
+ Fixes #4. Fix registering multiple routes to same lazy view.
+ Move documentation from README to Read the Docs

0.5.1 (Jan 31, 2014)
--------------------

+ Fixes #3. Make :class:`~.LazyView` proxy class lazy again. Fix circullar
  imports and working outside application context.

0.5 (Dec 27, 2013)
------------------

+ Python 3 support (only for Flask 0.10+).
+ Flask 0.10+ support.
+ Fixes #2. Access view function documentation and repr while loading views via
  strings.

0.4 (Oct 28, 2012)
------------------

+ Add support of adding admin views to Flask applications via
  :meth:`~.LazyViews.add_admin` method.
+ Configure Travis CI support.

0.3 (Oct 4, 2012)
-----------------

+ Implement :meth:`~.LazyViews.add_error` shortcut method for adding custom
  error handling for Flask application or blueprint.

0.2 (Sep 17, 2012)
------------------

+ Implement :meth:`~.LazyViews.init_app` and :meth:`~.LazyViews.init_blueprint`
  methods for configuring :class:`~.LazyViews` instance outside main
  application module or for multiple applications.
+ Add :meth:`~.LazyViews.add_static` shortcut method for adding custom URL
  rules for serving static files.
+ Add ability to register real view functions with :class:`~.LazyViews`
  instance.

0.1 (Apr 3, 2012)
-----------------

* Initial release.
