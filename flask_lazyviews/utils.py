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
        self.__module__, self.__name__ = name.rsplit('.', 1)
        self.import_name = name
        self.args, self.kwargs = args, kwargs
        self.__doc__ = import_string(self.import_name).__doc__

    def __call__(self, *args, **kwargs):
        """
        Make real call to the view.
        """
        if self.args or self.kwargs:
            view = self.view(self.args, self.kwargs)
        else:
            view = self.view
        return view(*args, **kwargs)

    @cached_property
    def view(self):
        """
        Import view and cache it to current cls.
        """
        imported = import_string(self.import_name)

        if isinstance(imported, type) and issubclass(imported, View):
            view_name = self.import_name.lower().replace('view', '')
            return imported.as_view(view_name)

        return imported
