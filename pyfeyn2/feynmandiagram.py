from dataclasses import MISSING, Field, dataclass, field
from typing import Any, List, Optional, Union

import cssutils
from xsdata.formats.converter import Converter, converter

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
        default=None, metadata={"xml_attribute": True, "type": "Attribute"}
    )

    def _sync_latexname(self):
        """Sync the latexname with the pdgid"""
        if self.pdgid is not None:
            self.latexname = get_name(self.pdgid)

    # def __post_init__(self):
    #    self._sync_latexname()

    def set_pdgid(self, pdgid):
        self.pdgid = pdgid
        self._sync_latexname()
        return self

    def set_type(self, typ):
        self.type = typ
        return self


id = 0


@dataclass
class Identifiable:
    id: Optional[str] = field(
        default=None, metadata={"xml_attribute": True, "type": "Attribute"}
    )

    def __post_init__(self):
        global id
        if self.id is None:
            # use some global counter to generate unique id
            self.id = self.__class__.__name__ + str(id)
            id = id + 1


@dataclass
class Labeled:
    label: Optional[str] = field(
        default=None, metadata={"xml_attribute": True, "type": "Attribute"}
    )

    def set_label(self, label):
        self.label = label
        return self


@dataclass
class Texted:
    text: Optional[str] = field(
        default="", metadata={"xml_attribute": True, "type": "Attribute"}
    )

    def set_text(self, text):
        self.text = text
        return self


@dataclass
class Point:
    x: Optional[float] = field(
        default=None, metadata={"xml_attribute": True, "type": "Attribute"}
    )
    y: Optional[float] = field(
        default=None, metadata={"xml_attribute": True, "type": "Attribute"}
    )
    z: Optional[float] = field(
        default=None, metadata={"xml_attribute": True, "type": "Attribute"}
    )

    def set_point(self, p):
        self.x = float(p.x)
        self.y = float(p.y)
        return self

    def set_xy(self, x, y):
        self.x = float(x)
        self.y = float(y)
        return self

    def set_xyz(self, x, y, z):
        self.x = float(x)
        self.y = float(y)
        self.z = float(z)
        return self


CSSString = cssutils.css.CSSStyleDeclaration


@dataclass
class Styled:
    style: CSSString = field(
        default_factory=lambda: cssutils.parseStyle(""),
        metadata={"name": "style", "xml_attribute": True, "type": "Attribute"},
    )

    def raw_style(self):
        return self.style.cssText.replace("\n", " ")

    def put_style(self, key, value):
        if self.style is not None:
            self.style.setProperty(key, value)
        return self


class CSSConverter(Converter):
    def deserialize(self, value: str, **kwargs) -> CSSString:
        return cssutils.parseStyle(value)

    def serialize(self, value: CSSString, **kwargs) -> str:
        return value.cssText.replace("\n", " ")


converter.register_converter(CSSString, CSSConverter())


@dataclass
class Bending:
    bend: Optional[float] = field(
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
class Vertex(Labeled, Point, Styled, Identifiable):
    pass


@dataclass
class Connector(Labeled, Bending, PDG, Styled, Identifiable):
    momentum: Optional[str] = field(
        default=None, metadata={"xml_attribute": True, "type": "Attribute"}
    )
    tension: Optional[float] = field(
        default=None, metadata={"xml_attribute": True, "type": "Attribute"}
    )
    length: Optional[float] = field(
        default=None, metadata={"xml_attribute": True, "type": "Attribute"}
    )

    def set_momentum(self, momentum):
        self.momentum = momentum
        return self

    def set_tension(self, tension):
        self.tension = tension
        return self

    def set_length(self, length):
        self.length = length
        return self

    pass


@dataclass
class Leg(Point, Targeting, Connector):
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
class Propagator(Line, Connector):
    pass


@dataclass
class Label(Point, Texted, Identifiable):
    pass


@dataclass
class FeynmanDiagram:
    class Meta:
        name = "diagram"

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
    labels: List[Label] = field(
        default_factory=list,
        metadata={"name": "label", "type": "Element", "namespace": ""},
    )

    def add(self, *all: List[Union[Propagator, Vertex, Leg, Label]]):
        for any in all:
            if isinstance(any, Propagator):
                self.propagators.append(any)
            elif isinstance(any, Vertex):
                self.vertices.append(any)
            elif isinstance(any, Leg):
                self.legs.append(any)
            elif isinstance(any, Label):
                self.labels.append(any)
            else:
                raise Exception("Unknown type: " + str(type(any)) + " " + str(any))
        return self

    def get_point(self, id):
        for v in self.vertices:
            if v.id == id:
                return v
        for l in self.legs:
            if l.id == id:
                return l
        return None


@dataclass
class Meta:
    class Meta:
        name = "meta"

    name: Optional[str] = field(
        default="", metadata={"xml_attribute": True, "type": "Attribute"}
    )
    value: Optional[str] = field(
        default="", metadata={"xml_attribute": True, "type": "Attribute"}
    )


aliasMeta = Meta


@dataclass
class Head:
    class Meta:
        name = "head"

    metas: List[aliasMeta] = field(
        default_factory=list,
        metadata={"name": "meta", "namespace": ""},
    )

    description: Optional[str] = field(
        default="", metadata={"xml_attribute": True, "type": "Element"}
    )


@dataclass
class FeynML:
    class Meta:
        name = "feynml"

    head: List[Head] = field(
        default_factory=list, metadata={"name": "head", "namespace": ""}
    )

    diagrams: List[FeynmanDiagram] = field(
        default_factory=list,
        metadata={"name": "diagram", "type": "Element", "namespace": ""},
    )

    def get_diagram(self, id):
        for d in self.diagrams:
            if d.id == id:
                return d
        return None
