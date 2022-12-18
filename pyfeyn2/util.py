# TODO split in to own package
def withify(prefix="with_", sufix="", override=False):
    """Decorator to add with_ methods to a class."""

    def _withify(cls):
        inst = cls()
        for k in inst.____annotations__.keys():
            fun = prefix + k + sufix
            if override or not hasattr(cls, fun):

                def tmp(self, value):
                    self.__dict__[k] = value
                    return self

                setattr(cls, fun, tmp)
        return cls

    return _withify
