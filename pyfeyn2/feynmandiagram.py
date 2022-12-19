import logging
import warnings
from dataclasses import dataclass, field
from typing import List, Optional, Union

import cssutils
from particle import Particle
from xsdata.formats.converter import Converter, converter

from pyfeyn2.particles import get_either_particle, get_name
from pyfeyn2.util import deprecated, withify

# We don't want to see the cssutils warnings, since we have custom properties
cssutils.log.setLevel(logging.CRITICAL)


# from pyfeyn2.propagator import Propagator
# from pyfeyn2.vertex import Vertex

# Global counter for unique ids
global_id = 0


@withify()
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


@withify()
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
                warnings.warn(
                    f"Inferring type from pdgid not implemented for pdgid {self.pdgid} "
                )
                self.type = "line"

    def __post_init__(self):
        super().__post_init__()
        self._sync()

    # def with_pdgid(self, pdgid):
    #    self.pdgid = pdgid
    #    self._sync()
    #    return self

    # def with_name(self, name):
    #    self.name = name
    #    self._sync()
    #    return self

    # TODO: remove these deprecated methods
    @deprecated(version="2.0.8", reason="Use with_...() instead")
    def set_pdgig(self, *args, **kwargs):
        return self.with_pdgid(*args, **kwargs)

    @deprecated(version="2.0.8", reason="Use with_...() instead")
    def set_type(self, *args, **kwargs):
        return self.with_type(*args, **kwargs)

    @deprecated(version="2.0.8", reason="Use with_...() instead")
    def set_name(self, *args, **kwargs):
        return self.with_name(*args, **kwargs)


@withify()
@dataclass
class Labeled:
    label: Optional[str] = field(
        default=None, metadata={"xml_attribute": True, "type": "Attribute"}
    )

    @deprecated(version="2.0.8", reason="Use with_...() instead")
    def set_label(self, *args, **kwargs):
        return self.with_label(*args, **kwargs)


@withify()
@dataclass
class Texted:
    text: Optional[str] = field(
        default="", metadata={"xml_attribute": True, "type": "Attribute"}
    )

    @deprecated(version="2.0.8", reason="Use with_...() instead")
    def set_text(self, *args, **kwargs):
        return self.with_text(*args, **kwargs)


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

    def with_point(self, p):
        self.x = float(p.x)
        self.y = float(p.y)
        return self

    def with_xy(self, x, y):
        self.x = float(x)
        self.y = float(y)
        return self

    def with_xyz(self, x, y, z):
        self.x = float(x)
        self.y = float(y)
        self.z = float(z)
        return self

    # TODO: remove these deprecated methods

    @deprecated(version="2.0.8", reason="Use with_...() instead")
    def set_point(self, *args, **kwargs):
        return self.with_point(*args, **kwargs)

    @deprecated(version="2.0.8", reason="Use with_...() instead")
    def set_xy(self, *args, **kwargs):
        return self.with_xy(*args, **kwargs)

    @deprecated(version="2.0.8", reason="Use with_...() instead")
    def set_xyz(self, *args, **kwargs):
        return self.with_xyz(*args, **kwargs)


CSSString = cssutils.css.CSSStyleDeclaration
CSSSheet = cssutils.css.CSSStyleSheet


class CSSStringConverter(Converter):
    @staticmethod
    def deserialize(value: str, **kwargs) -> CSSString:
        return cssutils.parseStyle(value)

    @staticmethod
    def serialize(value: CSSString, **kwargs) -> str:
        return value.cssText.replace("\n", " ")


class CSSSheetConverter(Converter):
    @staticmethod
    def deserialize(value: str, **kwargs) -> CSSSheet:
        return cssutils.parseString(value)

    @staticmethod
    def serialize(value: CSSSheet, **kwargs) -> str:
        return value.cssText.replace(b"\n", b" ")


converter.register_converter(CSSString, CSSStringConverter())
converter.register_converter(CSSSheet, CSSSheetConverter())


@dataclass
class Styled:
    style: CSSString = field(
        default_factory=lambda: cssutils.parseStyle(""),
        metadata={"name": "style", "xml_attribute": True, "type": "Attribute"},
    )

    clazz: Optional[str] = field(
        default=None,
        metadata={"name": "class", "xml_attribute": True, "type": "Attribute"},
    )

    def raw_style(self):
        return self.style.cssText.replace("\n", " ")

    def put_style(self, key, value):
        if self.style is not None:
            self.style.setProperty(key, value)
        return self

    def with_style(self, style):
        if style is not None:
            self.style = cssutils.parseStyle(style)
        return self

    def with_class(self, clazz):
        self.clazz = clazz
        return self


@dataclass
class Bending:
    bend: Optional[float] = field(
        default=None, metadata={"xml_attribute": True, "type": "Attribute"}
    )


@dataclass
class Targeting:
    target: Optional[str] = field(default="", metadata={})

    def with_target(self, target):
        if isinstance(target, str):
            self.target = target
        else:
            self.target = target.id
        return self

    @deprecated(version="2.0.8", reason="Use with_...() instead")
    def set_target(self, *args, **kwargs):
        return self.with_target(*args, **kwargs)


