import copy


def auto_bend(ifd):
    """Automatically bend lines to avoid overlaps."""
    # TODO
    fd = copy.deepcopy(ifd)
    for pa in fd.propagators:
        for pb in fd.propagators:
            if pa.target is pb.target and pa.source is pb.source:
                pa.bend = True
                pb.bend = True
    return fd


def auto_tadpole(ifd):
    """Automatically bend lines to avoid overlaps."""
    fd = copy.deepcopy(ifd)
    for p in fd.propagators:
        if p.target is p.source:
            p.bend = True
    return fd
