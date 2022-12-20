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

                def tmp(self, value, k=ok):
                    """Set `value` and return self."""
                    self.__dict__[k] = value
                    return self

                tmp.__doc__ = f"Set {k} to `value` and return self."
                setattr(cls, fun, tmp)
        return cls

    return _withify


@_deprecated(
    deprecated_in="2.0.7.1",
    removed_in="2.1",
    details="Use smpl.doc.deprecate instead? Better split smpl.doc into its own package.",
)
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
            [version.split(".")[0]] + [str(int(version.split(".")[1]) + 2)]
        )

    return _deprecated(
        deprecated_in=version,
        removed_in=removed_in,
        # current_version=_version("pyfeyn2"),
        details=details,
    )