@dataclass
class Sourcing:
    source: Optional[str] = field(default="", metadata={})

    def with_source(self, source):
        if isinstance(source, str):
            self.source = source
        else:
            self.source = source.id
        return self

    @deprecated(version="2.0.8", reason="Use with_...() instead")
    def set_source(self, *args, **kwargs):
        return self.with_source(*args, **kwargs)


@dataclass
class Line(Targeting, Sourcing):
    def connect(self, source, target):
        return self.with_source(source.id).set_target(target.id)


@withify()
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

    @deprecated(version="2.0.8", reason="Use with_...() instead")
    def set_momentum(self, *args, **kwargs):
        return self.with_momentum(*args, **kwargs)

    @deprecated(version="2.0.8", reason="Use with_...() instead")
    def set_tension(self, *args, **kwargs):
        return self.with_tension(*args, **kwargs)

    @deprecated(version="2.0.8", reason="Use with_...() instead")
    def set_length(self, *args, **kwargs):
        return self.with_length(*args, **kwargs)


@withify()
@dataclass
class Leg(Point, Targeting, Connector):
    sense: str = field(default=None, metadata={})

    external: Optional[str] = field(
        default=None, metadata={"xml_attribute": True, "type": "Attribute"}
    )

    def with_incoming(self):
        self.sense = "incoming"
        return self

    def with_outgoing(self):
        self.sense = "outgoing"
        return self

    @deprecated(version="2.0.8", reason="Use with_...() instead")
    def set_external(self, *args, **kwargs):
        return self.with_external(*args, **kwargs)

    @deprecated(version="2.0.8", reason="Use with_...() instead")
    def set_incoming(self, *args, **kwargs):
        return self.with_incoming(*args, **kwargs)

    @deprecated(version="2.0.8", reason="Use with_...() instead")
    def set_outgoing(self, *args, **kwargs):
        return self.with_outgoing(*args, **kwargs)


@withify()
@dataclass
class Propagator(Line, Connector):
    pass


@withify()
@dataclass
class Label(Point, Texted, Identifiable):
    pass


@withify()
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

    sheet: CSSSheet = field(
        default_factory=lambda: cssutils.parseString(""),
        metadata={
            "name": "style",
            "xml_attribute": True,
            "type": "Attribute",
            "namespace": "",
        },
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

    def get_connections(self, vertex):
        return [
            p
            for p in self.propagators
            if p.source == vertex.id or p.target == vertex.id
        ] + [l for l in self.legs if l.target == vertex.id]

    def remove_propagator(self, propagator):
        self.propagators.remove(propagator)
        return self

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

    def with_rule(self, rule: str):
        self.sheet.add(rule)
        return self

    def with_rules(self, rules: str):
        self.sheet = cssutils.parseString(
            self.sheet.cssText.decode("utf-8") + "\n" + rules
        )
        return self

    def _get_rule_style(self, selectorText: str) -> cssutils.css.CSSStyleDeclaration:
        ret = None
        for rule in self.sheet:
            if rule.selectorText == selectorText and rule.type == rule.STYLE_RULE:
                ret = rule.style
        if ret:
            return ret
        else:
            return cssutils.css.CSSStyleDeclaration()

    def _get_class_style(self, obj: Styled) -> cssutils.css.CSSStyleDeclaration:
        cssstr = ""
        cssstr += self._get_rule_style(type(obj).__name__.lower()).cssText + ";"
        clazzes = []
        if obj.clazz:
            clazzes += obj.clazz.split()
        # pdgid is a special case of a class
        if isinstance(obj, PDG):
            if obj.pdgid:
                clazzes += ["pdgid" + str(int(obj.pdgid))]
        # first pure classes
        for clazz in clazzes:
            # css class
            cssstr += self._get_rule_style("." + clazz).cssText + ";"
        # then element + class
        for clazz in clazzes:
            # css element + class
            cssstr += (
                self._get_rule_style(type(obj).__name__.lower() + "." + clazz).cssText
                + ";"
            )

        return cssutils.css.CSSStyleDeclaration(cssText=cssstr)

    def get_style(self, obj) -> cssutils.css.CSSStyleDeclaration:
        """Get the style of an object.

        This is prefered over accessing the style attribute directly, sicne it includes class and pdgid definitions.
        """
        # selectorText is string
        cssstr = ""
        # global style
        cssstr += self._get_rule_style("*").cssText + ";"
        if isinstance(obj, str):
            cssstr += self._get_rule_style(obj).cssText + ";"
        if isinstance(obj, Styled):
            # css class
            cssstr += self._get_class_style(obj).cssText + ";"
        if isinstance(obj, Identifiable):
            # css id
            cssstr += self._get_rule_style("#" + obj.id).cssText + ";"
        if isinstance(obj, Styled):
            # specific attribute style
            cssstr += obj.style.cssText + ";"
        return cssutils.css.CSSStyleDeclaration(cssText=cssstr)


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
    description: Optional[str] = field(default="", metadata={"type": "Element"})

    # TODO setup style ?
    # style: Optional[str] = field(default="", metadata={"type": "Element"})


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
