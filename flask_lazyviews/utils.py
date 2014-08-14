"""
=====================
flask_lazyviews.utils
=====================

Proxy class for import view function from string.

"""

from flask.views import View
from werkzeug.utils import cached_property, import_string


__all__ = ('LazyView', )


class LazyView(object):
    """
    Import view function only when necessary.
    """
    def __init__(self, name, *args, **kwargs):
        """
        Initialize ``LazyView`` instance for view that would be imported from
        ``name`` path.
        """
        self.import_name = name
        self.args, self.kwargs = args, kwargs
        self.__module__, self.__name__ = name.rsplit('.', 1)

    def __call__(self, *args, **kwargs):
        """
        Make real call to the view.
        """
        if self.args or self.kwargs:
            view = self.view(self.args, self.kwargs)
        else:
            view = self.view
        return view(*args, **kwargs)

    def __eq__(self, other):
        """
        Check that two lazy view instances have equal import names.
        """
        try:
            return self.import_name == other.import_name
        except (AttributeError, ImportError):
            return False

    def __ne__(self, other):
        """
        Check that two lazy view instances have not equal import names.
        """
        return not self.__eq__(other)

    def __getattribute__(self, name):
        """
        Proxify documentation attribute from original view if it could be
        imported.
        """
        try:
            if name == '__doc__':
                return self.view.__doc__
        except ImportError:
            pass
        return super(LazyView, self).__getattribute__(name)

    def __repr__(self):
        """
        Show custom repr message if view function exists.
        """
        try:
            return repr(self.view)
        except ImportError:
            return super(LazyView, self).__repr__()

    @cached_property
    def view(self):
        """
        Import view from string and cache it to current class instance.
        """
        imported = import_string(self.import_name)

        if isinstance(imported, type) and issubclass(imported, View):
            view_name = self.import_name.lower().replace('view', '')
            return imported.as_view(view_name)

        return imported
