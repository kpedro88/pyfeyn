import copy


def auto_label(objs, override=False):
    """Automatically label objects."""
    for p in objs:
        if p.label is None or override:
            p.label = "$" + p.particle.latex_name + "$"


def auto_label_propagators(ifd, override=False):
    """Automatically label propagators."""
    fd = copy.deepcopy(ifd)
    objs = fd.propagators
    for p in objs:
        if p.label is None or override:
            p.label = "$" + p.particle.latex_name + "$"
    return fd


def auto_label_legs(ifd, override=False):
    """Automatically label legs."""
    fd = copy.deepcopy(ifd)
    objs = fd.legs
    for p in objs:
        if p.particle is None or override:
            p.particle = "$" + p.particle.latex_name + "$"
    return fd
