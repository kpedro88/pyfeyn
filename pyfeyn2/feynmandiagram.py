from dataclasses import dataclass, field
from decimal import Decimal
from typing import List, Optional

from pyfeyn2.particles import get_name

# from pyfeyn2.propagator import Propagator
# from pyfeyn2.vertex import Vertex


@dataclass
class PDG:
    pdgid: Optional[int] = field(
        default=21, metadata={"xml_attribute": True, "type": "Attribute"}
    )
    type: Optional[str] = field(
        default="", metadata={"xml_attribute": True, "type": "Attribute"}
    )
    latexname: Optional[str] = field(
        default="", metadata={"xml_attribute": True, "type": "Attribute"}
    )

    def _sync_latexname(self):
        """Sync the latexname with the pdgid"""
        if self.pdgid is not None:
            self.latexname = get_name(self.pdgid)

    def __post_init__(self):
        self._sync_latexname()

    def set_pdgid(self, pdgid):
        self.pdgid = pdgid
        self._sync_latexname()
        return self

    def set_type(self, type):
        self.type = type
        return self


id = 0


@dataclass
class Identifiable:
    id: Optional[str] = field(
        default="", metadata={"xml_attribute": True, "type": "Attribute"}
    )

    def __post_init__(self):
        global id
        if self.id == "":
            # use some global counter to generate unique id
            self.id = self.__class__.__name__ + str(id)
            id = id + 1


@dataclass
class Labeled:
    label: Optional[str] = field(
        default="", metadata={"xml_attribute": True, "type": "Attribute"}
    )

    def set_label(self, label):
        self.label = label
        return self


@dataclass
class Point:
    x: Optional[Decimal] = field(
        default=None, metadata={"xml_attribute": True, "type": "Attribute"}
    )
    y: Optional[Decimal] = field(
        default=None, metadata={"xml_attribute": True, "type": "Attribute"}
    )
    z: Optional[Decimal] = field(
        default=None, metadata={"xml_attribute": True, "type": "Attribute"}
    )

    def set_xy(self, x, y):
        self.x = float(x)
        self.y = float(y)
        return self

    def set_xyz(self, x, y):
        self.x = float(x)
        self.y = float(y)
        self.z = float(z)
        return self


@dataclass
class Styled:
    style: Optional[str] = field(
        default=None, metadata={"xml_attribute": True, "type": "Attribute"}
    )


@dataclass
class Bending:
    bend: Optional[str] = field(
        default=None, metadata={"xml_attribute": True, "type": "Attribute"}
    )


@dataclass
class Targeting:
    target: Optional[str] = field(
        default="", metadata={"xml_attribute": True, "type": "Attribute"}
    )

    def set_target(self, target):
        self.target = target.id
        return self


@dataclass
class Sourcing:
    source: Optional[str] = field(
        default="", metadata={"xml_attribute": True, "type": "Attribute"}
    )

    def set_source(self, source):
        self.source = source.id
        return self


@dataclass
class Line(Targeting, Sourcing):
    def connect(self, source, target):
        self.set_source(source)
        self.set_target(target)
        return self


@dataclass
class Vertex(Labeled, Styled, Point, Identifiable):
    pass


@dataclass
class Leg(Labeled, Styled, PDG, Bending, Point, Targeting, Identifiable):
    sense: str = field(
        default="", metadata={"xml_attribute": True, "type": "Attribute"}
    )

    def set_incoming(self):
        self.sense = "incoming"
        return self

    def set_outgoing(self):
        self.sense = "outgoing"
        return self


@dataclass
class Propagator(Labeled, Styled, PDG, Bending, Line, Identifiable):
    pass


@dataclass
class FeynmanDiagram:
    class Meta:
        name = "feynmandiagram"

    propagators: List[Propagator] = field(
        default_factory=list,
        metadata={"name": "propagator", "type": "Element", "namespace": ""},
    )
    vertices: List[Vertex] = field(
        default_factory=list,
        metadata={"name": "vertex", "type": "Element", "namespace": ""},
    )
    legs: List[Leg] = field(
        default_factory=list,
        metadata={"name": "leg", "type": "Element", "namespace": ""},
    )

    def get_point(self, id):
        for v in self.vertices:
            if v.id == id:
                return v
        for l in self.legs:
            if l.id == id:
                return l
        return None
