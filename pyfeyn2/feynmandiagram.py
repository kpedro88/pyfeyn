from dataclasses import dataclass, field
from typing import List, Optional

# from pyfeyn2.propagator import Propagator
# from pyfeyn2.vertex import Vertex


@dataclass
class Vertex:
    id: Optional[str] = field(
        default="P1", metadata={"xml_attribute": True, "type": "Attribute"}
    )
    name: str = field(default=0, metadata={"xml_attribute": True, "type": "Attribute"})


@dataclass
class Propagator:
    id: Optional[str] = field(
        default="P1", metadata={"xml_attribute": True, "type": "Attribute"}
    )
    pdgid: Optional[int] = field(
        default=0, metadata={"xml_attribute": True, "type": "Attribute"}
    )
    name: str = field(default=0, metadata={"xml_attribute": True, "type": "Attribute"})


@dataclass
class FeynmanDiagram:
    class Meta:
        name = "FeynmanDiagram"

    propagators: List[Propagator] = field(
        default_factory=list,
        metadata={"name": "Propagator", "type": "Element", "namespace": ""},
    )
    vertices: List[Vertex] = field(
        default_factory=list,
        metadata={"name": "Vertex", "type": "Element", "namespace": ""},
    )
