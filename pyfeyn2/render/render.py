import io

import PIL
from IPython.display import display
from matplotlib import pyplot as plt

from pyfeyn2.feynmandiagram import FeynmanDiagram, Leg, Vertex


class Render:
    def __init__(self, fd):
        self.fd = fd
        self.src = ""

    def set_feynman_diagram(self, fd):
        self.fd = fd

    def get_src(self):
        return self.src

    def render(self, file=None):
        pass

    def valid_style(self, style: str) -> bool:
        return False

    def valid_type(self, typ: str) -> bool:
        return False

    def valid_attribute(self, attr: str) -> bool:
        if attr == "id":
            return True
        if attr == "sense":
            return True
        if attr == "target":
            return True
        if attr == "source":
            return True
        if attr == "type":
            return True
        return False

    def demo_propagator(self, d, show=True):
        fd = FeynmanDiagram()
        v0 = Vertex("v0").set_xy(0, 0)
        v1 = Vertex("v1").set_xy(2, 2)
        v2 = Vertex("v2").set_xy(-2, 2)
        v3 = Vertex("v3").set_xy(2, -2)
        v4 = Vertex("v4").set_xy(-2, -2)
        l1 = Leg("l1").set_target(v0).set_type(d).set_incoming().set_xy(-2, 0)
        l2 = Leg("l2").set_target(v0).set_type(d).set_outgoing().set_xy(2, 0)
        # fd.propagators.append(p1)
        fd.vertices.extend([v0, v1, v2, v3, v4])
        fd.legs.extend([l1, l2])
        self.set_feynman_diagram(fd)
        self.render(show=show)
