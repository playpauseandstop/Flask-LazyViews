"""
=========================
flask_lazyviews.lazyviews
=========================

Class for adding lazy views to Flask application or blueprint.

"""

import sys

from functools import partial

from flask import render_template

from .utils import LazyView


__all__ = ('LazyViews', )


string_types = (str, unicode) if sys.version_info[0] < 3 else (str, )  # noqa


class LazyViews(object):
    """
    Main instance for adding *lazy* views to Flask application or blueprint.
    """
    __slots__ = ('import_prefix', 'instance')

    def __init__(self, instance=None, import_prefix=None):
        """
        Initialize :class:`LazyViews` instance.

        Basically it requires ``app`` or ``blueprint`` instance as first
        argument, but you could leave it empty and initialize it later with
        manually call :meth:`init_app` method. It could be helpful, if you want
        to configure :class:`LazyViews` instance somewhere outside your
        ``app.py`` or for multiple applications.
        """
        # Keep import prefix state to have ability reuse it later
        self.import_prefix = import_prefix
        self.instance = None

        if instance:
            self.init_app(instance, import_prefix)

    def add(self, url_rule, mixed, **options):
        """
        Add URL rule to Flask application or blueprint.

        ``mixed`` could be a real callable function, or a string Python path
        to callable view function. If ``mixed`` is a string, it would be
        wrapped into :class:`~flask_lazyviews.utils.LazyView` instance.
        """
        assert self.instance, 'LazyViews instance is not properly initialized.'
        options['view_func'] = self.get_view(mixed)
        self.instance.add_url_rule(url_rule, **options)

    def add_admin(self, mixed, *args, **kwargs):
        """
        Add admin view if `Flask-Admin <http://flask-admin.readthedocs.org/>`_
        extension added to application.

        .. important:: This method only works for Flask applications, not
           blueprints.
        """
        assert self.instance, 'LazyViews instance is not properly initialized.'

        if not hasattr(self.instance, 'blueprints'):
            raise ValueError('Cannot add admin view to blueprint.')

        app = self.instance

        if 'admin' not in app.extensions:
            raise ValueError('Looks like, Flask-Admin extension not added '
                             'to current application, {0!r}'.format(app))

        admin = app.extensions['admin']
        admin = admin[0] if isinstance(admin, list) else admin
        view = self.get_view(mixed)

        if isinstance(view, LazyView):
            view = view(*args, **kwargs)

        admin.add_view(view)

    def add_error(self, code_or_exception, mixed, app=False):
        """
        Add error handler to Flask application or blueprint.

        When passing ``app=True`` tries to register global app error handler
        for blueprint.
        """
        assert self.instance, 'LazyViews instance is not properly initialized.'

        app_handler = getattr(self.instance, 'app_errorhandler', None)
        handler = self.instance.errorhandler
        method = app_handler if app and app_handler else handler

        method(code_or_exception)(self.get_view(mixed))

    def add_static(self, url_rule, filename=None, **options):
        """
        Add URL rule for serving static files to Flask app or blueprint.
        """
        assert self.instance, 'LazyViews instance is not properly initialized.'
        if filename:
            options.setdefault('defaults', {}).update({'filename': filename})
        self.add(url_rule, self.instance.send_static_file, **options)

    def add_template(self, url_rule, template_name, **options):
        """
        Render template name with context for given URL rule.

        Context should be a plain dict or callable. If callable its result
        would be passed to :func:`flask.render_template` function.
        """
        assert self.instance, 'LazyViews instance is not properly initialized.'

        def renderer(template_name, mixed):
            context = mixed() if callable(mixed) else mixed or {}
            return partial(render_template, template_name, **context)

        view = renderer(template_name, options.pop('context', None))
        self.add(url_rule, view, **options)

    def build_import_name(self, import_name):
        """
        Prepend import prefix to import name if it earlier defined by user.
        """
        return '.'.join(filter(None, (self.import_prefix, import_name)))

    def get_view(self, mixed):
        """
        If ``mixed`` value is callable it's our view, else wrap it with
        :class:`flask_lazyviews.utils.LazyView` instance.
        """
        if callable(mixed) or not isinstance(mixed, string_types):
            return mixed
        return LazyView(self.build_import_name(mixed))

    def init_app(self, app, import_prefix=None):
        """
        Configure :class:`LazyViews` instance, store ``app`` or ``blueprint``
        instance and import prefix if any.
        """
        if import_prefix and import_prefix.startswith('.'):
            import_name = (app.import_name
                           if app.import_name != '__main__'
                           else '')

            assert import_name, ('You should properly configure import name '
                                 'for {0!r} instance or edit import prefix to '
                                 'not start with ".".'.format(app))

            import_prefix = import_name + import_prefix

        self.import_prefix = import_prefix or self.import_prefix
        self.instance = app

    def init_blueprint(self, blueprint, import_prefix=None):
        """
        Alias for init app function, cause basically there are no important
        differences between Flask app and blueprint if we only need to add URL
        rule.
        """
        return self.init_app(blueprint, import_prefix)
