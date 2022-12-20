import logging
import warnings
from dataclasses import dataclass, field
from typing import List, Optional, Union

import cssutils
from cssselect import GenericTranslator, SelectorError
from lxml import etree
from particle import Particle
from xsdata.formats.converter import Converter, converter
from xsdata.formats.dataclass.parsers import XmlParser
from xsdata.formats.dataclass.serializers import XmlSerializer
from xsdata.formats.dataclass.serializers.config import SerializerConfig

from pyfeyn2.particles import get_either_particle
from pyfeyn2.types import get_default_sheet
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
    id: Optional[str] = field(
        default=None, metadata={"name": "id", "namespace": "", "type": "Attribute"}
    )
    # id2: Optional[str] = field(default=None, metadata={"name": "id2", "namespace": ""})

    def __post_init__(self):
        global global_id
        if self.id is None:
            # use some global counter to generate unique id
            self.id = self.__class__.__name__ + str(global_id)
            global_id = global_id + 1


@withify()
@dataclass
class PDG(Identifiable):
    pdgid: Optional[int] = field(
        default=None, metadata={"name": "pdgid", "namespace": "", "type": "Attribute"}
    )
    """PDG ID of the particle"""
    name: Optional[str] = field(default=None, metadata={"type": "Element"})
    """Name of the particle"""
    type: Optional[str] = field(
        default=None, metadata={"xml_attribute": True, "type": "Attribute"}
    )

    # TODO check SUSY
    particle: Optional[Particle] = field(default=None, metadata={"type": "Ignore"})
    """Particle object from the particle package"""

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
            self.pdgid = int(self.particle.pdgid)

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

    @deprecated(version="2.0.7.1", reason="Use with...().")
    def set_pdgig(self, *args, **kwargs):
        return self.with_pdgid(*args, **kwargs)

    @deprecated(version="2.0.7.1", reason="Use with...().")
    def set_type(self, *args, **kwargs):
        return self.with_type(*args, **kwargs)

    @deprecated(version="2.0.7.1", reason="Use with...().")
    def set_name(self, *args, **kwargs):
        return self.with_name(*args, **kwargs)


@withify()
@dataclass
class Labeled:
    label: Optional[str] = field(
        default=None, metadata={"xml_attribute": True, "type": "Attribute"}
    )
    """Label the object"""

    @deprecated(version="2.0.7.1", reason="Use with...().")
    def set_label(self, *args, **kwargs):
        return self.with_label(*args, **kwargs)


@withify()
@dataclass
class Texted:
    text: Optional[str] = field(
        default="", metadata={"xml_attribute": True, "type": "Attribute"}
    )
    """Text the object"""

    @deprecated(version="2.0.7.1", reason='Use label=""')
    @deprecated(version="2.0.7.1", reason="Use with...().")
    def set_text(self, *args, **kwargs):
        return self.with_text(*args, **kwargs)


@dataclass
class Point:
    x: Optional[float] = field(
        default=None, metadata={"xml_attribute": True, "type": "Attribute"}
    )
    """x coordinate"""
    y: Optional[float] = field(
        default=None, metadata={"xml_attribute": True, "type": "Attribute"}
    )
    """y coordinate"""
    z: Optional[float] = field(
        default=None, metadata={"xml_attribute": True, "type": "Attribute"}
    )
    """z coordinate"""

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

    @deprecated(version="2.0.7.1", reason="Use with...().")
    def set_point(self, *args, **kwargs):
        return self.with_point(*args, **kwargs)

    @deprecated(version="2.0.7.1", reason="Use with...().")
    def set_xy(self, *args, **kwargs):
        return self.with_xy(*args, **kwargs)

    @deprecated(version="2.0.7.1", reason="Use with...().")
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
        return value.cssText.decode("utf-8")  # .replace("\n", " ")


converter.register_converter(CSSString, CSSStringConverter())
converter.register_converter(CSSSheet, CSSSheetConverter())


