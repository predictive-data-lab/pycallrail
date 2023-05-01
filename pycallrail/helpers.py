import typing
import functools

# create a decorator to type check classes
def type_checked(cls) -> object:
    """
    A decorator to type check a class.
    """
    orig_init = cls.__init__
    def new_init(self, *args, **kwargs):
        for attr_name, attr_value in kwargs.items():
            attr_type = typing.get_type_hints(cls).get(attr_name)
            if attr_type and not isinstance(attr_value, attr_type):
                raise TypeError(f"{cls.__name__}.{attr_name} must be of type {attr_type}")
            setattr(self, attr_name, attr_value)
        orig_init(self, *args, **kwargs)
    cls.__init__ = new_init
    return cls