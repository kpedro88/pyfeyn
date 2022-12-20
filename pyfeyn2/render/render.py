import abc
from typing import List

from pyfeyn2.feynmandiagram import FeynmanDiagram, Leg, Propagator, Vertex


class Render:
    def __init__(self, fd=None):
        self.fd = fd
        self.src = ""

    def set_feynman_diagram(self, fd):
        self.fd = fd

    def get_src(self):
        return self.src

    def set_src(self, src):
        self.src = src

    @abc.abstractmethod
    def render(
        self,
        file=None,
        show=True,
        resolution=100,
        width=None,
        height=None,
        clean_up=True,
    ):
        """
        Render the diagram.
        """
        return

    @classmethod
    def valid_styles(cls) -> List[str]:
        return []

    @classmethod
    def valid_types(cls) -> List[str]:
        return []

    @classmethod
    def valid_attributes(cls) -> List[str]:
        return ["type", "class"]

    @classmethod
    def valid_type(cls, typ: str) -> bool:
        return typ in cls.valid_types()

    @classmethod
    def valid_style(cls, style: str) -> bool:
        return style in cls.valid_styles()

    @classmethod
    def valid_attribute(cls, attr: str) -> bool:
        return attr in cls.valid_attributes()

    def demo_propagator(self, d, show=True, label=None):
        v1 = Vertex().with_xy(-2, -2)
        v2 = Vertex().with_xy(2, -2)

        fd = FeynmanDiagram().add(
            v1,
            v2,
            Propagator().connect(v1, v2).with_type(d).set_label(label).set_tension(0.0),
            Leg()
            .with_target(v1)
            .set_point(v1)
            .with_type("phantom")
            .with_incoming()
            .set_length(0.0),
            Leg()
            .with_target(v2)
            .set_point(v2)
            .with_type("phantom")
            .with_outgoing()
            .set_length(0.0),
        )

        self.set_feynman_diagram(fd)
        self.render(show=show)
