import logging
from dataclasses import dataclass, field
from typing import List, Optional, Union

import cssutils
from particle import Particle
from xsdata.formats.converter import Converter, converter

from pyfeyn2.particles import get_either_particle, get_name

# We don't want to see the cssutils warnings, since we have custom properties
cssutils.log.setLevel(logging.CRITICAL)


# from pyfeyn2.propagator import Propagator
# from pyfeyn2.vertex import Vertex

# Global counter for unique ids
global_id = 0


@dataclass
class Identifiable:
    id: Optional[str] = field(default=None, metadata={"name": "id", "namespace": ""})
    id2: Optional[str] = field(default=None, metadata={"name": "id2", "namespace": ""})

    def __post_init__(self):
        global global_id
        if self.id is None:
            # use some global counter to generate unique id
            self.id = self.__class__.__name__ + str(global_id)
            global_id = global_id + 1


@dataclass
class PDG(Identifiable):
    pdgid: Optional[int] = field(default=None, metadata={})
    name: Optional[str] = field(default=None, metadata={})
    type: Optional[str] = field(
        default=None, metadata={"xml_attribute": True, "type": "Attribute"}
    )

    # TODO check SUSY
    particle: Optional[Particle] = field(default=None, metadata={"type": "Ignore"})

    def _sync(self):
        """Sync the particle with the pdgid, name etc."""
        if self.pdgid is not None:
            self.particle = Particle.from_pdgid(self.pdgid)
            self.name = self.particle.name
        elif self.name is not None:
            self.particle = get_either_particle(
                programmatic_name=self.name,
                name=self.name,
                evtgen_name=self.name,
                html_name=self.name,
                latex_name=self.name,
            )
            if self.particle is None:
                raise ValueError(f"Particle {self.name} not found")
            self.pdgid = self.particle.pdgid

        if self.pdgid is not None and self.type is None:
            # TODO infere type from pdgid
            if self.pdgid in range(1, 7):
                self.type = "fermion"
            elif self.pdgid == 22:
                self.type = "photon"
            elif self.pdgid == 21:
                self.type = "gluon"
            elif self.pdgid in range(11, 19):
                self.type = "fermion"
            elif abs(self.pdgid) == 24:
                self.type = "boson"
            elif self.pdgid == 23:
                self.type = "boson"
            elif self.pdgid == 25:
                self.type = "higgs"
            else:
                raise NotImplementedError(
                    f"Inferring type from pdgid not implemented for pdgid {self.pdgid} "
                )

    def __post_init__(self):
        super().__post_init__()
        self._sync()

    def set_pdgid(self, pdgid):
        self.pdgid = pdgid
        self._sync()
        return self

    def set_type(self, typ):
        self.type = typ
        return self


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
    @staticmethod
    def deserialize(value: str, **kwargs) -> CSSString:
        return cssutils.parseStyle(value)

    @staticmethod
    def serialize(value: CSSString, **kwargs) -> str:
        return value.cssText.replace("\n", " ")


converter.register_converter(CSSString, CSSConverter())


@dataclass
class Bending:
    bend: Optional[float] = field(
        default=None, metadata={"xml_attribute": True, "type": "Attribute"}
    )


@dataclass
class Targeting:
    target: Optional[str] = field(default="", metadata={})

    def set_target(self, target):
        self.target = target.id
        return self


@dataclass
class Sourcing:
    source: Optional[str] = field(default="", metadata={})

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
class Connector(Labeled, Bending, Styled, PDG):
    momentum: Optional[str] = field(default=None, metadata={})
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
    sense: str = field(default=None, metadata={})

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

    def add(self, *fd_all: List[Union[Propagator, Vertex, Leg, Label]]):
        for a in fd_all:
            if isinstance(a, Propagator):
                self.propagators.append(a)
            elif isinstance(a, Vertex):
                self.vertices.append(a)
            elif isinstance(a, Leg):
                self.legs.append(a)
            elif isinstance(a, Label):
                self.labels.append(a)
            else:
                raise Exception("Unknown type: " + str(type(a)) + " " + str(a))
        return self

    def get_vertex(self, id):
        for v in self.vertices:
            if v.id == id:
                return v
        for l in self.legs:
            if l.id == id:
                return l
        return None

    def get_bounding_box(self):
        min_x = 0
        min_y = 0
        max_x = 0
        max_y = 0
        for v in self.vertices:
            min_x = min(min_x, v.x)
            min_y = min(min_y, v.y)
            max_x = max(max_x, v.x)
            max_y = max(max_y, v.y)
        for l in self.legs:
            min_x = min(min_x, l.x)
            min_y = min(min_y, l.y)
            max_x = max(max_x, l.x)
            max_y = max(max_y, l.y)
        return min_x, min_y, max_x, max_y


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
