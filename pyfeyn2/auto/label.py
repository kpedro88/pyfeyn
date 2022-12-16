import copy

def auto_label(objs):
    """Automatically label objects."""
    for p in objs:
        if p.label is None:
            p.label = "$" + p.particle.latex_name + "$"


def auto_label_propagators(ifd):
    """Automatically label propagators."""
    fd = copy.deepcopy(ifd)
    auto_label(fd.propagators)
    return fd
