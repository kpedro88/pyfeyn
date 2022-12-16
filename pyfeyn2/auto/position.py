import copy

from pyfeyn2.interface.dot import dot_to_positions, feynman_to_dot


def scale_positions(fd, scale):
    """Scale the positions of the vertices and legs."""
    for v in fd.vertices:
        v.x *= scale
        v.y *= scale
    return fd


def feynman_adjust_points(feyndiag, size=5, delete_vertices=True):
    """Adjust the points of the vertices and legs using Dot language algorithms."""
    fd = feyndiag
    if delete_vertices:
        for v in fd.vertices:
            v.x = None
            v.y = None
    norm = size
    dot = feynman_to_dot(fd, resubstituteslash=False)
    positions = dot_to_positions(dot)
    mmax = 0
    for _, p in positions.items():
        if p[0] > mmax:
            mmax = p[0]
        if p[1] > mmax:
            mmax = p[1]
    for v in fd.vertices:
        if v.id in positions:
            v.x = positions[v.id][0] / mmax * norm
            v.y = positions[v.id][1] / mmax * norm
    for l in fd.legs:
        l.x = positions[l.id][0] / mmax * norm
        l.y = positions[l.id][1] / mmax * norm
    return fd
