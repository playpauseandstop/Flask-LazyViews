from .utils import LazyView


class LazyViews(object):
    """
    Main instance for adding *lazy* views to Flask application or blueprint.
    """
    import_prefix = None
    instance = None

    def __init__(self, instance=None, import_prefix=None):
        """
        Initialize ``LazyViews`` instance.

        Basically it requires ``app`` or ``blueprint`` instance as first
        argument, but you could leave it empty and initialize it later with
        manually call ``init_app`` method. It could be helpful, if you want to
        configure ``LazyViews`` instance somewhere outside your ``app.py`` or
        for multiple applications.
        """
        if instance:
            self.init_app(instance, import_prefix)

    def add(self, url_rule, mixed, **options):
        """
        Add URL rule to Flask application or blueprint.

        ``mixed`` could be a real callable function, or a string Python path
        to callable view function. If ``mixed`` is a string, it would be
        wrapped with ``LazyView`` class.
        """
        assert self.instance, 'LazyViews instance is not properly initialized.'
        view = mixed if callable(mixed) else \
               LazyView(self.build_import_name(mixed))
        self.instance.add_url_rule(url_rule, view_func=view, **options)

    def add_error(self, code, mixed, **options):
        """
        Add error handler to Flask application or blueprint.
        """
        view = mixed if callable(mixed) else \
               LazyView(self.build_import_name(mixed))
        self.instance.errorhandler(404, **options)(view)

    def add_static(self, url_rule, **options):
        """
        Add URL rule for serving static files to Flask app or blueprint.
        """
        assert self.instance, 'LazyViews instance is not properly initialized.'
        self.add(url_rule, self.instance.send_static_file, **options)

    def build_import_name(self, import_name):
        """
        Prepend import prefix to import name if it earlier defined by user.
        """
        not_empty = lambda data: filter(lambda item: item, data)
        return '.'.join(not_empty((self.import_prefix, import_name)))

    def init_app(self, app, import_prefix=None):
        """
        Configure ``LazyViews`` instance, store ``app`` or ``blueprint``
        instance and import prefix if any.
        """
        if import_prefix and import_prefix.startswith('.'):
            import_name = \
                app.import_name if app.import_name != '__main__' else ''

            assert import_name, 'You should properly configure import name ' \
                                'for {0!r} instance or edit import prefix to '\
                                'not start with ".".'.\
                                format(mixed.__class__.__name__)

            import_prefix = import_name + import_prefix

        self.import_prefix = import_prefix
        self.instance = app

    def init_blueprint(self, blueprint, import_prefix=None):
        """
        Alias for init app function, cause basically there are no important
        differences between Flask app and blueprint if we only need to add URL
        rule.
        """
        return self.init_app(blueprint, import_prefix)
