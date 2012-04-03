from werkzeug.utils import cached_property, import_string


__all__ = ('LazyView', )


class LazyView(object):
    """
    Import view function only when necessary.
    """
    def __init__(self, name):
        """
        Initialize ``LazyView`` instance for view that would be imported from
        ``name`` path.
        """
        self.__module__, self.__name__ = name.rsplit('.', 1)
        self.import_name = name

    def __call__(self, *args, **kwargs):
        """
        Make real call to the view.
        """
        return self.view(*args, **kwargs)

    @cached_property
    def view(self):
        """
        Import view and cache it to current cls.
        """
        return import_string(self.import_name)
