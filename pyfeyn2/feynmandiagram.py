"""Moved to :py:mod:`feynml`"""
from importlib.metadata import version

from feynml.connector import Connector as Connector_
from feynml.feynmandiagram import FeynmanDiagram as FeynmanDiagram_
from feynml.feynml import FeynML as FeynML_
from feynml.feynml import Head as Head_
from feynml.feynml import Meta as Meta_
from feynml.feynml import Tool as Tool_
from feynml.leg import Leg as Leg_
from feynml.momentum import Momentum as Momentum_
from feynml.pdgid import PDG as PDG_
from feynml.point import Point as Point_
from feynml.propagator import Propagator as Propagator_
from feynml.styled import Styled as Styled_
from feynml.vertex import Vertex as Vertex_
from smpl_doc import doc

Head = doc.deprecated("2.2.6", "Directly use feynml.feynml.Head")(Head_)
Meta = doc.deprecated("2.2.6", "Directly use feynml.feynml.Meta")(Meta_)
Tool = doc.deprecated("2.2.6", "Directly use feynml.feynml.Tool")(Tool_)

Connector = doc.deprecated("2.2.6", "Directly use feynml.connector.Connector")(
    Connector_
)
FeynmanDiagram = doc.deprecated(
    "2.2.6", "Directly use feynml.feynmandiagram.FeynDiagram"
)(FeynmanDiagram_)
Leg = doc.deprecated("2.2.6", "Directly use feynml.leg.Leg")(Leg_)
Momentum = doc.deprecated("2.2.6", "Directly use feynml.momentum.Momentum")(Momentum_)
PDG = doc.deprecated("2.2.6", "Directly use feynml.pdg.PDG")(PDG_)
Vertex = doc.deprecated("2.2.6", "Directly use feynml.vertex.Vertex")(Vertex_)
Styled = doc.deprecated("2.2.6", "Directly use feynml.styled.Styled")(Styled_)
Propagator = doc.deprecated("2.2.6", "Directly use feynml.propagator.Propagator")(
    Propagator_
)
Point = doc.deprecated("2.2.6", "Directly use feynml.point.Point")(Point_)


@doc.deprecated("2.2.6", "Directly use feynml.feynml.FeynML")
class FeynML(FeynML_):
    """FeynML with pyfeyn2 meta tag."""

    def __post_init__(self):
        self.head.metas.append(Meta("pyfeyn2", version("pyfeyn2")))
        return super().__post_init__()
