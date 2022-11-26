from dataclasses import dataclass, field
from decimal import Decimal
from typing import List, Optional

# from pyfeyn2.propagator import Propagator
# from pyfeyn2.vertex import Vertex


@dataclass
class PDG:
    pdgid: Optional[int] = field(
        default=0, metadata={"xml_attribute": True, "type": "Attribute"}
    )
    type: Optional[str] = field(
        default="", metadata={"xml_attribute": True, "type": "Attribute"}
    )

    def set_pdgid(self, pdgid):
        self.pdgid = pdgid
        # TODO get type from pdgid
        return self

    def set_type(self, type):
        self.type = type
        return self


@dataclass
class Identifiable:
    id: Optional[str] = field(
        default="", metadata={"xml_attribute": True, "type": "Attribute"}
    )


@dataclass
class Labeled:
    label: Optional[str] = field(
        default="", metadata={"xml_attribute": True, "type": "Attribute"}
    )


@dataclass
class Point:
    x: Optional[Decimal] = field(
        default=0.0, metadata={"xml_attribute": True, "type": "Attribute"}
    )
    y: Optional[Decimal] = field(
        default=0.0, metadata={"xml_attribute": True, "type": "Attribute"}
    )
    z: Optional[Decimal] = field(
        default=0.0, metadata={"xml_attribute": True, "type": "Attribute"}
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
class Vertex(Labeled, Point, Identifiable):
    pass


@dataclass
class Leg(Labeled, PDG, Point, Targeting, Identifiable):
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
class Propagator(Labeled, PDG, Line, Identifiable):
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
