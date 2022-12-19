from importlib.metadata import version as _version

from deprecation import deprecated as _deprecated

# TODO split in to own package
def withify(prefix="with_", sufix="", override=False):
    """Decorator to add with_ methods to a class."""

    def _withify(cls):
        inst = cls()
        for k in inst.__annotations__.keys():
            fun = prefix + k + sufix
            ok = k
            if override or not hasattr(cls, fun):
                def tmp(self, value,k=ok):
                    self.__dict__[k] = value
                    return self

                setattr(cls, fun, tmp)
        return cls

    return _withify


def deprecated(
    version=None, deprecated_in=None, removed_in=None, reason=None, details=None
):
    # merge details and reason
    if details is None:
        details = reason
    elif reason is not None:
        details = reason + " " + details

    # merge deprecated_in and version
    if version is None:
        version = deprecated_in

    # increment minor version
    if removed_in is None:
        removed_in = ".".join(
            version.split(".")[:-2]
            + [str(int(version.split(".")[-2]) + 1)]
            + [version.split(".")[-1]]
        )

    return _deprecated(
        deprecated_in=version,
        removed_in=removed_in,
        current_version=_version("pyfeyn2"),
        details=details,
    )