@dataclass
class Styled:
    style: CSSString = field(
        default_factory=lambda: cssutils.parseStyle(""),
        metadata={"name": "style", "xml_attribute": True, "type": "Attribute"},
    )
    """CSS style string."""

    clazz: Optional[str] = field(
        default=None,
        metadata={"name": "class", "xml_attribute": True, "type": "Attribute"},
    )
    """CSS class string."""

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

    @deprecated(version="2.0.7.1", reason='Use style="bend : true".')
    def with_bend(self, bend):
        self.bend = bend
        return self


@dataclass
class Targeting:
    target: Optional[str] = field(default="", metadata={})
    """Target of the object"""

    def with_target(self, target):
        if isinstance(target, str):
            self.target = target
        else:
            self.target = target.id
        return self

    @deprecated(version="2.0.7.1", reason="Use with...().")
    def set_target(self, *args, **kwargs):
        return self.with_target(*args, **kwargs)


@dataclass
class Sourcing:
    source: Optional[str] = field(default="", metadata={})
    """Source of the object"""

    def with_source(self, source):
        if isinstance(source, str):
            self.source = source
        else:
            self.source = source.id
        return self

    @deprecated(version="2.0.7.1", reason="Use with...().")
    def set_source(self, *args, **kwargs):
        return self.with_source(*args, **kwargs)


@dataclass
class Line(Targeting, Sourcing):
    def connect(self, source, target):
        return self.with_source(source.id).with_target(target.id)


@withify()
@dataclass
class Vertex(Labeled, Point, Styled, Identifiable):
    pass


@withify()
@dataclass
class Connector(Labeled, Bending, Styled, PDG):
    momentum: Optional[str] = field(default=None, metadata={})
    """Momentum of the connector"""
    tension: Optional[float] = field(
        default=None, metadata={"xml_attribute": True, "type": "Attribute"}
    )
    """Tension of the connector"""
    length: Optional[float] = field(
        default=None, metadata={"xml_attribute": True, "type": "Attribute"}
    )
    """Length of the connector"""

    @deprecated(version="2.0.7.1", reason="Use with...().")
    def set_momentum(self, *args, **kwargs):
        return self.with_momentum(*args, **kwargs)

    @deprecated(version="2.0.7.1", reason='Use style="tension=".')
    @deprecated(version="2.0.7.1", reason="Use with...().")
    def set_tension(self, *args, **kwargs):
        return self.with_tension(*args, **kwargs)

    @deprecated(version="2.0.7.1", reason='Use style="tension=".')
    @deprecated(version="2.0.7.1", reason="Use with...().")
    def set_length(self, *args, **kwargs):
        return self.with_length(*args, **kwargs)


@withify()
@dataclass
class Leg(Point, Targeting, Connector):
    sense: str = field(default=None, metadata={})
    """Sense of the leg, either 'incoming' or 'outgoing'"""

    external: Optional[str] = field(
        default=None, metadata={"xml_attribute": True, "type": "Attribute"}
    )
    """External text for leg"""

    def with_incoming(self):
        self.sense = "incoming"
        return self

    def with_outgoing(self):
        self.sense = "outgoing"
        return self

    @deprecated(version="2.0.7.1", reason="Use with...().")
    def set_external(self, *args, **kwargs):
        return self.with_external(*args, **kwargs)

    @deprecated(version="2.0.7.1", reason="Use with...().")
    def set_incoming(self, *args, **kwargs):
        return self.with_incoming(*args, **kwargs)

    @deprecated(version="2.0.7.1", reason="Use with...().")
    def set_outgoing(self, *args, **kwargs):
        return self.with_outgoing(*args, **kwargs)


@withify()
@dataclass
class Propagator(Line, Connector):
    pass


@withify()
@dataclass
class Label(Point, Texted, Identifiable):
    @deprecated(version="2.0.7.1", reason="Use a orphaned Vertex with Label.")
    def __init__(self, *args, **kwargs):
        pass


