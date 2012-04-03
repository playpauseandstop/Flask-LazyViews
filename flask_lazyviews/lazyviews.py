from .utils import LazyView


class LazyViews(object):
    """
    """
    def __init__(self, mixed, import_prefix=None):
        """
        """
        self._mixed = mixed

        if import_prefix and import_prefix.startswith('.'):
            import_name = \
                mixed.import_name if mixed.import_name != '__main__' else ''

            assert import_name, 'You should properly configure import name ' \
                                'for %r instance or edit import prefix to ' \
                                'not start with ".".' % \
                                mixed.__class__.__name__

            import_prefix = import_name + import_prefix

        self._import_prefix = import_prefix

    def add(self, url_rule, import_name, **options):
        """
        """
        view = LazyView(self.build_import_name(import_name))
        self._mixed.add_url_rule(url_rule, view_func=view, **options)

    def build_import_name(self, import_name):
        """
        """
        not_empty = lambda data: filter(lambda item: item, data)
        return '.'.join(not_empty((self._import_prefix or None, import_name)))