@withify()
@dataclass
class FeynmanDiagram:
    class Meta:
        name = "diagram"

    default_style: Optional[bool] = field(
        default=True,
        metadata={"name": "default_style", "xml_attribute": True, "type": "Attribute"},
    )

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

    def get_vertex(self, idd):
        for v in self.vertices:
            if v.id == idd:
                return v
        for leg in self.legs:
            if leg.id == idd:
                return leg
        return None

    def get_connections(self, vertex):
        return [
            p
            for p in self.propagators
            if p.source == vertex.id or p.target == vertex.id
        ] + [leg for leg in self.legs if leg.target == vertex.id]

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
        for leg in self.legs:
            min_x = min(min_x, leg.x)
            min_y = min(min_y, leg.y)
            max_x = max(max_x, leg.x)
            max_y = max(max_y, leg.y)
        return min_x, min_y, max_x, max_y

    def add_rule(self, rule: str):
        self.sheet.add(rule)
        return self

    def add_rules(self, rules: str):
        self.sheet = cssutils.parseString(
            self.sheet.cssText.decode("utf-8") + "\n" + rules
        )
        return self

    def with_rule(self, rule: str):
        return self.with_rules(rule)

    def with_rules(self, rules: str):
        self.sheet = cssutils.parseString(rules)
        return self

    def get_style(self, obj) -> cssutils.css.CSSStyleDeclaration:
        """Get the style of an object.

        This is prefered over accessing the style attribute directly, sicne it includes class and pdgid definitions.
        """
        # selectorText is string
        css = []
        # global style
        css += [self._get_obj_style(obj)]
        if isinstance(obj, str):
            css += [self._get_rule_style(obj)]
        if isinstance(obj, Styled):
            # specific attribute style
            css += [obj.style]
        return cssutils.css.CSSStyleDeclaration(
            cssText=";".join([c.cssText for c in css])
        )

    def _get_obj_style(self, obj: Identifiable) -> cssutils.css.CSSStyleDeclaration:
        document = etree.XML(self.to_xml().encode("ascii"))

        def lambdaselector(s, obj=obj, document=document):
            try:
                expression = GenericTranslator().css_to_xpath(s)
            except SelectorError:
                warnings.warn("Invalid selector: " + s)
                return False
            return obj.id in [e.get("id") for e in document.xpath(expression)]

        return self._get_style(lambdaselector)

    def _get_style(self, lambdaselector) -> cssutils.css.CSSStyleDeclaration:

        ret = []

        if self.default_style:
            sheets = [get_default_sheet(), self.sheet]
        else:
            sheets = [self.sheet]
        for sheet in sheets:
            idd = []
            cls = []
            rest = []
            glob = []
            for rule in sheet:
                if rule.type == rule.STYLE_RULE:
                    s = rule.selectorText
                    if lambdaselector(s):
                        if s.startswith("#"):
                            idd.append(rule)
                        elif s.startswith("["):
                            rest.append(rule)
                        elif s.startswith(":"):
                            rest.append(rule)
                        elif s.startswith("*"):
                            glob.append(rule)
                        elif s.contains("."):
                            cls.append(rule)
                        else:
                            rest.append(rule)
            ret += reversed(idd + cls + rest + glob)
        # sort rules by priority
        return cssutils.css.CSSStyleDeclaration(
            cssText=";".join([r.style.cssText for r in ret])
        )

    def to_xml(self) -> str:
        """Return self as XML."""
        config = SerializerConfig(pretty_print=True)
        serializer = XmlSerializer(config=config)
        return serializer.render(self)

    @classmethod
    def from_xml(cls, xml: str):
        """Load self from XML."""
        parser = XmlParser()
        return parser.from_string(xml, cls)


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


alias_meta = Meta


@dataclass
class Head:
    class Meta:
        name = "head"

    metas: List[alias_meta] = field(
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

    def get_diagram(self, idd):
        for d in self.diagrams:
            if d.id == idd:
                return d
        return None

    def to_xml(self) -> str:
        """Return self as XML."""
        config = SerializerConfig(pretty_print=True)
        serializer = XmlSerializer(config=config)
        return serializer.render(self)

    @classmethod
    def from_xml(cls, xml: str):
        """Load self from XML."""
        parser = XmlParser()
        return parser.from_string(xml, cls)
